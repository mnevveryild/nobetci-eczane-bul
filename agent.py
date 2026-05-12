from agno.agent import Agent
from agno.models.groq import Groq
from dotenv import load_dotenv
import os
from tools import nobetci_eczane_cek, mail_gonder

load_dotenv()

default_model = Groq(id=os.getenv("GROQ_MODEL", "llama-3.1-8b-instant"))

tools = [nobetci_eczane_cek, mail_gonder]

agent = Agent(
    name="NobetciEczaneAgent",
    description="Belirtilen il ve ilçedeki nöbetçi eczaneleri çekip e-posta gönderen asistan.",
    instructions=[
        "Kullanıcının belirttiği il ve ilçe için 'nobetci_eczane_cek' aracını kullanarak nöbetçi eczaneleri bul.",
        "Eczane verilerini başarılı bir şekilde aldıktan sonra, bu bilgileri okunabilir ve düzgün bir formatta düzenle.",
        "Düzenlenmiş eczane bilgilerini 'mail_gonder' aracını kullanarak kullanıcının belirttiği e-posta adresine gönder. E-postanın konusu anlaşılır olsun (Örn: '[İl] - [İlçe] Nöbetçi Eczaneleri').",
        "İşlemler tamamlandıktan sonra kullanıcıya hangi e-posta adresine kaç tane eczane bilgisi gönderdiğini özetle."
    ],
    tools=tools,
    model=default_model,
    markdown=True
)
