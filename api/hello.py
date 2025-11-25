# api/index.py ← nombre EXACTO del archivo
from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import os

app = FastAPI()

# CORS correcto y amplio (luego lo puedes restringir)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Cambia a tu dominio real en producción
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# === MANEJO CORRECTO DE PREFlight para TODAS las rutas ===
@app.options("/api/{full_path:path}")
@app.options("/{full_path:path}")
async def options_handler():
    return JSONResponse(
        content={},
        status_code=200,
        headers={
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
            "Access-Control-Allow-Headers": "*",
            "Access-Control-Allow-Credentials": "true",
        },
    )

# === ENDPOINT QUE SÍ FUNCIONA CON ARCHIVOS BINARIOS EN VERCEL ===
@app.get("/api/generar-docx")
@app.post("/api/generar-docx")
async def generar_docx(request: Request):
    pdf_path = "sample.pdf"  # ← aquí tu lógica real de generación

    if not os.path.exists(pdf_path):
        response = JSONResponse({"error": "Archivo no encontrado"}, status_code=404)
        response.headers["Access-Control-Allow-Origin"] = "*"
        response.headers["Access-Control-Allow-Credentials"] = "true"
        return response

    # ABRIR EL ARCHIVO Y ENVIARLO COMO STREAM (esto SÍ conserva CORS en Vercel)
    def iterfile():
        with open(pdf_path, mode="rb") as f:
            yield from f

    headers = {
        "Access-Control-Allow-Origin": "*",           # ← Crucial
        "Access-Control-Allow-Credentials": "true",   # ← Crucial
        "Access-Control-Expose-Headers": "*",         # ← Ayuda con algunos navegadores
        "Content-Disposition": 'attachment; filename="Datos históricos por sitio.pdf"',
    }

    return StreamingResponse(
        iterfile(),
        media_type="application/pdf",
        headers=headers
    )

# Ruta de prueba
@app.get("/")
@app.get("/api")
async def root():
    return {"message": "API FastAPI + Vercel + CORS + descarga PDF funcionando al 100% 🚀"}
