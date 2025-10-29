import runpod
import time  
import json
import base64
import io
from PIL import Image
import pypdfium2 as pdfium
from surya.foundation import FoundationPredictor
from surya.recognition import RecognitionPredictor
from surya.detection import DetectionPredictor

# Initialize models once (global)
foundation_predictor = FoundationPredictor()
recognition_predictor = RecognitionPredictor(foundation_predictor)
detection_predictor = DetectionPredictor()

def pdf_to_images(pdf_bytes: bytes):
    """Convert PDF to PIL images"""
    f = io.BytesIO(pdf_bytes)
    doc = pdfium.PdfDocument(f)
    imgs = []
    for i in range(len(doc)):
        page = doc[i]
        pil = page.render(scale=2.0).to_pil()  # 2x scale for quality
        imgs.append(pil)
    return imgs

def run_surya_ocr(images):
    """Run Surya OCR on images"""
    preds = recognition_predictor(images, det_predictor=detection_predictor)
    pages = []
    for p in preds:
        lines = []
        if hasattr(p, "text_lines"):
            for ln in p.text_lines:
                t = getattr(ln, "text", "")
                if t and t.strip():
                    lines.append(t)
        pages.append("\n".join(lines))
    return "\n\n".join(pages)

def handler(event):
    print(f"Worker Start")
    input = event['input']
    
    pdf_data = input.get('pdf_data')
    if pdf_data:
        try:
            print("Processing PDF with Surya OCR...")
            pdf_bytes = base64.b64decode(pdf_data)
            images = pdf_to_images(pdf_bytes)
            print(f"Converted PDF to {len(images)} images")
            ocr_text = run_surya_ocr(images)
            print(f"OCR completed, extracted {len(ocr_text)} characters")
            
            return {
                "success": True,
                "pages": len(images),
                "text_length": len(ocr_text),
                "ocr_text": ocr_text
            }
        except Exception as e:
            print(f"OCR Error: {str(e)}")
            return {"success": False, "error": str(e)}
    else:
        prompt = input.get('prompt')  
        seconds = input.get('seconds', 0)  
        print(f"Received prompt: {prompt}")
        print(f"Sleeping for {seconds} seconds...")
        time.sleep(seconds)  
        return prompt 

if __name__ == '__main__':
    try:
        runpod.serverless.start({'handler': handler })
    except AttributeError:
        print("Testing locally (RunPod serverless not available)")
        with open('test_input.json', 'r') as f:
            test_event = json.load(f)
        result = handler(test_event)
        print(f"Handler result: {result}")
