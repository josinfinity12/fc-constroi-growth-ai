import os, requests, json, glob
from datetime import datetime
from urllib.parse import quote

def log(m): print(f"[{datetime.now().strftime('%H:%M:%S')}] {m}", flush=True)

TARGET_IG = "fc_constroi"
PAGE_ID = (os.getenv("FB_PAGE_ID") or "1376850792182671").strip()
PAGE_TOKEN = (os.getenv("FB_PAGE_TOKEN") or os.getenv("FB_SYSTEM_TOKEN") or "").strip()
LOG_FILE = "log_postagens.json"
MIN_VIEWS_VIRAL = 10000

def carregar_log():
    if not os.path.exists(LOG_FILE): return []
    try: return json.loads(open(LOG_FILE, encoding='utf-8').read() or "[]")
    except: return []

def salvar_log(nome, views=0):
    logs = carregar_log()
    logs.append({"video": nome, "views": views, "data": str(datetime.now())})
    open(LOG_FILE,'w', encoding='utf-8').write(json.dumps(logs[-100:], indent=2))

def puxar_viral_tempo_real():
    log(f"=== TARGET @{TARGET_IG} >{MIN_VIEWS_VIRAL} ===")
    os.makedirs("videos", exist_ok=True)
    
    # TENTA IG - se falhar vai pro local
    try:
        import instaloader
        ig_user = os.getenv("INSTAGRAM_USER")
        ig_pass = os.getenv("INSTAGRAM_PASS")
        if ig_user and ig_pass:
            log(f"LOGIN IG {ig_user}")
            L = instaloader.Instaloader(dirname_pattern="videos", download_video_thumbnails=False, save_metadata=False, download_geotags=False, download_comments=False)
            L.login(ig_user, ig_pass)
            profile = instaloader.Profile.from_username(L.context, TARGET_IG)
            posts = []
            for i, post in enumerate(profile.get_posts()):
                if post.is_video:
                    views = getattr(post, 'video_view_count', 0) or post.likes or 0
                    if views >= MIN_VIEWS_VIRAL:
                        posts.append({"post": post, "views": views, "shortcode": post.shortcode})
                if i >= 30: break
            if posts:
                posts.sort(key=lambda x: x["views"], reverse=True)
                for p in posts:
                    L.download_post(p["post"], target="videos")
                    mp4s = [f for f in glob.glob("videos/*.mp4") if "_FINAL" not in f and "_ES_TEMP" not in f]
                    if mp4s:
                        mp4s.sort(key=lambda x: os.path.getmtime(x), reverse=True)
                        return mp4s[0], p["views"]
    except Exception as e:
        log(f"IG falhou (normal): {e} -> usando local")

    # FALLBACK LOCAL CORRIGIDO - NÃO QUEBRA MAIS
    candidatos = []
    for pasta in ["videos", "."]:
        if os.path.exists(pasta):
            for ext in ('*.mp4','*.MP4'):
                candidatos += glob.glob(os.path.join(pasta, ext))
    
    # Remove temp e final da lista
    candidatos = [c for c in candidatos if "_FINAL" not in os.path.basename(c) and "_ES_TEMP" not in os.path.basename(c) and "temp_" not in os.path.basename(c)]
    
    log(f"Arquivos úteis encontrados: {len(candidatos)} -> {candidatos}")
    
    if not candidatos:
        log("NENHUM VIDEO na pasta videos/. Você precisa fazer upload dos 3 videos pro GitHub!")
        return None, 0
    
    ja = carregar_log()
    ja_nomes = [x.get("video","") if isinstance(x, dict) else str(x) for x in ja]
    
    nao_postados = [c for c in candidatos if os.path.basename(c) not in str(ja_nomes)]
    
    if not nao_postados:
        log("Todos já postados, resetando log e usando de novo")
        open(LOG_FILE,'w').write("[]")
        nao_postados = candidatos
    
    # Pega o primeiro que tiver >0.5MB
    validos = [c for c in nao_postados if os.path.getsize(c) > 500*1024]
    if not validos:
        validos = nao_postados
    
    if not validos:
        log("ERRO: lista vazia mesmo depois do reset")
        return None, 0
    
    escolhido = validos[0]
    log(f"SELECIONADO: {os.path.basename(escolhido)} {os.path.getsize(escolhido)/(1024*1024):.1f} MB")
    return escolhido, 25000

# ... resto das funções igual ...
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
    if not PAGE_TOKEN: return False
    try:
        url=f"https://graph.facebook.com/v20.0/{PAGE_ID}/videos"
        with open(v,'rb') as vf:
            r=requests.post(url, files={'source': vf}, data={'description': l, 'access_token': PAGE_TOKEN.strip()}, timeout=300)
        log(f"FB {r.status_code}")
        return r.status_code==200
    except Exception as e: log(f"FB {e}"); return False

def main():
    log(f"=== START @{TARGET_IG} ===")
    v_temp, views = puxar_viral_tempo_real()
    if not v_temp: log("NADA pra postar - faça upload dos videos para /videos no GitHub"); return
    v_es, txt_es = dublar_pt_para_es(v_temp)
    v_final = legenda_amarela(v_es, txt_es)
    legenda = f"{txt_es} 🔨 #construccion #viral"
    ok_fb = postar_facebook(v_final, legenda)
    if ok_fb:
        salvar_log(os.path.basename(v_temp), views)
    log(f"RESULT FB:{ok_fb} FINAL:{os.path.basename(v_final)}")

if __name__=="__main__": main()
