from fastapi import FastAPI, HTTPException, Depends, Request
from slowapi import Limiter
from slowapi.util import get_remote_address
import logging

from app.models import SOAPRequest
from app.services import call_groq_api
from app.utils import extract_json_from_llm_response
from app.authentication import verify_api_key

# Inisialisasi FastAPI
app = FastAPI(
    title="Medical SOAP to Resume Converter API",
    description="API for generating structured medical resumes from SOAP notes"
)

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Setup rate limiter
limiter = Limiter(key_func=get_remote_address)

@app.get("/")
async def root():
    return {"message": "Medical SOAP to Resume Converter API"}

@app.post("/generate-resume", dependencies=[Depends(verify_api_key)])
@limiter.limit("10/minute")  # Batasi maksimal 10 request per menit per IP
async def generate_resume(request: Request, request_body: SOAPRequest):
    """Generate medical resume from SOAP text using Groq API."""
    
    prompt = f"""
    Anda adalah asisten medis yang menyusun resume medis dari catatan SOAP pasien.
    Hasilkan output dalam format JSON **tanpa teks tambahan** sesuai spesifikasi berikut:

    {{
      "RESUME MEDIS": {{
        "Keluhan Utama": "[...]",
        "Alasan Pasien Dirawat": "[...]",
        "Riwayat Penyakit": "[...]",
        "Pemeriksaan Fisik": "[...]",
        "Pemeriksaan Penunjang": "[...]",
        "Diagnosis Primer": "[...]",
        "Diagnosis Sekunder": "[...]",
        "RProsedur Terapi dan Tindakan Yang Dilakukan": "[...]",
        "Obat Yang Diberikan Saat Dirawat": "[...]",
        "Obat Yang Diberikan Setelah Pasien Keluar": "[...]",
        "Kondisi Pasien": "[...]",
        "Instruksi / Tindak Lanjut": "[...]",
        ...
      }}
    }}

    Catatan SOAP:
    {request_body.soap_text}
    """

    try:
        logger.info("Processing SOAP request...")
        chat_completion = await call_groq_api(prompt)
        resume_text = chat_completion.choices[0].message.content.strip()

        try:
            resume_json = extract_json_from_llm_response(resume_text)
            logger.info("Resume generated successfully")
            return resume_json
        except ValueError as e:
            logger.error(f"JSON Parsing Error: {str(e)}")
            raise HTTPException(status_code=422, detail=str(e))
    
    except Exception as e:
        logger.critical(f"Critical error: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal Server Error")