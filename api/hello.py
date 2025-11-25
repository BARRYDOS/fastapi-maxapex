from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import os

app = FastAPI()

# Aquí pon tu dominio real, no uses "*"
frontend_origin = "https://censoedomex.maxapex.net"

app.add_middleware(
    CORSMiddleware,
    allow_origins=[frontend_origin],  # Dominio frontend exacto
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Manejador de preflight OPTIONS universal
@app.options("/api/{full_path:path}")
@app.options("/{full_path:path}")
async def options_handler():
    # NOTA: No agregues manualmente 'Access-Control-Allow-Origin' si usas CORSMiddleware, 
    # pero para Vercel/stream puede ayudar forzar estos headers
    return JSONResponse(
        content={},
        status_code=200,
        headers={
            "Access-Control-Allow-Origin": frontend_origin,
            "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
            "Access-Control-Allow-Headers": "*",
            "Access-Control-Allow-Credentials": "true",
        },
    )

@app.get("/api/generar-docx")
@app.post("/api/generar-docx")
async def generar_docx(request: Request):
    pdf_path = "sample.pdf"  # Tu lógica de generación aquí

    if not os.path.exists(pdf_path):
        return JSONResponse({"error": "Archivo no encontrado"}, status_code=404)
        # CORSMiddleware ya agrega headers necesarios

    def iterfile():
        with open(pdf_path, mode="rb") as f:
            yield from f

    headers = {
        "Content-Disposition": 'attachment; filename="Datos históricos por sitio.pdf"',
        # No agregues Access-Control-* headers aquí; el middleware los añade
    }

    return StreamingResponse(
        iterfile(),
        media_type="application/pdf",
        headers=headers
    )

@app.get("/")
@app.get("/api")
async def root():
    return {"message": "API FastAPI + Vercel + CORS + descarga PDF funcionando al 100% 🚀"}
