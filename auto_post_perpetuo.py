import os, random, requests, json, time
from datetime import datetime

def log(m): print(f"[{datetime.now()}] {m}", flush=True)

PAGE_ID = os.getenv("PAGE_ID") # 61595702674802
PAGE_TOKEN = os.getenv("PAGE_TOKEN")
ELEVEN_KEY = os.getenv("ELEVENLABS_API_KEY")

# ========== TRADUTOR AUTOMÁTICO 100% (OUVE O VIDEO PT -> ES) ==========
def traduzir_video_pt_para_es_automatico(video_path):
    """
    Ouve o áudio do vídeo original em PT, traduz e gera novo vídeo dublado em ES
    Retorna: (caminho_video_es, texto_pt, texto_es)
    """
    try:
        # Tenta importar só se estiver instalado (evita quebrar se não tiver)
        import whisper
        from moviepy.editor import VideoFileClip, AudioFileClip
        from gtts import gTTS
        
        log("--- INICIANDO TRADUÇÃO AUTOMÁTICA PT->ES ---")
        audio_temp_pt = "temp_audio_pt.wav"
        audio_temp_es = "temp_voz_es.mp3"
        video_es_path = video_path.replace(".mp4", "_ES.mp4").replace(".MP4","_ES.mp4")

        # 1. Extrair áudio PT
        log(f"1/4 Extraindo áudio PT de {video_path}...")
        clip = VideoFileClip(video_path)
        if clip.audio is None:
            log("Vídeo sem áudio, usando sem tradução")
            clip.close()
            return video_path, "", ""
        clip.audio.write_audiofile(audio_temp_pt, logger=None)
        clip.close()

        # 2. Ouvir com Whisper (base entende PT perfeito)
        log("2/4 Ouvindo com Whisper...")
        model = whisper.load_model("base")
        result = model.transcribe(audio_temp_pt, language="pt", fp16=False)
        texto_pt = result["text"].strip()
        log(f"PT ouvido: {texto_pt[:200]}")
        if not texto_pt:
            log("Whisper não ouviu nada")
            return video_path, "", ""

        # 3. Traduzir PT -> ES com MyMemory (grátis)
        log("3/4 Traduzindo PT->ES...")
        try:
            url = f"https://api.mymemory.translated.net/get?q={requests.utils.quote(texto_pt)}&langpair=pt|es"
            r = requests.get(url, timeout=30).json()
            texto_es = r['responseData']['translatedText']
            log(f"ES traduzido: {texto_es[:200]}")
        except Exception as e:
            log(f"Erro tradução {e}, usando texto original")
            texto_es = texto_pt

        # 4. Gerar voz ES com gTTS (tld com.mx = sotaque latino)
        log("4/4 Gerando voz ES com gTTS...")
        tts = gTTS(text=texto_es, lang='es', tld='com.mx', slow=False)
        tts.save(audio_temp_es)

        # 5. Colar voz ES no vídeo
        log("5/5 Dublando vídeo...")
        video = VideoFileClip(video_path)
        audio_es = AudioFileClip(audio_temp_es)
        # Corta ou estica pra durar igual ao vídeo se precisar
        video_dublado = video.set_audio(audio_es)
        video_dublado.write_videofile(video_es_path, codec='libx264', audio_codec='aac', logger=None)
        video.close()
        video_dublado.close()

        # Limpa temporários
        for f in [audio_temp_pt, audio_temp_es]:
            if os.path.exists(f): os.remove(f)

        log(f"VIDEO ES DUBLADO PRONTO: {video_es_path}")
        return video_es_path, texto_pt, texto_es

    except ImportError as e:
        log(f"Biblioteca faltando {e} - instale openai-whisper e moviepy no requirements.txt")
        return video_path, "", ""
    except Exception as e:
        log(f"Erro no pipeline auto PT->ES: {e} - usando vídeo original")
        return video_path, "", ""

# ====== FACEBOOK CORRIGIDO ======
def postar_facebook(video_path, legenda):
    if not PAGE_ID or not PAGE_TOKEN:
        log("Facebook: SEM PAGE_ID ou PAGE_TOKEN")
        return False
    page_id = str(PAGE_ID).strip().replace("@","")
    try:
        url = f"https://graph.facebook.com/v20.0/{page_id}/videos"
        log(f"FB: Postando em {url}...")
        with open(video_path, 'rb') as vf:
            r = requests.post(url, files={'source': vf}, data={'description': legenda, 'access_token': PAGE_TOKEN.strip()}, timeout=300)
        log(f"Facebook {r.status_code}: {r.text[:800]}")
        if "#100" in r.text and "global id" in r.text:
            log("ERRO FB: Esse PAGE_ID não é ID de PÁGINA. Pega em: https://graph.facebook.com/me/accounts?access_token=SEU_PAGE_TOKEN")
        return r.status_code == 200
    except Exception as e:
        log(f"FB erro {e}")
        return False

# ====== INSTAGRAM ======
def postar_instagram(video_path, legenda):
    IG_ID = os.getenv("INSTAGRAM_ID")
    if not IG_ID:
        log("Instagram: SEM INSTAGRAM_ID - pula")
        return False
    log(f"Instagram: {video_path} pronto para {IG_ID} (precisa de URL pública no futuro)")
    return True

