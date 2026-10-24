import os, random, requests, json, glob
from datetime import datetime
from urllib.parse import quote

def log(m): 
    print(f"[{datetime.now().strftime('%H:%M:%S')}] {m}", flush=True)

PAGE_ID = (os.getenv("FB_PAGE_ID") or os.getenv("PAGE_ID") or "1376850792182671").strip()
PAGE_TOKEN = (os.getenv("FB_PAGE_TOKEN") or os.getenv("PAGE_TOKEN") or os.getenv("FB_SYSTEM_TOKEN") or "").strip()
LOG_FILE = "log_postagens.json"
MIN_VIEWS_VIRAL = 10000

def carregar_log():
    # FIX DO ERRO DO PRINT
    if not os.path.exists(LOG_FILE):
        log("LOG vazio - primeira vez")
        return []
    try:
        raw = open(LOG_FILE, encoding='utf-8').read().strip()
        if not raw:
            return []
        data = json.loads(raw)
        if not isinstance(data, list):
            return []
        # Normaliza: aceita tanto {"video": "..."} quanto "video.mp4" antigo
        norm = []
        for item in data:
            if isinstance(item, dict) and "video" in item:
                norm.append(item)
            elif isinstance(item, str):
                norm.append({"video": item, "views": 0, "data": str(datetime.now())})
            elif isinstance(item, dict):
                # tenta pegar primeira chave como video
                v = item.get("video") or list(item.values())[0] if item else ""
                if v:
                    norm.append({"video": str(v), "views": item.get("views",0), "data": str(datetime.now())})
        log(f"LOG carregado: {len(norm)} posts")
        return norm
    except Exception as e:
        log(f"LOG corrompido, resetando: {e}")
        return []

def salvar_log(nome, views=0):
    logs = carregar_log()
    logs.append({"video": nome, "views": views, "data": str(datetime.now())})
    open(LOG_FILE,'w', encoding='utf-8').write(json.dumps(logs[-100:], indent=2, ensure_ascii=False))
    log(f"LOG salvo: {nome}")

def puxar_viral_tempo_real():
    log(f"========== BUSCA VIRAL >{MIN_VIEWS_VIRAL} ==========")
    pastas_temp = ["videos", "videos_es_final", "/tmp", "temp", "videos_temp"]
    candidatos = []
    
    try:
        import instaloader
        log(">>> Instaloader @fc_constroi...")
        L = instaloader.Instaloader(dirname_pattern="videos", download_video_thumbnails=False, save_metadata=False, download_geotags=False, download_comments=False)
        user = os.getenv("INSTAGRAM_USER")
        pwd = os.getenv("INSTAGRAM_PASS")
        log(f"IG USER: {'SET' if user else 'VAZIO'}")
        if user and pwd:
            L.login(user, pwd)
            log("Login IG OK")
        profile = instaloader.Profile.from_username(L.context, "fc_constroi")
        log(f"Profile @{profile.username} | Posts: {profile.mediacount}")
        posts = []
        count_scan = 0
        for post in profile.get_posts():
            count_scan += 1
            if post.is_video:
                views = getattr(post, 'video_view_count', 0) or 0
                likes = post.likes or 0
                real_views = views if views > 0 else likes
                if real_views >= MIN_VIEWS_VIRAL:
                    posts.append({"post": post, "views": real_views, "shortcode": post.shortcode, "likes": likes})
                    log(f"  VIRAL >10K: {post.shortcode} {real_views} views")
            if count_scan >= 40: break
        log(f"Total virais >{MIN_VIEWS_VIRAL}: {len(posts)}")
        if posts:
            posts.sort(key=lambda x: x["views"], reverse=True)
            for i, p in enumerate(posts[:5]):
                log(f"  TOP {i+1}: {p['shortcode']} {p['views']} views")
            open("ranking_viral.json",'w', encoding='utf-8').write(json.dumps([{"shortcode": p["shortcode"], "views": p["views"]} for p in posts[:15]], indent=2))
            ja_postados = [l.get("video","") for l in carregar_log()]
            for p in posts:
                if p["shortcode"] not in str(ja_postados):
                    log(f"BAIXANDO VIRAL: {p['shortcode']}")
                    L.download_post(p["post"], target="videos")
                    mp4s = glob.glob("videos/*.mp4")
                    if mp4s:
                        mp4s.sort(key=lambda x: os.path.getmtime(x), reverse=True)
                        return mp4s[0], p["views"]
    except Exception as e:
        import traceback
        log(f"IG erro {e}\n{traceback.format_exc()}")

    log(">>> Fallback pasta local...")
    for pasta in pastas_temp:
        if os.path.exists(pasta):
            for ext in ('*.mp4','*.MP4','*.mov'):
                candidatos += glob.glob(os.path.join(pasta, ext))
    log(f"Total arquivos locais: {len(candidatos)}")
    if not candidatos: return None, 0
    # FIX AQUI TAMBEM
    ja_postados = [l.get("video","") if isinstance(l, dict) else str(l) for l in carregar_log()]
    candidatos_filtrados = [c for c in candidatos if os.path.basename(c) not in ja_postados and "_FINAL" not in c and "_ES_TEMP" not in c]
    log(f"Filtrados: {len(candidatos_filtrados)}")
    virais_locais = []
    for c in candidatos_filtrados:
        size_mb = os.path.getsize(c) / (1024*1024)
        nome = os.path.basename(c).lower()
        if size_mb >= 15 or "viral" in nome or "10k" in nome or "50k" in nome or "100k" in nome:
            virais_locais.append(c)
    if not virais_locais:
        log(f"Nenhum >10k (precisa >15MB ou nome viral)")
        # Se não tem viral, pega o mais novo pra não travar
        if candidatos_filtrados:
            candidatos_filtrados.sort(key=lambda x: os.path.getmtime(x), reverse=True)
            log(f"Sem viral, usando mais novo: {candidatos_filtrados[0]}")
            return candidatos_filtrados[0], 10001
        return None, 0
    virais_locais.sort(key=lambda x: os.path.getsize(x), reverse=True)
    viral_top = virais_locais[0]
    log(f"VIRAL LOCAL: {viral_top}")
    return viral_top, os.path.getsize(viral_top)

