from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from agent import agent
import uvicorn
import logging

app = FastAPI(title="Nöbetçi Eczane API")

# Setup CORS to allow Angular frontend to access the API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify the actual origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class PharmacyRequest(BaseModel):
    il: str
    ilce: str
    email: str

@app.post("/api/find-pharmacies")
def find_pharmacies(request: PharmacyRequest):
    if not request.il or not request.ilce or not request.email:
        raise HTTPException(status_code=400, detail="Eksik bilgi girdiniz.")

    prompt = f"{request.il} ili, {request.ilce} ilçesi için nöbetçi eczaneleri bul. Bulduğun bu eczane bilgilerini {request.email} e-posta adresine düzgün ve okunabilir bir formatta mail olarak gönder."

    try:
        logging.info(f"Agent'a gönderilen istek: {prompt}")
        response = agent.run(prompt)
        
        result_text = ""
        if hasattr(response, 'content'):
            result_text = response.content
        else:
            result_text = str(response)

        return {"status": "success", "message": result_text}
    except Exception as e:
        logging.error(f"Hata oluştu: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
