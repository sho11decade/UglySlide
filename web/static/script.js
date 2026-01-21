// Global variables
let selectedFile = null;
let processedFilename = null;

// DOM Elements
const fileInput = document.getElementById('fileInput');
const uploadArea = document.getElementById('uploadArea');
const selectedFileDiv = document.getElementById('selectedFile');
const fileNameSpan = document.getElementById('fileName');
const settingsSection = document.getElementById('settingsSection');
const processingSection = document.getElementById('processingSection');
const resultsSection = document.getElementById('resultsSection');
const errorSection = document.getElementById('errorSection');
const designLevel = document.getElementById('designLevel');
const contentLevel = document.getElementById('contentLevel');
const designLevelValue = document.getElementById('designLevelValue');
const contentLevelValue = document.getElementById('contentLevelValue');
const reduceMotionToggle = document.getElementById('reduceMotionToggle');
const highContrastToggle = document.getElementById('highContrastToggle');
const largeTextToggle = document.getElementById('largeTextToggle');

// Event Listeners
uploadArea.addEventListener('click', () => fileInput.click());
uploadArea.addEventListener('dragover', (e) => {
    e.preventDefault();
    uploadArea.classList.add('dragover');
});

uploadArea.addEventListener('keydown', (e) => {
    if (e.key === ' ' || e.key === 'Enter') {
        e.preventDefault();
        fileInput.click();
    }
    if (e.key === 'Escape') {
        fileInput.value = '';
        selectedFile = null;
        uploadArea.classList.remove('dragover');
    }
});

uploadArea.addEventListener('dragleave', () => {
    uploadArea.classList.remove('dragover');
});

uploadArea.addEventListener('drop', (e) => {
    e.preventDefault();
    uploadArea.classList.remove('dragover');
    
    const files = e.dataTransfer.files;
    if (files.length > 0) {
        handleFileSelection(files[0]);
    }
});

fileInput.addEventListener('change', (e) => {
    if (e.target.files.length > 0) {
        handleFileSelection(e.target.files[0]);
    }
});

document.getElementById('clearFileBtn').addEventListener('click', () => {
    selectedFile = null;
    fileInput.value = '';
    selectedFileDiv.style.display = 'none';
    settingsSection.style.display = 'none';
    uploadArea.classList.remove('dragover');
});

designLevel.addEventListener('input', (e) => {
    designLevelValue.textContent = e.target.value;
});

contentLevel.addEventListener('input', (e) => {
    contentLevelValue.textContent = e.target.value;
});

// Accessibility toggles
[reduceMotionToggle, highContrastToggle, largeTextToggle].forEach((el) => {
    el.addEventListener('change', applyAccessibilityPrefs);
});

function applyAccessibilityPrefs() {
    const body = document.body;
    body.classList.toggle('reduce-motion', reduceMotionToggle.checked);
    body.classList.toggle('high-contrast', highContrastToggle.checked);
    body.classList.toggle('large-text', largeTextToggle.checked);
}

/**
 * Handle file selection
 */
function handleFileSelection(file) {
    // Validate file type
    if (!file.name.endsWith('.pptx')) {
        showError('PPTXファイルのみ対応しています。');
        return;
    }
    
    // Validate file size (50MB)
    const maxSize = 50 * 1024 * 1024;
    if (file.size > maxSize) {
        showError('ファイルサイズが大きすぎます。最大50MBです。');
        return;
    }
    
    // Store file and show settings
    selectedFile = file;
    fileNameSpan.textContent = file.name;
    selectedFileDiv.style.display = 'flex';
    settingsSection.style.display = 'block';
    uploadArea.style.display = 'none';
    
    // Hide other sections
    errorSection.style.display = 'none';
    resultsSection.style.display = 'none';
}

/**
 * Process presentation with improved error handling
 */
async function processPresentation() {
    if (!selectedFile) {
        showError('ファイルを選択してください。');
        return;
    }
    
    // Hide previous sections and show processing
    settingsSection.style.display = 'none';
    errorSection.style.display = 'none';
    resultsSection.style.display = 'none';
    processingSection.style.display = 'block';
    processingSection.setAttribute('aria-busy', 'true');
    
    // Reset progress bar
    const progressFill = document.getElementById('progressFill');
    progressFill.style.width = '0%';
    progressFill.setAttribute('aria-valuenow', '0');
    const startTime = Date.now();
    let isProcessing = true;
    
    try {
        // Create FormData
        const formData = new FormData();
        formData.append('file', selectedFile);
        
        // Make request with query parameters
        const designLevelVal = parseInt(designLevel.value);
        const contentLevelVal = parseInt(contentLevel.value);
        
        // Update status text
        const statusText = document.getElementById('statusText');
        
        const response = await fetch(
            `/api/process?design_level=${designLevelVal}&content_level=${contentLevelVal}`,
            {
                method: 'POST',
                body: formData,
                timeout: 300000 // 5 minute timeout
            }
        );
        
        // Simulate progress
        let progress = 0;
        const progressInterval = setInterval(() => {
            progress = Math.min(progress + Math.random() * 15, 85);
            progressFill.style.width = progress + '%';
            progressFill.setAttribute('aria-valuenow', Math.round(progress));
            
            // Update status
            const elapsedSeconds = Math.floor((Date.now() - startTime) / 1000);
            statusText.textContent = `処理中... (${elapsedSeconds}秒経過)`;
        }, 300);
        
        if (!response.ok) {
            clearInterval(progressInterval);
            const contentType = response.headers.get('content-type');
            let error;
            
            if (contentType && contentType.includes('application/json')) {
                error = await response.json();
                throw new Error(error.error || `エラー (${response.status})`);
            } else {
                throw new Error(`サーバーエラー: ${response.status} ${response.statusText}`);
            }
        }
        
        const result = await response.json();
        clearInterval(progressInterval);
        progressFill.style.width = '100%';
        progressFill.setAttribute('aria-valuenow', '100');
        
        const elapsedTime = ((Date.now() - startTime) / 1000).toFixed(1);
        
        // Show results
        setTimeout(() => {
            showResults(result, elapsedTime);
        }, 500);
        
    } catch (error) {
        processingSection.style.display = 'none';
        processingSection.setAttribute('aria-busy', 'false');
        
        // Provide specific error messages
        let errorMessage = error.message || 'エラーが発生しました。もう一度試してください。';
        
        if (errorMessage.includes('429')) {
            errorMessage = 'リクエストが多すぎます。しばらく待ってからお試しください。';
        } else if (errorMessage.includes('413')) {
            errorMessage = 'ファイルサイズが大きすぎます。50MB以下のファイルをお使いください。';
        } else if (errorMessage.includes('timeout')) {
            errorMessage = '処理がタイムアウトしました。ファイルサイズが大きくないか確認してください。';
        }
        
        showError(errorMessage);
    }
}

