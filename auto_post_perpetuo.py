import os, random, requests, json
from datetime import datetime

def log(m): print(f"[{datetime.now()}] {m}", flush=True)

PAGE_ID = os.getenv("PAGE_ID") # 61595702674802
PAGE_TOKEN = os.getenv("PAGE_TOKEN")
ELEVEN_KEY = os.getenv("ELEVENLABS_API_KEY")

def postar_facebook(video_path, legenda):
    try:
        url = f"https://graph.facebook.com/v20.0/{PAGE_ID}/videos"
        with open(video_path, 'rb') as vf:
            r = requests.post(url, files={'source': vf}, data={'description': legenda, 'access_token': PAGE_TOKEN}, timeout=180)
        log(f"Facebook {r.status_code}: {r.text[:500]}")
        return r.status_code == 200
    except Exception as e:
        log(f"FB erro {e}")
        return False

def postar_instagram(video_path, legenda):
    try:
        IG_ID = os.getenv("INSTAGRAM_ID")
        if not IG_ID: 
            log("Instagram: SEM INSTAGRAM_ID - pula")
            return False
        # Instagram precisa de URL publica, por enquanto loga
        log(f"Instagram: video {video_path} pronto para {IG_ID}")
        return True
    except Exception as e:
        log(f"IG erro {e}")
        return False

def postar_tiktok(video_path, legenda):
    token = os.getenv("TIKTOK_ACCESS_TOKEN")
    if not token:
        log("TikTok: SEM TOKEN - Coloca TIKTOK_ACCESS_TOKEN nos Secrets")
        return False
    log(f"TikTok: postaria {video_path} - token OK")
    return True

def postar_youtube(video_path, legenda):
    refresh = os.getenv("YOUTUBE_REFRESH_TOKEN")
    if not refresh:
        log("YouTube: SEM REFRESH_TOKEN")
        return False
    log(f"YouTube Shorts: postaria {video_path}")
    return True

def postar_kwai(video_path, legenda):
    token = os.getenv("KWAI_ACCESS_TOKEN")
    if not token:
        log("Kwai: SEM TOKEN")
        return False
    log(f"Kwai: postaria {video_path}")
    return True

def main():
    log("=== POST 5 REDES FC ===")
    pasta = "videos_es_final" if os.path.exists("videos_es_final") else "videos"
    vids = [f for f in os.listdir(pasta) if f.endswith(('.mp4','.mov'))]
    if not vids:
        log("Sem videos")
        return
    vpath = random.choice([os.path.join(pasta, f) for f in vids])
    legenda = "🔨 Tip de albañilería del día - Francis Construye #construccion #tips"

    log(f"Video: {vpath}")
    postar_facebook(vpath, legenda)
    postar_instagram(vpath, legenda)
    postar_tiktok(vpath, legenda)
    postar_youtube(vpath, legenda)
    postar_kwai(vpath, legenda)
    log("=== FIM 5 REDES ===")

if __name__ == "__main__":
    main()
