import os
import requests
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import PlainTextResponse, JSONResponse

ENCODER_URL = os.getenv("ENCODER_URL", "https://contract-parser-api.vercel.app/encode")
RUNPOD_API_URL = "https://api.runpod.ai/v2/01s4u2uzv9343o/runsync"
RUNPOD_API_KEY = os.getenv("RUNPOD_API_KEY")

app = FastAPI(title="OCR Proxy API")

@app.post("/ocr")
async def ocr_pdf(file: UploadFile = File(...)):
    try:
        if not file.filename.endswith('.pdf'):
            return JSONResponse(status_code=400, content={"error": "Only PDF files are supported"})

        # Read PDF bytes
        pdf_bytes = await file.read()
        if not pdf_bytes:
            return JSONResponse(status_code=400, content={"error": "Empty file"})

        # 1) Call encoder to get base64 (no RunPod here)
        enc_resp = requests.post(
            ENCODER_URL,
            headers={"Content-Type": "application/pdf"},
            data=pdf_bytes,
            timeout=30
        )
        if not enc_resp.ok:
            return JSONResponse(status_code=enc_resp.status_code, content={"error": f"Encoder error: {enc_resp.text}"})
        enc_json = enc_resp.json()
        pdf_base64 = enc_json.get("base64")
        if not pdf_base64:
            return JSONResponse(status_code=500, content={"error": "Encoder did not return base64"})

        # 2) Call RunPod with base64 (exact format RunPod expects)
        rp_resp = requests.post(
            RUNPOD_API_URL,
            headers={
                "Authorization": f"Bearer {RUNPOD_API_KEY}",
                "Content-Type": "application/json"
            },
            json={"input": {"pdf_data": pdf_base64}},
            timeout=120
        )
        if not rp_resp.ok:
            return JSONResponse(status_code=rp_resp.status_code, content={"error": f"RunPod API error: {rp_resp.text}"})

        rp_json = rp_resp.json()
        ocr_data = rp_json.get("output", rp_json)
        if not ocr_data or not ocr_data.get("success"):
            return JSONResponse(status_code=500, content={"error": ocr_data.get("error", "OCR processing failed")})

        ocr_text = ocr_data.get("ocr_text", "")
        return PlainTextResponse(content=ocr_text)

    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})