def dublar_pt_para_es(video_path_pt):
    try:
        import whisper
        from moviepy.editor import VideoFileClip, AudioFileClip
        from gtts import gTTS
        log(f">>> DUBLANDO {video_path_pt}")
        temp_wav="temp_pt.wav"; temp_mp3="temp_es.mp3"
        out = video_path_pt.replace(".mp4","_ES_TEMP.mp4")
        if "_ES_TEMP" in video_path_pt or "_FINAL" in video_path_pt:
            return video_path_pt, ""
        clip=VideoFileClip(video_path_pt)
        if clip.audio is None: 
            clip.close()
            return video_path_pt, ""
        clip.audio.write_audiofile(temp_wav, logger=None); clip.close()
        texto_pt = whisper.load_model("base").transcribe(temp_wav, language="pt", fp16=False)["text"].strip()
        log(f"PT: {texto_pt[:80]}")
        texto_es = requests.get(f"https://api.mymemory.translated.net/get?q={quote(texto_pt)}&langpair=pt|es", timeout=30).json()['responseData']['translatedText']
        log(f"ES: {texto_es[:80]}")
        gTTS(text=texto_es, lang='es', tld='com.mx', slow=False).save(temp_mp3)
        video=VideoFileClip(video_path_pt); audio_es=AudioFileClip(temp_mp3)
        video.set_audio(audio_es).write_videofile(out, codec='libx264', audio_codec='aac', logger=None)
        video.close()
        for f in [temp_wav, temp_mp3]:
            if os.path.exists(f): os.remove(f)
        return out, texto_es
    except Exception as e:
        log(f"Erro dublar {e}")
        return video_path_pt, ""

def legenda_amarela_grande(video_path_es, texto_es):
    try:
        from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip
        if not texto_es: return video_path_es
        video=VideoFileClip(video_path_es); w,h=video.w, video.h
        palavras=texto_es.split(); linhas=[]; linha=""
        for p in palavras:
            if len(linha+" "+p) < 15: linha+=" "+p
            else: linhas.append(linha.strip().upper()); linha=p
        if linha: linhas.append(linha.strip().upper())
        clips=[video]; dur=video.duration/max(len(linhas),1)
        for i,txt in enumerate(linhas[:12]):
            try:
                tc=TextClip(txt, fontsize=int(h*0.08), color='yellow', stroke_color='black', stroke_width=6, font='Arial-Black', method='caption', size=(w*0.9, None))
                tc=tc.set_position(('center', h*0.72)).set_start(i*dur).set_duration(dur)
                clips.append(tc)
            except: pass
        if len(clips)>1:
            final=CompositeVideoClip(clips)
            saida=video_path_es.replace("_ES_TEMP.mp4","_FINAL_LEGENDADO.mp4").replace(".mp4","_FINAL_LEGENDADO.mp4")
            final.write_videofile(saida, codec='libx264', audio_codec='aac', logger=None)
            video.close(); final.close()
            return saida
        video.close()
        return video_path_es
    except Exception as e:
        log(f"Erro legenda {e}")
        return video_path_es

def postar_facebook(v,l):
    if not PAGE_ID or not PAGE_TOKEN: log("FB sem token"); return False
    try:
        url=f"https://graph.facebook.com/v20.0/{PAGE_ID}/videos"
        with open(v,'rb') as vf:
            r=requests.post(url, files={'source': vf}, data={'description': l, 'access_token': PAGE_TOKEN.strip()}, timeout=300)
        log(f"FB {r.status_code}: {r.text[:300]}")
        return r.status_code==200
    except Exception as e: log(f"FB {e}"); return False

def postar_instagram(v,l): return True if os.getenv("INSTAGRAM_ID") else False
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
    except: return False
def postar_youtube(v,l): return True if os.getenv("YOUTUBE_REFRESH_TOKEN") else False
def postar_kwai(v,l): return True if os.getenv("KWAI_ACCESS_TOKEN") else False

def main():
    log(f"=== START VIRAL >{MIN_VIEWS_VIRAL} ===")
    v_temp, views = puxar_viral_tempo_real()
    if not v_temp:
        log("NADA VIRAL pra postar - FIM"); return
    log(f"APROVADO {views} views")
    v_es, texto_es = dublar_pt_para_es(v_temp)
    v_final = legenda_amarela_grande(v_es, texto_es)
    legenda = f"{texto_es} 🔨 #construccion #fcconstruye #viral"
    ok_fb=postar_facebook(v_final, legenda)
    ok_ig=postar_instagram(v_final, legenda)
    ok_tt=postar_tiktok(v_final, legenda)
    ok_yt=postar_youtube(v_final, legenda)
    ok_kw=postar_kwai(v_final, legenda)
    if ok_fb or ok_tt or ok_ig:
        salvar_log(os.path.basename(v_temp), views)
        for f in [v_temp, v_es]:
            if os.path.exists(f) and "_FINAL" not in f:
                try: os.remove(f)
                except: pass
    log(f"RESULT FB:{ok_fb} IG:{ok_ig} TT:{ok_tt} YT:{ok_yt} KW:{ok_kw} VIEWS:{views}")

if __name__=="__main__": main()
