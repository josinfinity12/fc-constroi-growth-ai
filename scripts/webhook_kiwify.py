# scripts/webhook_kiwify.py - NÃO ALTERA dashboard.py
from flask import Flask, request, jsonify
from supabase import create_client
import os
from datetime import datetime

app = Flask(__name__)

# Usa suas chaves que já estão no .streamlit/secrets.toml
# Pegando da env ou direto
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_SECRET = os.getenv("SUPABASE_SECRET")

supa = create_client(SUPABASE_URL, SUPABASE_SECRET)

@app.route("/webhook/kiwify", methods=["POST"])
def receber_kiwify():
    try:
        dados = request.get_json(force=True)
        print(f"Venda recebida: {dados}")

        # Kiwify manda esses campos - pegamos tudo que vier
        venda = {
            "sck": dados.get("sck") or dados.get("Tracking_parameters", {}).get("sck") or dados.get("src") or "",
            "valor": float(str(dados.get("Commissions", {}).get("charge_amount") or dados.get("amount") or dados.get("price") or 0).replace(",",".")),
            "utm_campaign": dados.get("utm_campaign") or dados.get("Tracking_parameters", {}).get("utm_campaign") or "",
            "utm_medium": dados.get("utm_medium") or dados.get("Tracking_parameters", {}).get("utm_medium") or "",
            "status": dados.get("order_status") or dados.get("status") or "aprovado",
            "created_at": datetime.now().isoformat(),
            "raw": dados  # salva tudo
        }

        supa.table("vendas_kiwify").insert(venda).execute()
        return jsonify({"ok": True, "salvo": venda}), 200
    except Exception as e:
        print(f"Erro: {e}")
        return jsonify({"erro": str(e)}), 500

if __name__ == "__main__":
    # Roda em http://localhost:5000/webhook/kiwify
    app.run(host="0.0.0.0", port=5000, debug=True)
    
    
