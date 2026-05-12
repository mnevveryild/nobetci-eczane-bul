import requests
from bs4 import BeautifulSoup
import smtplib
from email.mime.text import MIMEText
import os
from dotenv import load_dotenv

load_dotenv()


def nobetci_eczane_cek(il: str, ilce: str) -> str:
    tr_map = {
        'ş': 's', 'Ş': 'S', 'ı': 'i', 'İ': 'I',
        'ğ': 'g', 'Ğ': 'G', 'ü': 'u', 'Ü': 'U',
        'ö': 'o', 'Ö': 'O', 'ç': 'c', 'Ç': 'C'
    }

    il_clean = il
    ilce_clean = ilce
    for key, value in tr_map.items():
        il_clean = il_clean.replace(key, value)
        ilce_clean = ilce_clean.replace(key, value)

    il_clean = il_clean.lower()
    ilce_clean = ilce_clean.lower()

    url = f"https://www.eczaneler.gen.tr/nobetci-{il_clean}-{ilce_clean}"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    response = requests.get(url, headers=headers, timeout=15)

    if response.status_code != 200:
        return f"{il} {ilce} için nöbetçi eczane bilgisi alınamadı."

    soup = BeautifulSoup(response.text, 'html.parser')
    eczaneler = []

    for row in soup.select("table.table tr"):
        if row.find('th'):
            continue

        name_tag = row.select_one("a")
        if not name_tag:
            continue

        ad = name_tag.text.strip()
        cell_text = row.select_one("td").text

        try:
            address_part = cell_text.replace(ad, '').strip()

            tel_start_index = -1
            for i in range(len(address_part) - 1, 0, -1):
                if address_part[i].isdigit() and not address_part[i-1].isalpha():
                    tel_start_index = i
                    while tel_start_index > 0 and (address_part[tel_start_index-1].isdigit() or address_part[tel_start_index-1] in '() -'):
                        tel_start_index -= 1
                    break

            if tel_start_index != -1:
                adres = address_part[:tel_start_index].strip()
                tel = address_part[tel_start_index:].strip()
            else:
                adres = address_part
                tel = "Telefon bulunamadı"

        except Exception:
            adres = "Adres ayrıştırılamadı"
            tel = "Telefon ayrıştırılamadı"

        eczaneler.append(f"{ad}\nAdres: {adres}\nTel: {tel}")

    if not eczaneler:
        return f"{il} {ilce} için nöbetçi eczane bulunamadı."

    return '\n\n---\n\n'.join(eczaneler)


def mail_gonder(to: str, subject: str, content: str) -> str:
    user = os.getenv("GMAIL_USER")
    password = os.getenv("GMAIL_PASSWORD")

    if not user or not password:
        return "GMAIL_USER veya GMAIL_PASSWORD ortam değişkeni bulunamadı!"

    msg = MIMEText(content, 'plain', 'utf-8')
    msg["Subject"] = subject
    msg["From"] = user
    msg["To"] = to

    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(user, password)
        server.sendmail(user, [to], msg.as_string())

    return "E-posta gönderildi."
