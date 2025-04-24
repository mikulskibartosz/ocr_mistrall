import tempfile
import os
import shutil
from baml_client import b
from baml_client.types import Contract
from fastapi import FastAPI, File, UploadFile, HTTPException
from ocr.ocr import MistralOCR
from ocr.config import load_config

app = FastAPI(title="OCR Contracts API")

config = load_config()
ocr = MistralOCR(api_key=config.mistral_api_key)


@app.post("/ocr/", response_model=Contract)
async def ocr_pdf(file: UploadFile = File(...)):
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are supported")

    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:
        shutil.copyfileobj(file.file, temp_file)
        temp_path = temp_file.name

    try:
        extracted_pages = ocr.ocr(temp_path)
        extracted_text = "\n".join(extracted_pages)

        contract_data = b.ExtractContract(extracted_text)

        return contract_data

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing PDF: {str(e)}")

    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)


@app.get("/health")
async def health_check():
    return {"status": "healthy"}
