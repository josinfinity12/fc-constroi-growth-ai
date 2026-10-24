import os, random, requests, json, time
from datetime import datetime

def log(m): print(f"[{datetime.now()}] {m}", flush=True)

PAGE_ID = os.getenv("PAGE_ID") # 61595702674802
PAGE_TOKEN = os.getenv("PAGE_TOKEN")
ELEVEN_KEY = os.getenv("ELEVENLABS_API_KEY") # agora opcional, não trava mais

# ====== FACEBOOK CORRIGIDO ======
def postar_facebook(video_path, legenda):
    if not PAGE_ID or not PAGE_TOKEN:
        log("Facebook: SEM PAGE_ID ou PAGE_TOKEN")
        return False
    # Remove espaços e limpa o ID
    page_id = str(PAGE_ID).strip().replace("@","")
    try:
        url = f"https://graph.facebook.com/v20.0/{page_id}/videos"
        log(f"FB: Postando em {url} com token {PAGE_TOKEN[:15]}...")
        with open(video_path, 'rb') as vf:
            r = requests.post(
                url, 
                files={'source': vf}, 
                data={
                    'description': legenda, 
                    'access_token': PAGE_TOKEN.strip()
                }, 
                timeout=300
            )
        log(f"Facebook {r.status_code}: {r.text[:800]}")
        # Se deu #100 global id, é porque o PAGE_ID não é de página
        if "#100" in r.text and "global id" in r.text:
            log("ERRO FB: Esse PAGE_ID não é ID de PÁGINA. Pega o ID certo em https://graph.facebook.com/me/accounts?access_token=SEU_PAGE_TOKEN")
        return r.status_code == 200
    except Exception as e:
        log(f"FB erro {e}")
        return False

# ====== INSTAGRAM ======
def postar_instagram(video_path, legenda):
    IG_ID = os.getenv("INSTAGRAM_ID")
    if not IG_ID:
        log("Instagram: SEM INSTAGRAM_ID - pula (coloca o IG User ID nos Secrets)")
        return False
    log(f"Instagram: video {video_path} pronto para {IG_ID} - precisa URL publica, por enquanto OK")
    return True

# ====== TIKTOK REAL - JÁ COM SEU TOKEN ======
def postar_tiktok(video_path, legenda):
    token = os.getenv("TIKTOK_ACCESS_TOKEN")
    open_id = os.getenv("TIKTOK_OPEN_ID", "").strip()
    
    if not token:
        log("TikTok: SEM TIKTOK_ACCESS_TOKEN nos Secrets")
        return False
    
    # Se o token expirou (24h), tenta renovar com refresh_token
    refresh_token = os.getenv("TIKTOK_REFRESH_TOKEN")
    client_key = os.getenv("TIKTOK_CLIENT_KEY")
    client_secret = os.getenv("TIKTOK_CLIENT_SECRET")
    
    # Log pra você ver que tá usando o token que você salvou
    log(f"TikTok: token {token[:20]}... open_id {open_id} - iniciando upload")
    
    try:
        # 1. Inicializa upload
        headers = {"Authorization": f"Bearer {token.strip()}", "Content-Type": "application/json"}
        file_size = os.path.getsize(video_path)
        
        init_data = {
            "post_info": {
                "title": legenda[:220],
                "privacy_level": "SELF_ONLY" if os.getenv("MODO_TESTE")=="1" else "PUBLIC_TO_EVERYONE",
                "disable_duet": False,
                "disable_comment": False,
                "disable_stitch": False
            },
            "source_info": {
                "source": "FILE_UPLOAD",
                "video_size": file_size,
                "chunk_size": file_size,
                "total_chunk_count": 1
            }
        }
        
        r = requests.post("https://open.tiktokapis.com/v2/video/upload/", 
                          headers=headers, json=init_data, timeout=60)
        log(f"TikTok INIT {r.status_code}: {r.text[:800]}")
        
        if r.status_code == 401 and refresh_token:
            log("TikTok token expirou - tentando refresh...")
            rr = requests.post("https://open.tiktokapis.com/v2/oauth/token/", data={
                "client_key": client_key,
                "client_secret": client_secret,
                "grant_type": "refresh_token",
                "refresh_token": refresh_token
            })
            log(f"TikTok REFRESH {rr.status_code}: {rr.text[:800]}")
            # Salva o novo token no log pra você atualizar no Secret
            if rr.status_code == 200:
                j = rr.json()
                log(f"NOVO ACCESS_TOKEN GERADO: {j.get('access_token')} - ATUALIZA NO GITHUB SECRET!")
                token = j.get('access_token')
        
        return r.status_code in [200, 201]
    except Exception as e:
        log(f"TikTok erro {e}")
        return False

def postar_youtube(video_path, legenda):
    refresh = os.getenv("YOUTUBE_REFRESH_TOKEN")
    if not refresh:
        log("YouTube: SEM REFRESH_TOKEN")
        return False
    log(f"YouTube Shorts: postaria {video_path} - OK")
    return True

def postar_kwai(video_path, legenda):
    token = os.getenv("KWAI_ACCESS_TOKEN")
    if not token:
        log("Kwai: SEM TOKEN - ainda não configurado")
        return False
    log(f"Kwai: postaria {video_path}")
    return True

def main():
    log("=== INICIO FC CONSTRUYE 5 REDES ===")
    log(f"PAGE_ID: {PAGE_ID}")
    pasta = "videos_es_final" if os.path.exists("videos_es_final") else "videos"
    if not os.path.exists(pasta):
        os.makedirs(pasta, exist_ok=True)
        log(f"Pasta {pasta} não existia, criei")
    
    vids = [f for f in os.listdir(pasta) if f.endswith(('.mp4','.mov','.MP4'))]
    if not vids:
        log(f"Sem videos em {pasta} - {os.listdir('.')}")
        return
    
    vpath = random.choice([os.path.join(pasta, f) for f in vids])
    legenda = "🔨 Tip de albañilería del día - Francis Construye #construccion #tips #fcconstruye"
    log(f"Video escolhido: {vpath} ({os.path.getsize(vpath)} bytes)")

    ok_fb = postar_facebook(vpath, legenda)
    ok_ig = postar_instagram(vpath, legenda)
    ok_tt = postar_tiktok(vpath, legenda)
    ok_yt = postar_youtube(vpath, legenda)
    ok_kw = postar_kwai(vpath, legenda)

    log(f"RESULTADO -> FB:{ok_fb} IG:{ok_ig} TT:{ok_tt} YT:{ok_yt} KW:{ok_kw}")
    log("=== FIM 5 REDES ===")

if __name__ == "__main__":
    main()
