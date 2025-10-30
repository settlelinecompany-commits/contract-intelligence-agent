FROM pytorch/pytorch:2.9.0-cuda12.8-cudnn9-runtime

WORKDIR /

RUN pip install --no-cache-dir runpod surya-ocr Pillow pypdfium2

# Pre-download ALL models including the 1.34GB Foundation model
# This happens during docker build, so models are baked into image (no runtime downloads)
COPY preload_models.py /
RUN python3 /preload_models.py && rm /preload_models.py

COPY rp_handler.py /

CMD ["python3", "-u", "rp_handler.py"]