/**
 * Show results with elapsed time
 */
function showResults(result, elapsedTime) {
    processingSection.style.display = 'none';
    processingSection.setAttribute('aria-busy', 'false');
    resultsSection.style.display = 'block';
    resultsSection.focus();
    
    // Store filename for download
    processedFilename = result.filename;
    
    // Display analysis results
    const resultsList = document.getElementById('resultsList');
    resultsList.innerHTML = '';

    // Show processing time
    if (elapsedTime) {
        const liTime = document.createElement('li');
        liTime.textContent = `⏱️ 処理時間: ${elapsedTime}秒`;
        liTime.style.color = '#00ff00';
        liTime.style.fontWeight = 'bold';
        resultsList.appendChild(liTime);
    }

    // Optional seed info
    if (result.seed !== undefined && result.seed !== null) {
        const liSeed = document.createElement('li');
        liSeed.textContent = `🌱 シード: ${result.seed}`;
        resultsList.appendChild(liSeed);
    }
    
    if (result.analysis_before && result.analysis_after) {
        const before = result.analysis_before;
        const after = result.analysis_after;
        const sections = [
            { title: '処理前', data: before },
            { title: '処理後', data: after },
        ];
        sections.forEach(sec => {
            const header = document.createElement('li');
            header.textContent = `━━━ ${sec.title} ━━━`;
            header.style.fontWeight = 'bold';
            header.style.color = '#ff00ff';
            resultsList.appendChild(header);
            [
                { label: 'スライド数', value: sec.data.total_slides || 0, icon: '📄' },
                { label: '検出されたフォント', value: sec.data.fonts_found || 0, icon: '🔤' },
                { label: '検出された色', value: sec.data.colors_found || 0, icon: '🎨' },
                { label: '検出されたアニメーション', value: sec.data.animations_found || 0, icon: '✨' },
            ].forEach(item => {
                const li = document.createElement('li');
                li.textContent = `${item.icon} ${item.label}: ${item.value}`;
                resultsList.appendChild(li);
            });
        });
    } else {
        const analysis = result.analysis || {};
        const items = [
            { label: 'スライド数', value: analysis.total_slides || 0, icon: '📄' },
            { label: '検出されたフォント', value: analysis.fonts_found || 0, icon: '🔤' },
            { label: '検出された色', value: analysis.colors_found || 0, icon: '🎨' },
            { label: '検出されたアニメーション', value: analysis.animations_found || 0, icon: '✨' },
        ];
        items.forEach(item => {
            const li = document.createElement('li');
            li.textContent = `${item.icon} ${item.label}: ${item.value}`;
            resultsList.appendChild(li);
        });
    }
}

/**
 * Download file
 */
async function downloadFile() {
    if (!processedFilename) {
        showError('ファイル情報が失われました。もう一度処理してください。');
        return;
    }
    
    try {
        const response = await fetch(`/api/download/${encodeURIComponent(processedFilename)}`);
        
        if (!response.ok) {
            throw new Error('ダウンロードに失敗しました。');
        }
        
        // Create blob and download
        const blob = await response.blob();
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = processedFilename;
        document.body.appendChild(a);
        a.click();
        window.URL.revokeObjectURL(url);
        document.body.removeChild(a);
        
    } catch (error) {
        showError('ダウンロードに失敗しました: ' + error.message);
    }
}

/**
 * Reset form
 */
function resetForm() {
    selectedFile = null;
    processedFilename = null;
    fileInput.value = '';
    selectedFileDiv.style.display = 'none';
    settingsSection.style.display = 'none';
    processingSection.style.display = 'none';
    resultsSection.style.display = 'none';
    errorSection.style.display = 'none';
    uploadArea.style.display = 'block';
    uploadArea.classList.remove('dragover');
    
    // Reset sliders
    designLevel.value = 7;
    contentLevel.value = 7;
    designLevelValue.textContent = 7;
    contentLevelValue.textContent = 7;
}

/**
 * Show error message
 */
function showError(message) {
    processingSection.style.display = 'none';
    resultsSection.style.display = 'none';
    settingsSection.style.display = 'none';
    errorSection.style.display = 'block';
    
    document.getElementById('errorMessage').textContent = message;
    errorSection.focus();
}

/**
 * Health check
 */
async function checkHealth() {
    try {
        const response = await fetch('/api/health');
        if (!response.ok) {
            console.error('Health check failed');
        }
    } catch (error) {
        console.error('Cannot connect to server:', error);
    }
}

// Initial setup
// デフォルトでアニメーション抑制を有効化
if (reduceMotionToggle && !reduceMotionToggle.checked) {
    reduceMotionToggle.checked = true;
}
checkHealth();
applyAccessibilityPrefs();