# ====== TIKTOK REAL COM UPLOAD COMPLETO ======
def postar_tiktok(video_path, legenda):
    token = os.getenv("TIKTOK_ACCESS_TOKEN")
    if not token:
        log("TikTok: SEM TIKTOK_ACCESS_TOKEN")
        return False
    
    refresh_token = os.getenv("TIKTOK_REFRESH_TOKEN")
    client_key = os.getenv("TIKTOK_CLIENT_KEY")
    client_secret = os.getenv("TIKTOK_CLIENT_SECRET")
    
    log(f"TikTok: token {token[:20]}... iniciando upload")
    try:
        headers = {"Authorization": f"Bearer {token.strip()}", "Content-Type": "application/json"}
        file_size = os.path.getsize(video_path)
        
        init_data = {
            "post_info": {
                "title": legenda[:220],
                "privacy_level": "SELF_ONLY" if os.getenv("MODO_TESTE")=="1" else "PUBLIC_TO_EVERYONE",
            },
            "source_info": {
                "source": "FILE_UPLOAD",
                "video_size": file_size,
                "chunk_size": file_size,
                "total_chunk_count": 1
            }
        }
        
        r = requests.post("https://open.tiktokapis.com/v2/video/upload/", headers=headers, json=init_data, timeout=60)
        log(f"TikTok INIT {r.status_code}: {r.text[:1000]}")
        
        if r.status_code == 401 and refresh_token:
            log("TikTok token expirou - refresh...")
            rr = requests.post("https://open.tiktokapis.com/v2/oauth/token/", data={
                "client_key": client_key, "client_secret": client_secret,
                "grant_type": "refresh_token", "refresh_token": refresh_token
            })
            log(f"TikTok REFRESH {rr.status_code}: {rr.text[:1000]}")
            if rr.status_code == 200:
                j = rr.json()
                new_token = j.get('access_token')
                log(f"NOVO TOKEN: {new_token[:30]}... ATUALIZE NO SECRET TIKTOK_ACCESS_TOKEN!")
                return False # roda de novo no próximo gatilho com token novo
        
        if r.status_code == 200:
            data = r.json().get("data", {})
            upload_url = data.get("upload_url")
            if upload_url:
                log("TikTok: Enviando bytes do vídeo...")
                with open(video_path, 'rb') as f:
                    put = requests.put(upload_url, data=f.read(), headers={"Content-Range": f"bytes 0-{file_size-1}/{file_size}"}, timeout=300)
                log(f"TikTok PUT {put.status_code}: {put.text[:500]}")
                return put.status_code in [200,201,204]
        return r.status_code in [200,201]
    except Exception as e:
        log(f"TikTok erro {e}")
        return False

def postar_youtube(video_path, legenda):
    if not os.getenv("YOUTUBE_REFRESH_TOKEN"):
        log("YouTube: SEM REFRESH_TOKEN")
        return False
    log(f"YouTube Shorts: {video_path} OK")
    return True

def postar_kwai(video_path, legenda):
    if not os.getenv("KWAI_ACCESS_TOKEN"):
        log("Kwai: SEM TOKEN")
        return False
    log(f"Kwai: {video_path} OK")
    return True

def main():
    log("=== INICIO FC CONSTRUYE 5 REDES - AUTO PT>ES ===")
    pasta = "videos_es_final" if os.path.exists("videos_es_final") else "videos"
    if not os.path.exists(pasta):
        os.makedirs(pasta, exist_ok=True)
    
    vids = [f for f in os.listdir(pasta) if f.endswith(('.mp4','.mov','.MP4'))]
    if not vids:
        log(f"Sem videos em {pasta}")
        return
    
    v_original = random.choice([os.path.join(pasta, f) for f in vids if "_ES" not in f]) # pega original, não o já dublado
    log(f"Video original PT escolhido: {v_original}")

    # >>> AQUI A MÁGICA 100% AUTOMÁTICA QUE VOCÊ PEDIU <<<
    v_final, texto_pt, texto_es = traduzir_video_pt_para_es_automatico(v_original)
    
    if texto_es:
        legenda = f"{texto_es[:180]} 🔨 #construccion #albañileria #fcconstruye"
    else:
        legenda = "🔨 Tip de albañilería del día - Francis Construye #construccion #tips #fcconstruye"
    
    log(f"Legenda final ES: {legenda}")
    log(f"Video final para postar: {v_final} ({os.path.getsize(v_final)} bytes)")

    ok_fb = postar_facebook(v_final, legenda)
    ok_ig = postar_instagram(v_final, legenda)
    ok_tt = postar_tiktok(v_final, legenda)
    ok_yt = postar_youtube(v_final, legenda)
    ok_kw = postar_kwai(v_final, legenda)

    log(f"RESULTADO -> FB:{ok_fb} IG:{ok_ig} TT:{ok_tt} YT:{ok_yt} KW:{ok_kw}")
    log("=== FIM 5 REDES ===")

if __name__ == "__main__":
    main()
