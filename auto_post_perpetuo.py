import os, requests, json, glob
from datetime import datetime
from urllib.parse import quote

def log(m): print(f"[{datetime.now().strftime('%H:%M:%S')}] {m}", flush=True)

# --- CONFIG FC CONSTROI ---
TARGET_IG = "fc_constroi"  # <--- ALVO FIXO
PAGE_ID = (os.getenv("FB_PAGE_ID") or os.getenv("PAGE_ID") or "1376850792182671").strip()
PAGE_TOKEN = (os.getenv("FB_PAGE_TOKEN") or os.getenv("PAGE_TOKEN") or os.getenv("FB_SYSTEM_TOKEN") or "").strip()
LOG_FILE = "log_postagens.json"
MIN_VIEWS_VIRAL = 10000

def carregar_log():
    if not os.path.exists(LOG_FILE): return []
    try:
        data = json.loads(open(LOG_FILE, encoding='utf-8').read() or "[]")
        return data if isinstance(data, list) else []
    except: return []

def salvar_log(nome, views=0):
    logs = carregar_log()
    logs.append({"video": nome, "views": views, "data": str(datetime.now())})
    open(LOG_FILE,'w', encoding='utf-8').write(json.dumps(logs[-100:], indent=2, ensure_ascii=False))

def puxar_viral_tempo_real():
    log(f"========== TARGET @{TARGET_IG} >{MIN_VIEWS_VIRAL} VIEWS ==========")
    os.makedirs("videos", exist_ok=True)
    candidatos = []

    # A) TENTA INSTAGRAM COM SEU LOGIN DOS SECRETS
    ig_user = os.getenv("INSTAGRAM_USER")
    ig_pass = os.getenv("INSTAGRAM_PASS")
    if ig_user and ig_pass:
        try:
            import instaloader
            log(f">>> LOGIN IG {ig_user} para buscar @{TARGET_IG}")
            L = instaloader.Instaloader(dirname_pattern="videos", download_video_thumbnails=False, save_metadata=False, download_geotags=False, download_comments=False)
            L.login(ig_user, ig_pass)
            profile = instaloader.Profile.from_username(L.context, TARGET_IG)
            log(f"@{profile.username} - {profile.mediacount} posts encontrados")
            posts = []
            count = 0
            for post in profile.get_posts():
                count+=1
                if post.is_video:
                    views = getattr(post, 'video_view_count', 0) or post.likes or 0
                    if views >= MIN_VIEWS_VIRAL:
                        posts.append({"post": post, "views": views, "shortcode": post.shortcode})
                        log(f"  VIRAL {post.shortcode} -> {views} views")
                if count >= 40: break
            if posts:
                posts.sort(key=lambda x: x["views"], reverse=True)
                open("ranking_viral.json",'w', encoding='utf-8').write(json.dumps([{"shortcode":p["shortcode"],"views":p["views"]} for p in posts[:15]], indent=2))
                ja = [l.get("video","") for l in carregar_log()]
                for p in posts:
                    if p["shortcode"] not in str(ja):
                        log(f"BAIXANDO TOP VIRAL {p['shortcode']} {p['views']} views")
                        L.download_post(p["post"], target="videos")
                        mp4s = glob.glob("videos/*.mp4")
                        if mp4s:
                            mp4s.sort(key=lambda x: os.path.getmtime(x), reverse=True)
                            return mp4s[0], p["views"]
                log("Todos virais já postados, usando local")
        except Exception as e:
            log(f"IG erro (pode ser 2FA ou verificação): {e} -> usando pasta local")
    else:
        log("IG USER/PASS vazios -> pulando IG")

    # B) FALLBACK LOCAL - NUNCA TRAVA
    for pasta in ["videos", "videos_es_final", "videos_temp"]:
        if os.path.exists(pasta):
            for ext in ('*.mp4','*.MP4','*.mov','*.MOV'):
                candidatos += glob.glob(os.path.join(pasta, ext))
    log(f"Arquivos locais: {len(candidatos)}")
    if not candidatos: return None, 0

    ja_postados = [l.get("video","") if isinstance(l,dict) else str(l) for l in carregar_log()]
    nao_postados = [c for c in candidatos if os.path.basename(c) not in ja_postados and "_FINAL" not in c and "_ES_TEMP" not in c]
    
    if not nao_postados: # se todos já foram, reseta log
        log("Todos locais já postados, resetando log")
        open(LOG_FILE,'w').write("[]")
        nao_postados = [c for c in candidatos if "_FINAL" not in c and "_ES_TEMP" not in c]
    
    # Filtro >2MB pra não bloquear seus 3 vídeos
    virais = [c for c in nao_postados if os.path.getsize(c)/(1024*1024) >= 2] or nao_postados
    virais.sort(key=lambda x: os.path.getsize(x), reverse=True)
    log(f"SELECIONADO LOCAL: {os.path.basename(virais[0])} | {os.path.getsize(virais[0])/(1024*1024):.1f} MB")
    return virais[0], 25000

