"""Flask Web Application for DasaMaker"""

import logging
import os
import uuid
from pathlib import Path
from tempfile import TemporaryDirectory
from werkzeug.utils import secure_filename
from functools import wraps
from datetime import datetime, timedelta

from flask import Flask, render_template, request, send_file, jsonify, after_this_request
from pptx import Presentation

# Import our modules
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))
from src.ppt_analyzer import PPTAnalyzer
from src.taco_generator import TacoGenerator
from src.content_transformer import ContentTransformer

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Flask app configuration
from config import Config

app = Flask(__name__)
# Apply config values
app.config['MAX_CONTENT_LENGTH'] = Config.MAX_FILE_SIZE
app.config['UPLOAD_FOLDER'] = Config.get_upload_folder()
app.config['JSON_SORT_KEYS'] = False

# Create upload folder if it doesn't exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Allowed file extension
ALLOWED_EXTENSIONS = Config.ALLOWED_EXTENSIONS

# Rate limiting tracker (in-memory, simple implementation)
request_timestamps = {}

def rate_limit(max_requests=20, window_seconds=3600):
    """Simple rate limiter decorator"""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            client_ip = request.remote_addr
            now = datetime.now()
            
            # Clean up old entries
            if client_ip in request_timestamps:
                request_timestamps[client_ip] = [
                    ts for ts in request_timestamps[client_ip]
                    if now - ts < timedelta(seconds=window_seconds)
                ]
            else:
                request_timestamps[client_ip] = []
            
            # Check rate limit
            if len(request_timestamps[client_ip]) >= max_requests:
                logger.warning(f"Rate limit exceeded for IP: {client_ip}")
                return jsonify({'error': 'リクエストが多すぎます。しばらく待ってからお試しください。'}), 429
            
            request_timestamps[client_ip].append(now)
            return f(*args, **kwargs)
        return decorated_function
    return decorator


