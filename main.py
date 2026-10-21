from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from supabase import create_client
import os
from datetime import datetime

app = FastAPI(title="FC Controle Growth - 9 Abas")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

def extrair_filtros(sck_full: str, dados_extras: dict):
    s = (sck_full + " " + str(dados_extras)).lower()
    
    # PLATAFORMA - 5 + WIX
    plataforma = dados_extras.get("utm_source", "wix")
    if "instagram" in s: plataforma = "instagram"
    elif "tiktok" in s: plataforma = "tiktok"
    elif "kwai" in s: plataforma = "kwai"
    elif "facebook" in s or "fb_" in s: plataforma = "facebook"
    elif "youtube" in s or "yt_" in s: plataforma = "youtube"
    elif "wix" in s: plataforma = "wix"

    # CIDADE - OBRAS LOCAL
    cidade = dados_extras.get("cidade", "irara")
    for c in ["feira", "salvador", "ssa", "alvorada", "irara", "feira-de-santana"]:
        if c in s: 
            cidade = "feira" if "feira" in c else c
            break
    
    # INTERESSE
    interesse = dados_extras.get("interesse", "porcelanato")
    if "pia" in s: interesse = "pia_esculpida"
    elif "nicho" in s: interesse = "nicho_led"
    elif "closet" in s: interesse = "closet"
    elif "bancada" in s: interesse = "bancada"
    elif "porcelanato" in s: interesse = "porcelanato"

    # PAGO X ORGANICO - sua logica
    src = dados_extras.get("utm_medium", "organico")
    eh_pago = "fb_" in s or "google_" in s or "tiktok_" in s or "cpc" in s or "paid" in s or "ads" in s or "pago" in s
    traffic_type = "pago" if eh_pago else "organico"

    return plataforma, cidade, interesse, traffic_type

@app.get("/")
def health():
    return {"status": "ok", "projeto": "fc-controi-growth", "hora": datetime.now().isoformat()}

@app.post("/webhook/kiwify")
async def webhook_kiwify(request: Request):
    try:
        data = await request.json()
        print(f"KIWIFY WEBHOOK CHEGOU: {data}")

        sck = data.get("sck") or data.get("custom_id") or data.get("tracking") or "wix_academia_org"
        sck_v2 = data.get("sck_v2") or sck
        
        # Kiwify manda diferente as vezes
        customer = data.get("Customer") or data.get("customer") or {}
        email = customer.get("email") or data.get("customer_email") or data.get("email") or "sem_email"
        valor = data.get("sale_amount") or data.get("amount") or data.get("Commissions", {}).get("charge_amount") or 99.90
        status = data.get("order_status") or data.get("status") or "paid"

        extras = {
            "cidade": data.get("cidade") or sck_v2,
            "interesse": data.get("interesse") or sck_v2,
            "utm_source": data.get("utm_source") or sck,
            "utm_medium": data.get("utm_medium") or "organico",
            "utm_campaign": data.get("utm_campaign") or "topo"
        }

        plataforma, cidade, interesse, traffic_type = extrair_filtros(sck_v2, extras)

        payload = {
            "sck": sck,
            "sck_completo": sck_v2,
            "cidade": cidade,
            "interesse": interesse,
            "plataforma": plataforma,
            "traffic_type": traffic_type,
            "utm_campaign": extras["utm_campaign"],
            "utm_source": plataforma,
            "utm_medium": traffic_type,
            "email": email,
            "valor": float(str(valor).replace(",",".")) if valor else 99.90,
            "status": status
        }

        supabase.table("vendas_kiwify").insert(payload).execute()
        print(f"SALVO SUPABASE: {payload}")
        
        return {"ok": True, "salvo": payload}

    except Exception as e:
        print(f"ERRO WEBHOOK: {e}")
        return {"ok": False, "erro": str(e)}

@app.post("/webhook/5plataformas")
async def webhook_5plataformas(request: Request):
    data = await request.json()
    plataforma, cidade, interesse, traffic_type = extrair_filtros(data.get("sck",""), data)
    supabase.table("vendas_kiwify").insert({
        "sck": data.get("sck"),
        "sck_completo": f"{data.get('sck')}_{cidade}_{interesse}",
        "cidade": cidade,
        "interesse": interesse,
        "plataforma": plataforma,
        "traffic_type": "organico",
        "utm_campaign": data.get("comentario",""),
        "email": data.get("username"),
        "valor": 0,
        "status": "lead"
    }).execute()
    return {"ok": True}

@app.post("/teste")
async def teste_manual(request: Request):
    data = await request.json()
    supabase.table("vendas_kiwify").insert(data).execute()
    return {"ok": True, "teste": data}
  
