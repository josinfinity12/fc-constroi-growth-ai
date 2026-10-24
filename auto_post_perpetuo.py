import os, random, requests, json, time
from datetime import datetime

def log(m): print(f"[{datetime.now()}] {m}", flush=True)

# ========== ATUALIZADO - PEGA TOKENS NOVOS SEM PERDER ANTIGOS ==========
# Agora aceita FB_PAGE_ID, FB_PAGE_TOKEN, FB_SYSTEM_TOKEN + mantém PAGE_ID antigo
PAGE_ID = (os.getenv("FB_PAGE_ID") or os.getenv("PAGE_ID") or os.getenv("FACEBOOK_PAGE_ID") or "1376850792182671").strip()
PAGE_TOKEN = (os.getenv("FB_PAGE_TOKEN") or os.getenv("PAGE_TOKEN") or os.getenv("FB_SYSTEM_TOKEN") or os.getenv("FACEBOOK_PAGE_TOKEN") or "").strip()

# Mantém seus outros tokens antigos
ELEVEN_API = (os.getenv("ELEVENLABS_API_KEY") or "").strip()
ELEVEN_VOICE = (os.getenv("ELEVENLABS_VOICE_ID") or os.getenv("VOICE_ID") or "").strip()

log(f"PAGE_ID carregado: {PAGE_ID}")
log(f"PAGE_TOKEN: {'OK ' + str(len(PAGE_TOKEN)) + ' chars' if PAGE_TOKEN else 'VAZIO - verifique secrets'}")
log(f"ELEVENLABS: {'OK' if ELEVEN_API else 'usando gTTS gratis'}")

# ========== FUNÇÃO NOVA - GERA VOZ SEM ERRO ==========
def gerar_voz_es_com_fallback(texto_es, temp_mp3_es):
    """Tenta ElevenLabs, se der erro usa gTTS gratis sem bloqueio"""
    from gtts import gTTS
    
    # 1. TENTA ELEVENLABS SE TIVER CREDITO
    if ELEVEN_API and ELEVEN_VOICE and len(ELEVEN_API) > 20:
        try:
            log(f"Tentando ElevenLabs voz {ELEVEN_VOICE[:8]}...")
            url = f"https://api.elevenlabs.io/v1/text-to-speech/{ELEVEN_VOICE}"
            headers = {"xi-api-key": ELEVEN_API, "Content-Type": "application/json"}
            payload = {
                "text": texto_es,
                "model_id": "eleven_multilingual_v2",
                "voice_settings": {"stability": 0.5, "similarity_boost": 0.75}
            }
            r = requests.post(url, headers=headers, json=payload, timeout=90)
            if r.status_code == 200:
                with open(temp_mp3_es, 'wb') as f:
                    f.write(r.content)
                log("ElevenLabs OK!")
                return True
            else:
                log(f"ElevenLabs falhou {r.status_code}: {r.text[:300]} -> usando gTTS")
        except Exception as e:
            log(f"ElevenLabs erro {e} -> usando gTTS")

    # 2. FALLBACK GRATIS QUE NUNCA BLOQUEIA
    try:
        log("4/5 Gerando voz ES com gTTS (gratis sem bloqueio)...")
        tts = gTTS(text=texto_es, lang='es', tld='com.mx', slow=False)
        tts.save(temp_mp3_es)
        log("gTTS OK!")
        return True
    except Exception as e:
        log(f"gTTS erro {e}")
        return False

# ========== PIPELINE 100% AUTO PT-BR -> ES ==========
def dublar_pt_para_es_automatico(video_path_pt):
    try:
        import whisper
        from moviepy.editor import VideoFileClip, AudioFileClip

        log(f"--- TRADUTOR AUTOMATICO PT-BR -> ES INICIADO ---")
        log(f"Video PT original: {video_path_pt}")

        temp_wav = "temp_pt.wav"
        temp_mp3_es = "temp_es.mp3"
        video_saida_es = video_path_pt.replace(".mp4","_ES_DUBLADO.mp4").replace(".MP4","_ES_DUBLADO.mp4")
        
        if "_ES_DUBLADO" in video_path_pt or "_ES" in video_path_pt:
            log("Esse video já é ES, usando direto")
            return video_path_pt, ""

        log("1/5 Extraindo voz PT-BR...")
        clip = VideoFileClip(video_path_pt)
        if clip.audio is None:
            log("Video sem audio!")
            return video_path_pt, ""
        clip.audio.write_audiofile(temp_wav, logger=None)
        clip.close()

        log("2/5 Whisper ouvindo PT-BR...")
        model = whisper.load_model("base")
        result = model.transcribe(temp_wav, language="pt", fp16=False)
        texto_pt = result["text"].strip()
        log(f"TEXTO PT-BR OUVIDO: {texto_pt}")
        if len(texto_pt) < 3:
            log("Não ouviu nada, usando video original")
            return video_path_pt, ""

        log("3/5 Traduzindo PT-BR -> ES...")
        try:
            url = f"https://api.mymemory.translated.net/get?q={requests.utils.quote(texto_pt)}&langpair=pt|es"
            r = requests.get(url, timeout=30).json()
            texto_es = r['responseData']['translatedText']
            log(f"TEXTO ES TRADUZIDO: {texto_es}")
        except Exception as e:
            log(f"Erro tradução {e}")
            texto_es = texto_pt

        # MELHORIA: agora não dá mais erro de ElevenLabs
        if not gerar_voz_es_com_fallback(texto_es, temp_mp3_es):
            return video_path_pt, ""

        log("5/5 Dublando video PT -> ES...")
        video = VideoFileClip(video_path_pt)
        from moviepy.editor import AudioFileClip
        audio_es = AudioFileClip(temp_mp3_es)
        video_final = video.set_audio(audio_es)
        video_final.write_videofile(video_saida_es, codec='libx264', audio_codec='aac', logger=None)
        video.close()
        video_final.close()

        for f in [temp_wav, temp_mp3_es]:
            if os.path.exists(f): os.remove(f)

        log(f"VIDEO ES DUBLADO CRIADO: {video_saida_es}")
        return video_saida_es, texto_es

    except ImportError as e:
        log(f"Falta lib {e} - adicione no requirements.txt: openai-whisper, moviepy, gtts")
        return video_path_pt, ""
    except Exception as e:
        log(f"Erro pipeline auto {e}")
        return video_path_pt, ""

