import os
import json
import random
import requests
from datetime import datetime

def log(msg):
    print(f"[{datetime.now()}] {msg}", flush=True)

PAGE_ID = os.getenv("PAGE_ID")
PAGE_TOKEN = os.getenv("PAGE_TOKEN")
ELEVEN_KEY = os.getenv("ELEVENLABS_API_KEY")
ELEVEN_VOICE = os.getenv("ELEVENLABS_VOICE_ID") or "21m00Tcm4TlvDq8ikWAM"

log(f"PAGE_ID: {PAGE_ID}")
log(f"Eleven Key: {'OK' if ELEVEN_KEY else 'VAZIO'}")

def gerar_voz(texto):
    if not ELEVEN_KEY:
        log("Sem ElevenLabs Key")
        return None
    try:
        from elevenlabs.client import ElevenLabs
        client = ElevenLabs(api_key=ELEVEN_KEY)
        log(f"Gerando voz: {texto[:60]}")
        audio = client.text_to_speech.convert(
            voice_id=ELEVEN_VOICE,
            model_id="eleven_multilingual_v2",
            text=texto
        )
        with open("voz.mp3", "wb") as f:
            for chunk in audio:
                f.write(chunk)
        log(f"Voz OK: {os.path.getsize('voz.mp3')} bytes")
        return "voz.mp3"
    except Exception as ex:
        log(f"Erro ElevenLabs: {ex}")
        return None

def postar(video_path, legenda):
    if not PAGE_ID or not PAGE_TOKEN:
        log("PAGE_ID ou TOKEN vazio")
        return False
    try:
        url = f"https://graph.facebook.com/v20.0/{PAGE_ID}/videos"
        log(f"Postando {video_path} na pagina {PAGE_ID}")
        with open(video_path, 'rb') as vf:
            r = requests.post(url, files={'source': vf}, data={'description': legenda, 'access_token': PAGE_TOKEN}, timeout=180)
        log(f"FB {r.status_code}: {r.text[:1000]}")
        return r.status_code == 200
    except Exception as ex:
        log(f"Erro postar: {ex}")
        return False

def main():
    log("=== INICIO FC CONSTRUYE ===")
    pasta = "videos_es_final"
    if not os.path.exists(pasta):
        pasta = "videos"
    if not os.path.exists(pasta):
        os.makedirs(pasta, exist_ok=True)
        log("Sem videos, criando log")
        with open("log_postagens.json", "w") as f:
            json.dump({"total": 0}, f)
        return

    vids = [f for f in os.listdir(pasta) if f.lower().endswith(('.mp4','.mov'))]
    if not vids:
        log(f"Nenhum video em {pasta}")
        return

    escolhido = random.choice(vids)
    vpath = os.path.join(pasta, escolhido)
    legenda = "Francis Construye - Tip del dia! #construccion #albanileria"
    gerar_voz("Sabias este truco de construccion? Mira el video!")
    ok = postar(vpath, legenda)
    log("POSTADO OK" if ok else "FALHA POST")

if __name__ == "__main__":
    main()
