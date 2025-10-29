FROM pytorch/pytorch:2.9.0-cuda12.8-cudnn9-runtime

WORKDIR /

RUN pip install --no-cache-dir runpod surya-ocr Pillow pypdfium2

COPY rp_handler.py /

CMD ["python3", "-u", "rp_handler.py"]
