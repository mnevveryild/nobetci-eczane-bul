from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from tools import nobetci_eczane_cek, mail_gonder

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


class PharmacyRequest(BaseModel):
    il: str
    ilce: str
    email: str


@app.post("/api/find-pharmacies")
async def find_pharmacies(request: PharmacyRequest):
    if not request.il or not request.ilce or not request.email:
        raise HTTPException(status_code=400, detail="İl, ilçe ve e-posta alanları zorunludur.")

    eczane_bilgisi = nobetci_eczane_cek(request.il, request.ilce)

    konu = f"{request.il} - {request.ilce} Nöbetçi Eczaneleri"
    icerik = f"{request.il} / {request.ilce} için nöbetçi eczaneler:\n\n{eczane_bilgisi}"

    sonuc = mail_gonder(request.email, konu, icerik)

    if "bulunamadı" in eczane_bilgisi.lower():
        return {"status": "warning", "message": eczane_bilgisi}

    return {
        "status": "success",
        "message": f"Nöbetçi eczane bilgileri {request.email} adresine gönderildi."
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