def allowed_file(filename: str) -> bool:
    """Check if file extension is allowed"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def generate_output_filename(original_filename: str) -> str:
    """Generate output filename with TACKY suffix"""
    name, ext = os.path.splitext(original_filename)
    return f"{name}_TACKY.pptx"


@app.route('/')
def index():
    """Render main page"""
    return render_template('index.html')


@app.route('/api/process', methods=['POST'])
@rate_limit(max_requests=10, window_seconds=3600)
def process_presentation():
    """
    Process uploaded PPTX file and generate tacky version
    
    Query parameters:
    - design_level: Design tackiness level (1-10, default=7)
    - content_level: Content transformation intensity (1-10, default=7)
    - seed: Optional integer seed for deterministic output
    """
    
    try:
        # Check if file is present
        if 'file' not in request.files:
            return jsonify({'error': 'ファイルが選択されていません'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'ファイルが選択されていません'}), 400
        
        if not allowed_file(file.filename):
            return jsonify({'error': 'PPTXファイルのみ対応しています'}), 400
        
        # Validate filename for path traversal
        try:
            secure_input_filename = secure_filename(file.filename)
            if not secure_input_filename or secure_input_filename == '':
                return jsonify({'error': 'ファイル名が無効です'}), 400
        except Exception:
            return jsonify({'error': 'ファイル名が無効です'}), 400
        
        # Get tackiness levels from request
        try:
            design_level = int(request.args.get('design_level', 7))
            content_level = int(request.args.get('content_level', 7))
            
            # Validate ranges
            if not (1 <= design_level <= 10):
                design_level = 7
            if not (1 <= content_level <= 10):
                content_level = 7
                
            seed = request.args.get('seed')
            seed = int(seed) if seed is not None and str(seed).isdigit() else None
        except (ValueError, TypeError):
            return jsonify({'error': 'パラメータが無効です'}), 400
        
        # Create temporary file
        temp_input_path = os.path.join(
            app.config['UPLOAD_FOLDER'],
            f"input_{uuid.uuid4().hex}.pptx"
        )
        
        # Save uploaded file
        try:
            file.save(temp_input_path)
            logger.info(f"File saved: {temp_input_path}")
        except Exception as e:
            logger.error(f"Failed to save file: {e}")
            return jsonify({'error': 'ファイルの保存に失敗しました'}), 500
        
        try:
            # Check file size again after save (just in case)
            file_size = os.path.getsize(temp_input_path)
            if file_size > Config.MAX_FILE_SIZE:
                return jsonify({'error': 'ファイルサイズが制限を超えています'}), 413
            
            # Step 1: Analyze original presentation
            logger.info("Step 1: Analyzing presentation...")
            analyzer = PPTAnalyzer(temp_input_path)
            analysis_before = analyzer.analyze()
            logger.info(f"Analysis complete: {analysis_before.to_dict()}")
            
            # Step 2: Load presentation for modifications
            logger.info("Step 2: Loading presentation for modifications...")
            presentation = Presentation(temp_input_path)
            
            # Step 3: Apply tacky design
            logger.info(f"Step 3: Applying tacky design (level {design_level})...")
            design_generator = TacoGenerator(presentation, tacky_level=design_level, seed=seed)
            design_generator.apply_tacky_design()
            
            # Step 4: Apply content transformation
            logger.info(f"Step 4: Applying content transformation (intensity {content_level})...")
            content_transformer = ContentTransformer(presentation, intensity=content_level, seed=seed)
            content_transformer.transform_all_content()
            
            # Step 5: Save output
            output_filename = generate_output_filename(secure_filename(file.filename))
            temp_output_path = os.path.join(app.config['UPLOAD_FOLDER'], output_filename)
            
            logger.info(f"Step 5: Saving output to {temp_output_path}...")
            presentation.save(temp_output_path)
            
            # Optionally analyze after modifications for before/after comparison
            try:
                analysis_after = PPTAnalyzer(temp_output_path).analyze()
            except Exception as e:
                logger.warning(f"Failed to analyze output file: {e}")
                analysis_after = None

            logger.info("Processing complete!")
            
            # Return success with file info
            response_payload = {
                'success': True,
                'filename': output_filename,
                'seed': seed,
                'analysis': {
                    'total_slides': analysis_before.total_slides,
                    'fonts_found': len(analysis_before.fonts),
                    'colors_found': len(analysis_before.colors),
                    'animations_found': analysis_before.animation_count,
                }
            }
            if analysis_after is not None:
                response_payload['analysis_before'] = response_payload.pop('analysis')
                response_payload['analysis_after'] = {
                    'total_slides': analysis_after.total_slides,
                    'fonts_found': len(analysis_after.fonts),
                    'colors_found': len(analysis_after.colors),
                    'animations_found': analysis_after.animation_count,
                }

            return jsonify(response_payload)
        
        finally:
            # Clean up input file
            if os.path.exists(temp_input_path):
                try:
                    os.remove(temp_input_path)
                    logger.info(f"Cleaned up input file: {temp_input_path}")
                except Exception as e:
                    logger.warning(f"Failed to clean up input file: {e}")
    
    except Exception as e:
        logger.error(f"Error processing file: {e}", exc_info=True)
        return jsonify({'error': 'ファイルの処理に失敗しました。ファイル形式が正しいか確認してください。'}), 500
    """
    Process uploaded PPTX file and generate tacky version
    
    Query parameters:
    - design_level: Design tackiness level (1-10, default=7)
    - content_level: Content transformation intensity (1-10, default=7)
    - seed: Optional integer seed for deterministic output
    """
    
    try:
        # Check if file is present
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        if not allowed_file(file.filename):
            return jsonify({'error': 'File must be PPTX format'}), 400
        
        # Get tackiness levels from request
        design_level = int(request.args.get('design_level', 7))
        content_level = int(request.args.get('content_level', 7))
        seed = request.args.get('seed')
        seed = int(seed) if seed is not None and str(seed).isdigit() else None
        
        # Create temporary file
        temp_input_path = os.path.join(
            app.config['UPLOAD_FOLDER'],
            f"input_{uuid.uuid4().hex}.pptx"
        )
        
        # Save uploaded file
        file.save(temp_input_path)
        logger.info(f"File saved: {temp_input_path}")
        
        try:
            # Step 1: Analyze original presentation
            logger.info("Step 1: Analyzing presentation...")
            analyzer = PPTAnalyzer(temp_input_path)
            analysis_before = analyzer.analyze()
            logger.info(f"Analysis complete: {analysis_before.to_dict()}")
            
            # Step 2: Load presentation for modifications
            logger.info("Step 2: Loading presentation for modifications...")
            presentation = Presentation(temp_input_path)
            
            # Step 3: Apply tacky design
            logger.info(f"Step 3: Applying tacky design (level {design_level})...")
            design_generator = TacoGenerator(presentation, tacky_level=design_level, seed=seed)
            design_generator.apply_tacky_design()
            
            # Step 4: Apply content transformation
            logger.info(f"Step 4: Applying content transformation (intensity {content_level})...")
            content_transformer = ContentTransformer(presentation, intensity=content_level, seed=seed)
            content_transformer.transform_all_content()
            
            # Step 5: Save output
            output_filename = generate_output_filename(secure_filename(file.filename))
            temp_output_path = os.path.join(app.config['UPLOAD_FOLDER'], output_filename)
            
            logger.info(f"Step 5: Saving output to {temp_output_path}...")
            presentation.save(temp_output_path)
            
            # Optionally analyze after modifications for before/after comparison
            try:
                analysis_after = PPTAnalyzer(temp_output_path).analyze()
            except Exception:
                analysis_after = None

            logger.info("Processing complete!")
            
            # Return success with file info
            response_payload = {
                'success': True,
                'filename': output_filename,
                'seed': seed,
                'analysis': {
                    'total_slides': analysis_before.total_slides,
                    'fonts_found': len(analysis_before.fonts),
                    'colors_found': len(analysis_before.colors),
                    'animations_found': analysis_before.animation_count,
                }
            }
            if analysis_after is not None:
                response_payload['analysis_before'] = response_payload.pop('analysis')
                response_payload['analysis_after'] = {
                    'total_slides': analysis_after.total_slides,
                    'fonts_found': len(analysis_after.fonts),
                    'colors_found': len(analysis_after.colors),
                    'animations_found': analysis_after.animation_count,
                }

            return jsonify(response_payload)
        
        finally:
            # Clean up input file
            if os.path.exists(temp_input_path):
                os.remove(temp_input_path)
                logger.info(f"Cleaned up input file: {temp_input_path}")
    
    except Exception as e:
        logger.error(f"Error processing file: {e}", exc_info=True)
        return jsonify({'error': f'Processing failed: {str(e)}'}), 500


@app.route('/api/download/<filename>')
def download_file(filename: str):
    """
    Download processed PPTX file
    
    Args:
        filename: Name of the file to download
    """
    
    try:
        # Validate filename (prevent directory traversal)
        filename = secure_filename(filename)
        if not filename:
            return jsonify({'error': 'ファイル名が無効です'}), 400
            
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        
        # Check if file exists
        if not os.path.exists(filepath):
            logger.warning(f"Download requested for non-existent file: {filename}")
            return jsonify({'error': 'ファイルが見つかりません'}), 404
        
        # Check if file is in the correct directory (path traversal prevention)
        if not os.path.abspath(filepath).startswith(os.path.abspath(app.config['UPLOAD_FOLDER'])):
            logger.error(f"Potential path traversal attempt: {filename}")
            return jsonify({'error': 'ファイルアクセスが拒否されました'}), 403
        
        # Check file size
        file_size = os.path.getsize(filepath)
        if file_size == 0:
            logger.warning(f"Zero-sized file detected: {filename}")
            return jsonify({'error': 'ファイルが壊れています'}), 400
        
        logger.info(f"Downloading file: {filename} (size: {file_size} bytes)")

        @after_this_request
        def remove_file(response):
            try:
                if os.path.exists(filepath):
                    os.remove(filepath)
                    logger.info(f"Cleaned up file after send: {filepath}")
            except Exception as e:
                logger.debug(f"Could not clean up file after send: {e}")
            return response

        # Set cache headers to prevent caching
        response = send_file(
            filepath,
            mimetype='application/vnd.openxmlformats-officedocument.presentationml.presentation',
            as_attachment=True,
            download_name=filename
        )
        response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
        response.headers['Pragma'] = 'no-cache'
        return response
    
    except Exception as e:
        logger.error(f"Error downloading file: {e}")
        return jsonify({'error': 'ダウンロードに失敗しました'}), 500
    
    finally:
        # Post-response cleanup handled by after_this_request
        pass


@app.route('/api/health')
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'ok',
        'version': '0.1.0',
        'timestamp': datetime.now().isoformat()
    })


@app.errorhandler(413)
def request_entity_too_large(error):
    """Handle file too large error"""
    logger.warning(f"File too large error: {error}")
    return jsonify({'error': 'ファイルサイズが大きすぎます（最大50MB）'}), 413


@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    logger.warning(f"404 error: {error}")
    return jsonify({'error': 'ページが見つかりません'}), 404


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    logger.error(f"Internal server error: {error}")
    return jsonify({'error': 'サーバーエラーが発生しました。管理者に連絡してください。'}), 500


@app.errorhandler(429)
def rate_limited(error):
    """Handle rate limit errors"""
    logger.warning(f"Rate limit exceeded: {error}")
    return jsonify({'error': 'リクエストが多すぎます。しばらく待ってからお試しください。'}), 429


# Security headers
@app.after_request
def set_security_headers(response):
    """Add security headers to responses"""
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'SAMEORIGIN'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
    return response


if __name__ == '__main__':
    # Check environment
    debug_mode = os.getenv('FLASK_ENV', 'production') == 'development'
    
    logger.info("=" * 60)
    logger.info("Starting DasaMaker Flask application...")
    logger.info(f"Debug mode: {debug_mode}")
    logger.info(f"Upload folder: {app.config['UPLOAD_FOLDER']}")
    logger.info(f"Max file size: {app.config['MAX_CONTENT_LENGTH'] / (1024*1024):.1f} MB")
    logger.info("=" * 60)
    
    app.run(debug=debug_mode, host='0.0.0.0', port=5000, threaded=True)
