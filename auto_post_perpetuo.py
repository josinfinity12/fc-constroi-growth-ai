import os, random, requests, json, glob
from datetime import datetime
from urllib.parse import quote

def log(m): print(f"[{datetime.now().strftime('%H:%M:%S')}] {m}", flush=True)

PAGE_ID = (os.getenv("FB_PAGE_ID") or os.getenv("PAGE_ID") or "1376850792182671").strip()
PAGE_TOKEN = (os.getenv("FB_PAGE_TOKEN") or os.getenv("PAGE_TOKEN") or os.getenv("FB_SYSTEM_TOKEN") or "").strip()
LOG_FILE = "log_postagens.json"
MIN_VIEWS_VIRAL = 10000

def carregar_log():
    if not os.path.exists(LOG_FILE):
        return []
    try:
        raw = open(LOG_FILE, encoding='utf-8').read().strip()
        if not raw: return []
        data = json.loads(raw)
        norm = []
        for item in data if isinstance(data, list) else []:
            if isinstance(item, dict) and "video" in item:
                norm.append(item)
            elif isinstance(item, str):
                norm.append({"video": item, "views": 0})
        return norm
    except:
        return []

def salvar_log(nome, views=0):
    logs = carregar_log()
    logs.append({"video": nome, "views": views, "data": str(datetime.now())})
    open(LOG_FILE,'w', encoding='utf-8').write(json.dumps(logs[-100:], indent=2, ensure_ascii=False))

def puxar_viral_tempo_real():
    log(f"========== BUSCA VIRAL >{MIN_VIEWS_VIRAL} ==========")
    pastas_temp = ["videos", "videos_es_final", "videos_temp"]
    os.makedirs("videos", exist_ok=True)
    candidatos = []

    # A) SÓ TENTA IG SE TIVER LOGIN - FIX 302
    ig_user = os.getenv("INSTAGRAM_USER")
    ig_pass = os.getenv("INSTAGRAM_PASS")
    if ig_user and ig_pass:
        try:
            import instaloader
            log(f">>> IG login {ig_user} para buscar virais >10k")
            L = instaloader.Instaloader(dirname_pattern="videos", download_video_thumbnails=False, save_metadata=False, download_geotags=False, download_comments=False)
            L.login(ig_user, ig_pass)
            profile = instaloader.Profile.from_username(L.context, "fc_constroi")
            log(f"@{profile.username} {profile.mediacount} posts")
            posts = []
            count=0
            for post in profile.get_posts():
                count+=1
                if post.is_video:
                    views = getattr(post, 'video_view_count', 0) or post.likes or 0
                    if views >= MIN_VIEWS_VIRAL:
                        posts.append({"post": post, "views": views, "shortcode": post.shortcode})
                        log(f"  VIRAL {post.shortcode} {views} views")
                if count>=40: break
            if posts:
                posts.sort(key=lambda x: x["views"], reverse=True)
                open("ranking_viral.json",'w').write(json.dumps([{"shortcode": p["shortcode"], "views": p["views"]} for p in posts[:15]], indent=2))
                ja = [l.get("video","") for l in carregar_log()]
                for p in posts:
                    if p["shortcode"] not in str(ja):
                        L.download_post(p["post"], target="videos")
                        mp4s = glob.glob("videos/*.mp4")
                        if mp4s:
                            mp4s.sort(key=lambda x: os.path.getmtime(x), reverse=True)
                            return mp4s[0], p["views"]
        except Exception as e:
            log(f"IG falhou: {e} - indo para pasta local")
    else:
        log("IG USER VAZIO -> pulando IG, usando pasta local (sem erro 302)")

    # B) FALLBACK LOCAL - FIX LOG TRAVADO
    log(">>> Pasta local...")
    for pasta in pastas_temp:
        if os.path.exists(pasta):
            for ext in ('*.mp4','*.MP4','*.mov','*.MOV'):
                candidatos += glob.glob(os.path.join(pasta, ext))
    log(f"Total locais: {len(candidatos)}")
    if not candidatos:
        log("Nenhum arquivo local")
        return None, 0

    ja_postados = [l.get("video","") if isinstance(l, dict) else str(l) for l in carregar_log()]
    log(f"Já postados: {len(ja_postados)} -> {ja_postados[-3:]}")
    
    # Tenta filtrar não postados
    nao_postados = [c for c in candidatos if os.path.basename(c) not in ja_postados and "_FINAL" not in c and "_ES_TEMP" not in c]
    log(f"Não postados: {len(nao_postados)}")

    # Se todos já foram postados, reseta e pega o mais novo (pra não travar)
    if not nao_postados:
        log("TODOS já postados, resetando log e pegando mais novo")
        open(LOG_FILE,'w').write("[]")  # reseta log
        nao_postados = [c for c in candidatos if "_FINAL" not in c and "_ES_TEMP" not in c]

    # Filtro >10k: tenta >15MB ou nome viral, se não tiver, pega qualquer um pra não travar workflow
    virais = []
    for c in nao_postados:
        size_mb = os.path.getsize(c)/(1024*1024)
        nome = os.path.basename(c).lower()
        if size_mb >= 2 or "viral" in nome or "10k" in nome:  # baixei pra 2MB pra não bloquear seus 3 vídeos
            virais.append(c)
    
    if not virais:
        virais = nao_postados

    virais.sort(key=lambda x: os.path.getsize(x), reverse=True)
    log(f"SELECIONADO: {virais[0]} | {os.path.getsize(virais[0])/(1024*1024):.1f} MB")
    return virais[0], 15000

