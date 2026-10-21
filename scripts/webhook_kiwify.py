# scripts/webhook_kiwify.py - NÃO ALTERA dashboard.py - v3.3.2 APENAS ADICIONA - COMPLETO PARA COLAR
from flask import Flask, request, jsonify
from supabase import create_client
import os
from datetime import datetime

app = Flask(__name__)

# Usa suas chaves que já estão no .streamlit/secrets.toml
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_SECRET = os.getenv("SUPABASE_SECRET") or os.getenv("SUPABASE_KEY")

supa = create_client(SUPABASE_URL, SUPABASE_SECRET) if SUPABASE_URL and SUPABASE_SECRET else None

# ============================================================
# >>> ADIÇÃO v3.3.2 - APENAS SOMA - NÃO APAGA NADA ACIMA
# ============================================================
def extrair_filtros_sck_completo(sck_full: str, cidade_param="", interesse_param="", utm_source_param=""):
    """v3.3.2 - 6 CIDADES OFICIAIS + 5 PLATAFORMAS + PAGO/ORGANICO"""
    s = str(sck_full).lower() if sck_full else ""
    plat = str(utm_source_param).lower() if utm_source_param else "wix"
    if plat in ["", "wix", "null", "none", "undefined"]:
        if "instagram" in s: plat = "instagram"
        elif "tiktok" in s: plat = "tiktok"
        elif "kwai" in s: plat = "kwai"
        elif "facebook" in s or "fb_" in s or "_fb" in s or "face" in s: plat = "facebook"
        elif "youtube" in s or "yt_" in s: plat = "youtube"
        else: plat = "wix"
    cid_raw = (s + " " + str(cidade_param)).lower()
    cid = "irara"
    if "feira" in cid_raw: cid = "feira de santana"
    elif "santanopolis" in cid_raw or "santanópolis" in cid_raw: cid = "santanopolis"
    elif "santa barbara" in cid_raw or "santabarbara" in cid_raw or "barbara" in cid_raw: cid = "santa barbara"
    elif "serrinha" in cid_raw: cid = "serrinha"
    elif "ouricangas" in cid_raw: cid = "ouricangas"
    elif "irara" in cid_raw or "irar" in cid_raw: cid = "irara"
    elif "salvador" in cid_raw or "ssa" in cid_raw: cid = "salvador"
    elif "agua fria" in cid_raw or "aguafria" in cid_raw: cid = "agua fria"
    elif "pedrao" in cid_raw or "pedrão" in cid_raw: cid = "pedrao"
    inter_raw = (s + " " + str(interesse_param)).lower()
    inter = "porcelanato"
    if "pia" in inter_raw: inter = "pia_esculpida"
    elif "nicho" in inter_raw: inter = "nicho_led"
    elif "closet" in inter_raw: inter = "closet"
    elif "gaveta" in inter_raw: inter = "gaveta"
    elif "bancada" in inter_raw: inter = "bancada"
    elif "base" in inter_raw: inter = "base_300kg"
    pago = "fb_" in s or "google_" in s or "cpc" in s or "pago" in s or "_pago" in s or "paid" in s or "ads" in s
    traffic = "pago" if pago else "organico"
    return plat, cid, inter, traffic

@app.route("/")
def home_check():
    return "FC WEBHOOK KIWIFY v3.3.2 ONLINE - 6 CIDADES + 5 PLAT + sck_v2", 200

