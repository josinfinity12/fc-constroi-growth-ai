# auto_post_perpetuo.py v5.3 - VOZ ELEVENLABS + POST AUTO PAGINA 61595702674802
import os, subprocess, json, random, datetime, requests
from pathlib import Path
import time

OUTPUT_DIR = "/tmp/fc_perpetuo"
os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs("videos_es_final", exist_ok=True)

PAGE_ID = os.getenv("PAGE_ID", "61595702674802")
PAGE_TOKEN = os.getenv("PAGE_TOKEN", "")
ELEVENLABS_KEY = os.getenv("ELEVENLABS_API_KEY", "")
ELEVENLABS_VOICE = os.getenv("ELEVENLABS_VOICE_ID", "21m00Tcm4TlvDq8ikWAM") # Adam espanhol, troque pela sua voz clonada
LOG_FILE = "log_postagens.json"

def log(msg):
    print(f"[{datetime.datetime.now().strftime('%H:%M:%S')}] {msg}", flush=True)

def gerar_audio_elevenlabs(texto_es, reel_id):
    """GERA VOZ COM ELEVENLABS TRADUZIDA"""
    audio_path = f"{OUTPUT_DIR}/{reel_id}_es.mp3"
    
    if not ELEVENLABS_KEY:
        log("⚠️ ELEVENLABS_API_KEY vazio, usando gTTS fallback")
        try:
            from gtts import gTTS
            gTTS(text=texto_es, lang='es').save(audio_path)
            return audio_path
        except as e:
            log(f"gTTS erro: {e}")
            return None

    # ElevenLabs API v2
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{ELEVENLABS_VOICE}"
    headers = {
        "Accept": "audio/mpeg",
        "Content-Type": "application/json",
        "xi-api-key": ELEVENLABS_KEY
    }
    data = {
        "text": texto_es,
        "model_id": "eleven_multilingual_v2", # modelo que fala espanhol perfeito
        "voice_settings": {
            "stability": 0.5,
            "similarity_boost": 0.75,
            "style": 0.4,
            "use_speaker_boost": True
        }
    }
    
    try:
        log(f"🎤 Gerando voz ElevenLabs: {texto_es[:50]}...")
        r = requests.post(url, json=data, headers=headers, timeout=30)
        if r.status_code == 200:
            with open(audio_path, 'wb') as f:
                f.write(r.content)
            log(f"✅ Audio ElevenLabs gerado: {audio_path} ({len(r.content)} bytes)")
            return audio_path
        else:
            log(f"❌ ElevenLabs erro {r.status_code}: {r.text[:500]} - usando gTTS")
            from gtts import gTTS
            gTTS(text=texto_es, lang='es').save(audio_path)
            return audio_path
    except Exception as e:
        log(f"Exception ElevenLabs: {e} - fallback gTTS")
        try:
            from gtts import gTTS
            gTTS(text=texto_es, lang='es').save(audio_path)
            return audio_path
        except:
            return None

def puxar_3_reels_reais():
    reels = []
    try:
        cmd = ["yt-dlp", "--flat-playlist", "--dump-json", "--playlist-end", "3", "https://www.instagram.com/fc_constroi/reels/"]
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=40)
        if r.stdout:
            for line in r.stdout.strip().split("\n")[:3]:
                try:
                    d = json.loads(line)
                    reels.append({"id": d.get("id", f"reel_{random.randint(1,999)}"), "title": d.get("title","Gaveta R$8mil")[:80]})
                except: continue
    except Exception as e:
        log(f"yt-dlp: {e}")
    if len(reels) < 3:
        reels = [{"id":"gaveta_8000","title":"ERRO de R$8mil gaveta"},{"id":"nivel_parede","title":"Parede nivelada"},{"id":"rejunte_10anos","title":"Rejunte 10 anos"}]
    return reels[:3]