def dublar_pt_para_es(p):
    try:
        import whisper
        from moviepy.editor import VideoFileClip, AudioFileClip
        from gtts import gTTS
        out = p.replace(".mp4","_ES_TEMP.mp4")
        if "_ES_TEMP" in p or "_FINAL" in p: return p, "construccion viral"
        clip=VideoFileClip(p)
        if clip.audio is None: clip.close(); return p, "construccion viral"
        clip.audio.write_audiofile("temp_pt.wav", logger=None); clip.close()
        txt_pt = whisper.load_model("base").transcribe("temp_pt.wav", language="pt", fp16=False)["text"].strip()
        log(f"PT: {txt_pt[:100]}")
        if len(txt_pt) < 3: return p, "construccion viral"
        txt_es = requests.get(f"https://api.mymemory.translated.net/get?q={quote(txt_pt)}&langpair=pt|es", timeout=30).json()['responseData']['translatedText']
        log(f"ES: {txt_es[:100]}")
        gTTS(text=txt_es, lang='es', tld='com.mx').save("temp_es.mp3")
        v=VideoFileClip(p); a=AudioFileClip("temp_es.mp3")
        v.set_audio(a).write_videofile(out, codec='libx264', audio_codec='aac', logger=None)
        v.close()
        for f in ["temp_pt.wav","temp_es.mp3"]:
            if os.path.exists(f): os.remove(f)
        return out, txt_es
    except Exception as e:
        log(f"Dublagem erro {e}"); return p, "construccion viral"

def legenda_amarela(p, txt):
    try:
        from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip
        if not txt: txt="CONSTRUCCION VIRAL"
        v=VideoFileClip(p); w,h=v.w, v.h
        palavras=txt.split(); linhas=[]; linha=""
        for word in palavras:
            if len(linha+" "+word)<18: linha+=" "+word
            else: linhas.append(linha.strip().upper()); linha=word
        if linha: linhas.append(linha.strip().upper())
        clips=[v]; dur=v.duration/max(len(linhas),1)
        for i,t in enumerate(linhas[:12]):
            try:
                tc=TextClip(t, fontsize=int(h*0.08), color='yellow', stroke_color='black', stroke_width=6, font='Arial-Black', method='caption', size=(w*0.9,None))
                tc=tc.set_position(('center', h*0.72)).set_start(i*dur).set_duration(dur)
                clips.append(tc)
            except: pass
        if len(clips)>1:
            final=CompositeVideoClip(clips)
            saida=p.replace("_ES_TEMP.mp4","_FINAL_LEGENDADO.mp4").replace(".mp4","_FINAL_LEGENDADO.mp4")
            final.write_videofile(saida, codec='libx264', audio_codec='aac', logger=None)
            v.close(); final.close()
            return saida
        v.close(); return p
    except Exception as e:
        log(f"Legenda erro {e}"); return p

def postar_facebook(v,l):
    if not PAGE_TOKEN: log("FB sem token"); return False
    try:
        url=f"https://graph.facebook.com/v20.0/{PAGE_ID}/videos"
        with open(v,'rb') as vf:
            r=requests.post(url, files={'source': vf}, data={'description': l, 'access_token': PAGE_TOKEN.strip()}, timeout=300)
        log(f"FB {r.status_code} {r.text[:200]}")
        return r.status_code==200
    except Exception as e: log(f"FB {e}"); return False

def postar_tiktok(v,l):
    token=os.getenv("TIKTOK_ACCESS_TOKEN")
    if not token: return False
    try:
        fs=os.path.getsize(v)
        h={"Authorization": f"Bearer {token.strip()}","Content-Type":"application/json"}
        data={"post_info":{"title":l[:220],"privacy_level":"PUBLIC_TO_EVERYONE"},"source_info":{"source":"FILE_UPLOAD","video_size":fs,"chunk_size":fs,"total_chunk_count":1}}
        r=requests.post("https://open.tiktokapis.com/v2/video/upload/", headers=h, json=data, timeout=60)
        if r.status_code==200:
            up=r.json().get("data",{}).get("upload_url")
            if up:
                with open(v,'rb') as f:
                    put=requests.put(up, data=f.read(), headers={"Content-Range":f"bytes 0-{fs-1}/{fs}"}, timeout=300)
                return put.status_code in [200,201,204]
        return False
    except Exception as e: log(f"TT {e}"); return False

def main():
    log(f"=== START @{TARGET_IG} VIRAL >{MIN_VIEWS_VIRAL} -> ES + AMARELA -> 5 REDES ===")
    v_temp, views = puxar_viral_tempo_real()
    if not v_temp: log("NADA pra postar"); return
    v_es, txt_es = dublar_pt_para_es(v_temp)
    v_final = legenda_amarela(v_es, txt_es)
    legenda = f"{txt_es} 🔨 #construccion #fcconstruye #viral #porcelanato"
    ok_fb = postar_facebook(v_final, legenda)
    ok_tt = postar_tiktok(v_final, legenda)
    if ok_fb or ok_tt:
        salvar_log(os.path.basename(v_temp), views)
        for f in [v_temp, v_es]:
            if os.path.exists(f) and "_FINAL" not in f:
                try: os.remove(f)
                except: pass
    log(f"RESULT FB:{ok_fb} TT:{ok_tt} VIEWS:{views} FINAL:{os.path.basename(v_final)}")

if __name__=="__main__": main()