@app.route("/webhook/kiwify", methods=["POST", "GET"])
def receber_kiwify():
    try:
        if request.method == "GET":
            dados = request.args.to_dict()
        else:
            try:
                dados = request.get_json(force=True)
                if not dados:
                    dados = request.form.to_dict()
                    if not dados:
                        dados = request.args.to_dict()
            except:
                dados = request.form.to_dict() or request.args.to_dict()
        
        print(f"Venda recebida: {dados}")

        # SEU CODIGO ORIGINAL MANTIDO
        sck_original = ""
        try:
            tp = dados.get("Tracking_parameters")
            if isinstance(tp, dict):
                sck_original = tp.get("sck") or ""
            sck_original = sck_original or dados.get("sck") or dados.get("src") or ""
        except:
            sck_original = dados.get("sck") or ""
        
        valor_original = 0
        try:
            comm = dados.get("Commissions")
            if isinstance(comm, dict):
                valor_original = comm.get("charge_amount") or 0
            valor_original = valor_original or dados.get("amount") or dados.get("price") or 0
            valor_original = float(str(valor_original).replace(",","."))
        except:
            valor_original = 99.90
        
        utm_campaign_original = ""
        utm_medium_original = ""
        try:
            tp = dados.get("Tracking_parameters")
            if isinstance(tp, dict):
                utm_campaign_original = tp.get("utm_campaign") or ""
                utm_medium_original = tp.get("utm_medium") or ""
            utm_campaign_original = utm_campaign_original or dados.get("utm_campaign") or ""
            utm_medium_original = utm_medium_original or dados.get("utm_medium") or ""
        except:
            utm_campaign_original = dados.get("utm_campaign") or ""
            utm_medium_original = dados.get("utm_medium") or ""
        
        status_original = dados.get("order_status") or dados.get("status") or "aprovado"

        # ADICAO v3.3.2 - COLUNAS NOVAS WIX
        sck = dados.get("sck") or dados.get("SCK") or dados.get("sck_completo") or dados.get("custom_id") or sck_original or ""
        sck_v2 = dados.get("sck_v2") or dados.get("SCK_V2") or ""
        cidade_param = dados.get("cidade") or dados.get("city") or ""
        interesse_param = dados.get("interesse") or dados.get("interest") or ""
        utm_source_param = dados.get("utm_source") or dados.get("src") or ""
        utm_content_param = dados.get("utm_content") or ""
        
        if isinstance(dados.get("Tracking_parameters"), dict):
            tp = dados.get("Tracking_parameters")
            sck = sck or tp.get("sck") or ""
            sck_v2 = sck_v2 or tp.get("sck_v2") or ""
            cidade_param = cidade_param or tp.get("cidade") or ""
            interesse_param = interesse_param or tp.get("interesse") or ""
            utm_source_param = utm_source_param or tp.get("utm_source") or ""
        
        plat_auto, cid_auto, inter_auto, traffic_auto = extrair_filtros_sck_completo(sck or sck_v2, cidade_param, interesse_param, utm_source_param)
        
        venda = {
            "sck": sck or sck_original or "wix_academia_org",
            "valor": valor_original,
            "utm_campaign": utm_campaign_original or dados.get("utm_campaign") or "",
            "utm_medium": utm_medium_original or dados.get("utm_medium") or "",
            "status": status_original,
            "created_at": datetime.now().isoformat(),
            "raw": dados,
            "sck_completo": sck or sck_original,
            "sck_v2": sck_v2 or (sck + "_" + (cidade_param or cid_auto) + "_" + (interesse_param or inter_auto) + "_" + (utm_campaign_original or "topo")),
            "cidade": (cidade_param or cid_auto).lower(),
            "interesse": (interesse_param or inter_auto).lower(),
            "plataforma": (utm_source_param or plat_auto).lower(),
            "traffic_type": traffic_auto,
            "utm_source": (utm_source_param or plat_auto).lower(),
            "utm_content": utm_content_param or inter_auto,
            "email": dados.get("email") or dados.get("customer_email") or "sem_email",
            "raw_payload": str(dados)[:3000]
        }
        
        if isinstance(dados.get("Customer"), dict):
            venda["email"] = dados["Customer"].get("email") or venda["email"]

        print(f"Payload final v3.3.2: {venda}")

        if supa:
            supa.table("vendas_kiwify").insert(venda).execute()
            return jsonify({"ok": True, "salvo": venda, "versao": "v3.3.2"}), 200
        else:
            return jsonify({"ok": False, "error": "Supabase nao configurado", "payload": venda}), 500
    except Exception as e:
        print(f"Erro: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({"erro": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)), debug=True)
    
    