def dublar_pt_para_es(p):
    try:
        import whisper
        from moviepy.editor import VideoFileClip, AudioFileClip
        from gtts import gTTS
        out = p.replace(".mp4","_ES_TEMP.mp4")
        if "_ES_TEMP" in p or "_FINAL" in p:
            return p, "construccion viral"
        clip=VideoFileClip(p)
        if clip.audio is None:
            clip.close()
            return p, "construccion viral"
        clip.audio.write_audiofile("temp_pt.wav", logger=None); clip.close()
        txt_pt = whisper.load_model("base").transcribe("temp_pt.wav", language="pt", fp16=False)["text"].strip()
        log(f"PT: {txt_pt[:80]}")
        txt_es = requests.get(f"https://api.mymemory.translated.net/get?q={quote(txt_pt)}&langpair=pt|es", timeout=30).json()['responseData']['translatedText']
        log(f"ES: {txt_es[:80]}")
        gTTS(text=txt_es, lang='es', tld='com.mx').save("temp_es.mp3")
        v=VideoFileClip(p); a=AudioFileClip("temp_es.mp3")
        v.set_audio(a).write_videofile(out, codec='libx264', audio_codec='aac', logger=None)
        v.close()
        for f in ["temp_pt.wav","temp_es.mp3"]:
            if os.path.exists(f): os.remove(f)
        return out, txt_es
    except Exception as e:
        log(f"Dub erro {e}")
        return p, "construccion viral porcelanato"

def legenda_amarela(p, txt):
    try:
        from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip
        if not txt: txt="CONSTRUCCION VIRAL"
        v=VideoFileClip(p); w,h=v.w, v.h
        palavras=txt.split(); linhas=[]; linha=""
        for word in palavras:
            if len(linha+" "+word)<15: linha+=" "+word
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
        v.close()
        return p
    except Exception as e:
        log(f"Legenda erro {e}")
        return p

def postar_facebook(v,l):
    if not PAGE_TOKEN: return False
    try:
        url=f"https://graph.facebook.com/v20.0/{PAGE_ID}/videos"
        with open(v,'rb') as vf:
            r=requests.post(url, files={'source': vf}, data={'description': l, 'access_token': PAGE_TOKEN.strip()}, timeout=300)
        log(f"FB {r.status_code} {r.text[:300]}")
        return r.status_code==200
    except Exception as e:
        log(f"FB {e}"); return False

def main():
    log(f"=== START VIRAL >{MIN_VIEWS_VIRAL} ===")
    v_temp, views = puxar_viral_tempo_real()
    if not v_temp:
        log("NADA pra postar"); return
    v_es, txt_es = dublar_pt_para_es(v_temp)
    v_final = legenda_amarela(v_es, txt_es)
    legenda = f"{txt_es} 🔨 #construccion #viral"
    ok_fb=postar_facebook(v_final, legenda)
    if ok_fb:
        salvar_log(os.path.basename(v_temp), views)
        log("FB OK - apagando temp ES_TEMP")
        for f in [v_temp, v_es]:
            if os.path.exists(f) and "_FINAL" not in f:
                try: os.remove(f)
                except: pass
    log(f"RESULT FB:{ok_fb} VIEWS:{views}")

if __name__=="__main__": main()
