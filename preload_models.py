#!/usr/bin/env python3
"""
Pre-download all Surya OCR models during Docker build
This ensures all model weights are baked into the Docker image
"""
import sys

print('Starting model downloads...')
sys.stdout.flush()

# Download Foundation model (1.34GB)
print('Downloading Foundation model (1.34GB)...')
sys.stdout.flush()
from surya.foundation import FoundationPredictor
foundation = FoundationPredictor()
print('✅ Foundation model downloaded.')
sys.stdout.flush()

# Download Recognition model (~73MB)
print('Downloading Recognition model (~73MB)...')
sys.stdout.flush()
from surya.recognition import RecognitionPredictor
recognition = RecognitionPredictor(foundation)
print('✅ Recognition model downloaded.')
sys.stdout.flush()

# Download Detection model (~73MB)
print('Downloading Detection model (~73MB)...')
sys.stdout.flush()
from surya.detection import DetectionPredictor
detection = DetectionPredictor()
print('✅ Detection model downloaded.')
sys.stdout.flush()

# Verify cache size
import os
cache_dir = os.path.expanduser('~/.cache')
if os.path.exists(cache_dir):
    import subprocess
    try:
        result = subprocess.run(['du', '-sh', cache_dir], capture_output=True, text=True)
        print(f'Total cache size: {result.stdout.strip()}')
    except Exception as e:
        print(f'Could not check cache size: {e}')

print('✅ All models pre-downloaded successfully - ready for fast cold starts!')
sys.stdout.flush()