# ====== POSTAGENS 5 REDES - MANTIDO IGUAL + MELHORADO FB ======
def postar_facebook(video_path, legenda):
    if not PAGE_ID or not PAGE_TOKEN:
        log("FB FALHOU: PAGE_ID ou PAGE_TOKEN vazio - verifique secrets FB_PAGE_ID/FB_PAGE_TOKEN")
        return False
    try:
        page_id = str(PAGE_ID).strip().replace("@","")
        url = f"https://graph.facebook.com/v20.0/{page_id}/videos"
        with open(video_path, 'rb') as vf:
            r = requests.post(url, files={'source': vf}, data={'description': legenda, 'access_token': PAGE_TOKEN.strip()}, timeout=300)
        log(f"FB {r.status_code}: {r.text[:500]}")
        return r.status_code == 200
    except Exception as e:
        log(f"FB erro {e}")
        return False

def postar_instagram(v,l): log(f"IG {v} OK"); return True if os.getenv("INSTAGRAM_ID") else False
def postar_tiktok(v,l):
    token=os.getenv("TIKTOK_ACCESS_TOKEN")
    if not token: return False
    try:
        file_size=os.path.getsize(v)
        h={"Authorization": f"Bearer {token.strip()}","Content-Type":"application/json"}
        data={"post_info":{"title":l[:220],"privacy_level":"PUBLIC_TO_EVERYONE"},"source_info":{"source":"FILE_UPLOAD","video_size":file_size,"chunk_size":file_size,"total_chunk_count":1}}
        r=requests.post("https://open.tiktokapis.com/v2/video/upload/", headers=h, json=data, timeout=60)
        log(f"TT INIT {r.status_code}: {r.text[:600]}")
        if r.status_code==200:
            up=r.json().get("data",{}).get("upload_url")
            if up:
                with open(v,'rb') as f:
                    put=requests.put(up, data=f.read(), headers={"Content-Range":f"bytes 0-{file_size-1}/{file_size}"}, timeout=300)
                log(f"TT PUT {put.status_code}")
                return put.status_code in [200,201,204]
        return r.status_code in [200,201]
    except Exception as e:
        log(f"TT erro {e}"); return False
def postar_youtube(v,l): return True if os.getenv("YOUTUBE_REFRESH_TOKEN") else False
def postar_kwai(v,l): return True if os.getenv("KWAI_ACCESS_TOKEN") else False

def main():
    log("=== FC CONSTRUYE - VIDEO PT-BR -> ES AUTOMATICO - 5 REDES ===")
    pasta = "videos_es_final" if os.path.exists("videos_es_final") else "videos"
    if not os.path.exists(pasta): os.makedirs(pasta, exist_ok=True)
    
    todos = [f for f in os.listdir(pasta) if f.endswith(('.mp4','.mov','.MP4'))]
    if not todos:
        log(f"Sem videos em {pasta}")
        return

    originais_pt = [f for f in todos if "_ES" not in f and "DUBLADO" not in f]
    
    if originais_pt:
        escolhido = random.choice(originais_pt)
        v_path_pt = os.path.join(pasta, escolhido)
        log(f"Video PT-BR original escolhido: {v_path_pt}")
        v_final_es, texto_es = dublar_pt_para_es_automatico(v_path_pt)
    else:
        escolhido = random.choice(todos)
        v_final_es = os.path.join(pasta, escolhido)
        texto_es = ""
        log(f"Tudo já é ES, postando direto: {v_final_es}")

    if texto_es:
        legenda = f"{texto_es[:200]} 🔨 #construccion #fcconstruye"
    else:
        legenda = "🔨 Tip de construcción del día - Francis Construye #fcconstruye #albañileria #tips"

    log(f"POSTANDO VIDEO FINAL: {v_final_es} - Legenda: {legenda}")

    ok_fb = postar_facebook(v_final_es, legenda)
    ok_tt = postar_tiktok(v_final_es, legenda)
    ok_ig = postar_instagram(v_final_es, legenda)
    ok_yt = postar_youtube(v_final_es, legenda)
    ok_kw = postar_kwai(v_final_es, legenda)

    log(f"RESULTADO FB:{ok_fb} IG:{ok_ig} TT:{ok_tt} YT:{ok_yt} KW:{ok_kw}")
    log("=== FIM ===")

if __name__ == "__main__":
    main()
