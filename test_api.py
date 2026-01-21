#!/usr/bin/env python
"""Test Flask API file processing"""

import os
import sys
import requests
from pathlib import Path

# Wait a moment for the server to start
import time

BASE_URL = 'http://localhost:5000'
TEST_FILE = 'samples/test_sample.pptx'

print('Testing Flask API...')
print(f'Base URL: {BASE_URL}')
print(f'Test file: {TEST_FILE}')

# Check file exists
if not os.path.exists(TEST_FILE):
    print(f'✗ Test file not found: {TEST_FILE}')
    sys.exit(1)

print(f'✓ Test file found ({os.path.getsize(TEST_FILE)} bytes)')

# Test 1: Health check
print('\n1. Testing /api/health...')
try:
    response = requests.get(f'{BASE_URL}/api/health', timeout=5)
    print(f'   Status: {response.status_code}')
    print(f'   Response: {response.json()}')
except Exception as e:
    print(f'   ✗ Error: {e}')
    sys.exit(1)

# Test 2: Process file
print('\n2. Testing /api/process...')
try:
    with open(TEST_FILE, 'rb') as f:
        files = {'file': f}
        params = {'design_level': 5, 'content_level': 5}
        response = requests.post(
            f'{BASE_URL}/api/process',
            files=files,
            params=params,
            timeout=30
        )
    
    print(f'   Status: {response.status_code}')
    result = response.json()
    print(f'   Response: {result}')
    
    if response.status_code != 200:
        print(f'   ✗ Processing failed')
        sys.exit(1)
    
    filename = result.get('filename')
    print(f'   ✓ Output filename: {filename}')
    
    # Test 3: Download file
    print(f'\n3. Testing /api/download/{filename}...')
    response = requests.get(
        f'{BASE_URL}/api/download/{filename}',
        timeout=30
    )
    print(f'   Status: {response.status_code}')
    print(f'   Content-Length: {len(response.content)} bytes')
    
    if response.status_code != 200:
        print(f'   ✗ Download failed: {response.text}')
        sys.exit(1)
    
    # Save downloaded file
    download_path = 'samples/test_download.pptx'
    with open(download_path, 'wb') as f:
        f.write(response.content)
    
    print(f'   ✓ Downloaded: {download_path}')
    print(f'   ✓ Downloaded file size: {os.path.getsize(download_path)} bytes')
    
    # Try to open it
    print(f'\n4. Verifying downloaded file...')
    from pptx import Presentation
    try:
        prs = Presentation(download_path)
        print(f'   ✓ File opens successfully: {len(prs.slides)} slides')
    except Exception as e:
        print(f'   ✗ Cannot open file: {e}')
        sys.exit(1)
    
    print('\n--- All API tests passed! ---')

except Exception as e:
    print(f'   ✗ Error: {e}')
    import traceback
    traceback.print_exc()
    sys.exit(1)
