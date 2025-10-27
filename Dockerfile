# BACKUP VERSION - Simple Python setup (working)
# FROM python:3.10-slim
# WORKDIR /
# RUN pip install --no-cache-dir runpod
# COPY rp_handler.py /
# CMD ["python3", "-u", "rp_handler.py"]

# OCR VERSION - PyTorch with CUDA for Surya OCR
FROM pytorch/pytorch:2.9.0-cuda12.8-cudnn9-runtime

WORKDIR /

# Install Surya OCR and dependencies
RUN pip install --no-cache-dir runpod surya-ocr Pillow pypdfium2

# Copy your handler file
COPY rp_handler.py /

# Start the container
CMD ["python3", "-u", "rp_handler.py"]