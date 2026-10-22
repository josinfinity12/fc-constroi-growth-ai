# scripts/webhook_kiwify.py - NÃO ALTERA dashboard.py
# REGRA ETERNA: NUNCA DELETAR NADA - SÓ ADICIONAR/CORRIGIR
# v3.4.0 - KEYWORDS EXPANDIDAS: pia de banheiro, closet, bancada, fachadas, nichos, revestimentos, armarios, gavetas

from flask import Flask, request, jsonify
from supabase import create_client
import os
from datetime import datetime

app = Flask(__name__)

# Usa suas chaves que já estão no .streamlit/secrets.toml
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_SECRET = os.getenv("SUPABASE_SECRET")

if not SUPABASE_URL or not SUPABASE_SECRET:
    try:
        import streamlit as st
        if not SUPABASE_URL:
            SUPABASE_URL = st.secrets.get("SUPABASE_URL", "")
        if not SUPABASE_SECRET:
            SUPABASE_SECRET = st.secrets.get("SUPABASE_KEY", "") or st.secrets.get("SUPABASE_SECRET", "")
    except:
        pass

# --- v3.4.0 - KEYWORDS EXPANDIDAS - SÓ ADIÇÃO ---
def extrair_filtros_sck(sck_full: str):
    s = str(sck_full).lower()
    # 5 plataformas
    plat = "wix"
    if "instagram" in s: plat = "instagram"
    elif "tiktok" in s: plat = "tiktok"
    elif "kwai" in s: plat = "kwai"
    elif "facebook" in s or "fb_" in s: plat = "facebook"
    elif "youtube" in s or "yt_" in s: plat = "youtube"
    
    # 6 CIDADES ORIGINAIS CORRIGIDAS
    cid = "irara"
    if "feira" in s: cid = "feira"
    elif "santanopolis" in s or "santanópolis" in s: cid = "santanopolis"
    elif "santa_barbara" in s or "santa barbara" in s: cid = "santa_barbara"
    elif "serrinha" in s: cid = "serrinha"
    elif "ouricangas" in s or "ouriçangas" in s: cid = "ouricangas"
    
    # INTERESSES - CORRIGIDO + EXPANDIDO
    inter = "porcelanato"
    # CORREÇÃO: pia esculpida -> pia de banheiro
    if "pia de banheiro" in s or "pia_banheiro" in s or "pia esculpida" in s or "pia_esculpida" in s or "pia_90" in s or "_pia_" in s:
        inter = "pia_de_banheiro"  # CORRIGIDO
    # NOVOS - TUDO EM PORCELANATO
    elif "closet" in s:
        inter = "closet_porcelanato"
    elif "bancada" in s and "cozinha" in s:
        inter = "bancada_cozinha_porcelanato"
    elif "bancada" in s:
        inter = "bancada_porcelanato"
    elif "fachada" in s:
        inter = "fachadas_porcelanato"
    elif "nicho" in s:
        inter = "nichos_porcelanato"
    elif "revestimento" in s:
        inter = "revestimentos_porcelanato"
    elif "armario" in s or "armário" in s:
        inter = "armarios_porcelanato"
    elif "gaveta" in s:
        inter = "gavetas_porcelanato"
    elif "base" in s and "300kg" in s:
        inter = "base_300kg"  # mantido seu original
    elif "base" in s:
        inter = "base_armario_porcelanato"
        
    pago = "fb_" in s or "google_" in s or "cpc" in s or "pago" in s
    traffic = "pago" if pago else "organico"
    return plat, cid, inter, traffic

try:
    supa = create_client(SUPABASE_URL, SUPABASE_SECRET)
except:
    supa = None

@app.route("/webhook/kiwify", methods=["POST"])
def receber_kiwify():
    try:
        dados = request.get_json(force=True)
        print(f"Venda recebida: {dados}")

        sck_original = dados.get("sck") or dados.get("Tracking_parameters", {}).get("sck") or dados.get("src") or ""
        plat, cid, inter, traffic = extrair_filtros_sck(sck_original)
        
        venda = {
            "sck": sck_original,
            "sck_completo": sck_original,
            "cidade": cid,
            "interesse": inter,  # AGORA COM: pia_de_banheiro, closet_porcelanato, bancada_cozinha, fachadas, nichos, revestimentos, armarios, gavetas
            "plataforma": plat,
            "traffic_type": traffic,
            "valor": float(str(dados.get("Commissions", {}).get("charge_amount") or dados.get("amount") or dados.get("price") or 0).replace(",",".")),
            "utm_campaign": dados.get("utm_campaign") or dados.get("Tracking_parameters", {}).get("utm_campaign") or "",
            "utm_medium": dados.get("utm_medium") or dados.get("Tracking_parameters", {}).get("utm_medium") or "",
            "status": dados.get("order_status") or dados.get("status") or "aprovado",
            "created_at": datetime.now().isoformat(),
            "raw": dados
        }

        if supa:
            supa.table("vendas_kiwify").insert(venda).execute()
        else:
            if SUPABASE_URL and SUPABASE_SECRET:
                supa_temp = create_client(SUPABASE_URL, SUPABASE_SECRET)
                supa_temp.table("vendas_kiwify").insert(venda).execute()
                
        return jsonify({"ok": True, "salvo": venda}), 200
    except Exception as e:
        print(f"Erro: {e}")
        return jsonify({"erro": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
    
    
    
