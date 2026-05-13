# Nobetci Eczane Bul

Il ve ilce bilgisine gore nobetci eczaneleri bulan, sonucu kullanicinin e-posta adresine gonderen web uygulamasi.

Proje iki bolumden olusur:

- **Backend:** FastAPI tabanli API ve nobetci eczane/e-posta araclari
- **Frontend:** Angular ile hazirlanmis kullanici arayuzu

## Ozellikler

- Il ve ilce secerek nobetci eczane arama
- Nobetci eczane bilgilerini `eczaneler.gen.tr` uzerinden cekme
- Sonuclari Gmail SMTP ile e-posta olarak gonderme
- Angular arayuzunden API'ye istek atma
- CORS destegi ile frontend-backend haberlesmesi

## Proje Yapisi

```text
.
|-- app.py                  # Aracsiz FastAPI endpoint'i
|-- main.py                 # Agent destekli FastAPI endpoint'i
|-- agent.py                # Agno/Groq agent tanimi
|-- tools.py                # Nobetci eczane cekme ve mail gonderme araclari
|-- requirements.txt        # Python bagimliliklari
`-- frontend/               # Angular uygulamasi
    |-- package.json
    `-- src/app/
```

## Gereksinimler

- Python 3.10+
- Node.js 18+
- npm
- Gmail hesabi veya uygulama sifresi
- Groq API anahtari (agent destekli `main.py` kullanilacaksa)

## Ortam Degiskenleri

Kok dizinde `.env` dosyasi olusturun:

```env
GMAIL_USER=mail_adresiniz@gmail.com
GMAIL_PASSWORD=gmail_uygulama_sifreniz
GROQ_API_KEY=groq_api_anahtariniz
GROQ_MODEL=llama-3.1-8b-instant
```

Not: Gmail ile SMTP kullanmak icin normal hesap sifresi yerine Gmail uygulama sifresi kullanmaniz gerekebilir.

## Backend Kurulumu

Kok dizinde sanal ortam olusturun ve bagimliliklari yukleyin:

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
pip install fastapi uvicorn pydantic
```

Agent destekli API'yi calistirmak icin:

```bash
python main.py
```

Daha dogrudan, agent kullanmayan API'yi calistirmak icin:

```bash
python app.py
```

Backend varsayilan olarak su adreste calisir:

```text
http://localhost:8000
```

## Frontend Kurulumu

Frontend dizinine gecin ve paketleri yukleyin:

```bash
cd frontend
npm install
npm start
```

Angular uygulamasi varsayilan olarak su adreste acilir:

```text
http://localhost:4200
```

Frontend, API isteklerini su adrese gonderir:

```text
http://localhost:8000/api/find-pharmacies
```

## API Kullanimi

### Nobetci eczane bul ve e-posta gonder

```http
POST /api/find-pharmacies
Content-Type: application/json
```

Ornek istek:

```json
{
  "il": "Istanbul",
  "ilce": "Kadikoy",
  "email": "ornek@mail.com"
}
```

Ornek basarili yanit:

```json
{
  "status": "success",
  "message": "Nobetci eczane bilgileri ornek@mail.com adresine gonderildi."
}
```

## Gelistirme Notlari

- `tools.py` icindeki `nobetci_eczane_cek` fonksiyonu Turkce karakterleri URL uyumlu hale getirir.
- `mail_gonder` fonksiyonu Gmail SMTP uzerinden e-posta yollar.
- `main.py`, Agno agent kullanarak araclari model uzerinden calistirir.
- `app.py`, agent kullanmadan dogrudan arac fonksiyonlarini cagirir.
- Uretim ortaminda CORS ayarlarindaki `allow_origins=["*"]` yerine sadece izin verilen frontend adreslerini kullanmaniz onerilir.

## Test ve Build

Frontend testleri:

```bash
cd frontend
npm test
```

Frontend build:

```bash
cd frontend
npm run build
```

## Lisans

Bu proje icin henuz bir lisans dosyasi eklenmemistir.