def gerar_es(titulo_pt):
    if "gaveta" in titulo_pt.lower(): return "¿GAVETA PORCELANATO SE ROMPIÓ? Evita pérdida de ocho mil dólares con este truco profesional que los maestros no quieren que sepas."
    if "nivel" in titulo_pt.lower() or "parede" in titulo_pt.lower(): return "¿PARED DESNIVELADA? Te muestro como dejarla cien por ciento nivelada sin usar burbuja. Truco de obra."
    return "¿JUNTA MANCHADA? Te revelo la junta que no se mancha por diez años. Secreto de Fc Construye."

def montar_final_9x16(reel_id, titulo_es):
    final_path = f"videos_es_final/{reel_id}_FINAL_ES_9x16.mp4"
    try:
        from moviepy.editor import ColorClip, TextClip, CompositeVideoClip, AudioFileClip
        
        audio_path = gerar_audio_elevenlabs(titulo_es, reel_id)
        
        clip = ColorClip(size=(1080,1920), color=(15,15,15), duration=10)
        txt = TextClip(titulo_es, fontsize=55, color='white', bg_color='black', size=(900,500), method='caption').set_duration(10).set_position('center')
        final = CompositeVideoClip([clip, txt])
        
        if audio_path and os.path.exists(audio_path):
            audio = AudioFileClip(audio_path)
            # Ajusta video pra duracao do audio
            final = final.set_duration(max(8, audio.duration + 1))
            txt = txt.set_duration(final.duration)
            final = CompositeVideoClip([clip, txt]).set_audio(audio)
        
        final.write_videofile(final_path, fps=24, codec="libx264", audio_codec="aac", logger=None)
        final.close()
        log(f"✅ Video final com voz ElevenLabs: {final_path}")
    except Exception as e:
        log(f"Erro montar: {e}")
        Path(final_path).touch()
    return final_path

def postar_na_pagina_61595702674802(video_path, legenda):
    if not PAGE_TOKEN:
        log("❌ PAGE_TOKEN vazio")
        return False
    size = os.path.getsize(video_path) if os.path.exists(video_path) else 0
    log(f"Postando {video_path} ({size} bytes) na pagina {PAGE_ID}")

    if size < 10000:
        url = f"https://graph.facebook.com/v20.0/{PAGE_ID}/feed"
        r = requests.post(url, data={"message": legenda, "access_token": PAGE_TOKEN}, timeout=30)
        log(f"FB FEED {r.status_code}: {r.text[:300]}")
        return r.status_code == 200

    url = f"https://graph.facebook.com/v20.0/{PAGE_ID}/videos"
    try:
        with open(video_path, 'rb') as f:
            r = requests.post(url, files={'source': f}, data={'description': legenda, 'access_token': PAGE_TOKEN}, timeout=180)
            log(f"FB VIDEO {r.status_code}: {r.text[:500]}")
            return r.status_code == 200
    except Exception as e:
        log(f"Erro postar: {e}")
        return False

def main():
    log(f"🚀 INICIANDO v5.3 ELEVENLABS {datetime.datetime.now()}")
    log(f"ElevenLabs Key: {'OK '+ELEVENLABS_KEY[:10]+'...' if ELEVENLABS_KEY else 'VAZIO'}")
    log(f"Voice ID: {ELEVENLABS_VOICE}")

    for reel in puxar_3_reels_reais():
        titulo_es = gerar_es(reel['title'])
        legenda = f"{titulo_es}\n\nComenta YO QUIERO\n\n#construccion #fc_construye"
        video_path = montar_final_9x16(reel['id'], titulo_es)
        log(f"Legenda: {legenda}")
        ok = postar_na_pagina_61595702674802(video_path, legenda)
        log(f"{'✅ POSTADO' if ok else '❌ FALHA'} NA FC CONSTRUYE - Voz ElevenLabs")
        time.sleep(5)

    log("🎉 FIM CICLO v5.3 ELEVENLABS")

if __name__ == "__main__":
    main()
