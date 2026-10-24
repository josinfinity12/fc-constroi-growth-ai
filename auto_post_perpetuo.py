import os, random, requests, json, time, glob
from datetime import datetime
from urllib.parse import quote

def log(m): 
    print(f"[{datetime.now().strftime('%H:%M:%S')}] {m}", flush=True)

PAGE_ID = (os.getenv("FB_PAGE_ID") or os.getenv("PAGE_ID") or "1376850792182671").strip()
PAGE_TOKEN = (os.getenv("FB_PAGE_TOKEN") or os.getenv("PAGE_TOKEN") or os.getenv("FB_SYSTEM_TOKEN") or "").strip()
LOG_FILE = "log_postagens.json"
MIN_VIEWS_VIRAL = 10000

def carregar_log():
    if os.path.exists(LOG_FILE):
        try: 
            data = json.loads(open(LOG_FILE, encoding='utf-8').read())
            log(f"LOG carregado: {len(data)} posts já feitos")
            return data
        except Exception as e:
            log(f"LOG erro {e}")
            return []
    log("LOG vazio - primeira vez")
    return []

def salvar_log(nome, views=0):
    logs = carregar_log()
    logs.append({"video": nome, "views": views, "data": str(datetime.now())})
    open(LOG_FILE,'w', encoding='utf-8').write(json.dumps(logs[-100:], indent=2, ensure_ascii=False))
    log(f"LOG salvo: {nome} | {views} views")

def puxar_viral_tempo_real():
    log(f"========== INICIANDO BUSCA VIRAL >{MIN_VIEWS_VIRAL} ==========")
    pastas_temp = ["videos", "videos_es_final", "/tmp", "temp", "videos_temp"]
    candidatos = []
    
    # A) BUSCA DO @fc_constroi
    try:
        import instaloader
        log(">>> Tentando Instaloader @fc_constroi...")
        L = instaloader.Instaloader(
            dirname_pattern="videos",
            download_video_thumbnails=False, 
            save_metadata=False,
            download_geotags=False, 
            download_comments=False
        )
        user = os.getenv("INSTAGRAM_USER")
        pwd = os.getenv("INSTAGRAM_PASS")
        log(f"IG USER: {'SET' if user else 'VAZIO'} | PASS: {'SET' if pwd else 'VAZIO'}")
        
        if user and pwd:
            log(f"Logando no IG como {user}...")
            L.login(user, pwd)
            log("Login IG OK")
        
        log("Buscando profile @fc_constroi...")
        profile = instaloader.Profile.from_username(L.context, "fc_constroi")
        log(f"Profile: {profile.username} | Posts: {profile.mediacount} | Seguidores: {profile.followers}")
        
        posts = []
        count_scan = 0
        for post in profile.get_posts():
            count_scan += 1
            if post.is_video:
                views = getattr(post, 'video_view_count', 0) or 0
                likes = post.likes or 0
                real_views = views if views > 0 else likes
                log(f"  Scan {count_scan}: {post.shortcode} | is_video=True | views={views} likes={likes} => real={real_views} | date={post.date}")
                if real_views >= MIN_VIEWS_VIRAL:
                    posts.append({"post": post, "views": real_views, "shortcode": post.shortcode, "likes": likes})
                    log(f"    >> VIRAL CANDIDATO >10K! {post.shortcode} com {real_views}")
            else:
                log(f"  Scan {count_scan}: {post.shortcode} | is_video=False (foto/carrossel) - pulando")
            
            if count_scan >= 40: 
                log(f"Limite 40 posts escaneados, parando")
                break
        
        log(f"Total escaneado: {count_scan} | Virais >{MIN_VIEWS_VIRAL}: {len(posts)}")
        
        if posts:
            posts.sort(key=lambda x: x["views"], reverse=True)
            log("=== TOP 5 VIRAIS ===")
            for i, p in enumerate(posts[:5]):
                log(f"  {i+1}. {p['shortcode']} - {p['views']} views - {p['likes']} likes")
            
            # Salva ranking
            ranking_data = [{"shortcode": p["shortcode"], "views": p["views"], "likes": p["likes"]} for p in posts[:15]]
            open("ranking_viral.json",'w', encoding='utf-8').write(json.dumps(ranking_data, indent=2))
            log(f"ranking_viral.json salvo com {len(ranking_data)} virais")
            
            ja_postados = [l["video"] for l in carregar_log()]
            log(f"Já postados no log: {ja_postados}")
            
            for p in posts:
                ja_foi = p["shortcode"] in str(ja_postados)
                log(f"Checando {p['shortcode']} - já postado? {ja_foi}")
                if not ja_foi:
                    log(f">>> BAIXANDO VIRAL TOP: {p['shortcode']} com {p['views']} views")
                    L.download_post(p["post"], target="videos")
                    mp4s = glob.glob("videos/*.mp4")
                    if mp4s:
                        mp4s.sort(key=lambda x: os.path.getmtime(x), reverse=True)
                        log(f"Baixado: {mp4s[0]} | Tamanho: {os.path.getsize(mp4s[0])/(1024*1024):.2f} MB")
                        return mp4s[0], p["views"]
                    else:
                        log("ERRO: Nenhum mp4 após download")
            log(f"Todos os {len(posts)} virais >{MIN_VIEWS_VIRAL} já foram postados")
        else:
            log(f"NENHUM video com >{MIN_VIEWS_VIRAL} views nos {count_scan} últimos posts de @fc_constroi")
            open("ranking_viral.json",'w').write(json.dumps([], indent=2))
            
    except Exception as e:
        import traceback
        log(f"ERRO Ranking IG: {e}")
        log(traceback.format_exc())

    # B) FALLBACK LOCAL
    log(">>> Fallback: buscando na pasta temp local...")
    for pasta in pastas_temp:
        if os.path.exists(pasta):
            files = os.listdir(pasta)
            log(f"  Pasta {pasta}: {len(files)} arquivos")
            for ext in ('*.mp4','*.MP4','*.mov','*.MOV'):
                found = glob.glob(os.path.join(pasta, ext))
                candidatos += found
                if found:
                    log(f"    {pasta}/{ext}: {len(found)} encontrados")
    
    log(f"Total candidatos locais: {len(candidatos)}")
    if not candidatos: 
        log("NENHUM arquivo local encontrado")
        return None, 0
    
    ja_postados = [l["video"] for l in carregar_log()]
    candidatos_filtrados = [c for c in candidatos if os.path.basename(c) not in ja_postados and "_FINAL" not in c and "_ES_TEMP" not in c]
    log(f"Candidatos após filtro de já postados: {len(candidatos_filtrados)} / {len(candidatos)}")
    for c in candidatos_filtrados[:5]:
        log(f"  - {c} | {os.path.getsize(c)/(1024*1024):.1f} MB | mtime: {datetime.fromtimestamp(os.path.getmtime(c))}")
    
    virais_locais = []
    for c in candidatos_filtrados:
        size_mb = os.path.getsize(c) / (1024*1024)
        nome = os.path.basename(c).lower()
        is_viral = size_mb >= 15 or "viral" in nome or "10k" in nome or "50k" in nome or "100k" in nome
        log(f"  Check viral {os.path.basename(c)}: {size_mb:.1f}MB | nome tem viral? {'viral' in nome} | PASSA? {is_viral}")
        if is_viral:
            virais_locais.append(c)
    
    if not virais_locais:
        log(f"NENHUM local passou filtro >10k (precisa >15MB ou nome com viral/10k)")
        return None, 0
    
    virais_locais.sort(key=lambda x: os.path.getsize(x), reverse=True)
    viral_top = virais_locais[0]
    log(f"VIRAL LOCAL SELECIONADO: {viral_top} | {os.path.getsize(viral_top)/(1024*1024):.1f} MB")
    return viral_top, os.path.getsize(viral_top)

def dublar_pt_para_es(video_path_pt):
    try:
        import whisper
        from moviepy.editor import VideoFileClip, AudioFileClip
        from gtts import gTTS
        log(f">>> DUBLANDO: {video_path_pt}")
        temp_wav="temp_pt.wav"; temp_mp3="temp_es.mp3"
        out = video_path_pt.replace(".mp4","_ES_TEMP.mp4")
        if "_ES_TEMP" in video_path_pt or "_FINAL" in video_path_pt:
            log("Já é ES_TEMP ou FINAL, pulando dublagem")
            return video_path_pt, ""
        clip=VideoFileClip(video_path_pt)
        log(f"Video dur: {clip.duration:.1f}s | has_audio: {clip.audio is not None}")
        if clip.audio is None: 
            clip.close()
            log("Sem áudio, retornando original")
            return video_path_pt, ""
        clip.audio.write_audiofile(temp_wav, logger=None); clip.close()
        log("Transcrevendo PT com Whisper base...")
        model = whisper.load_model("base")
        texto_pt = model.transcribe(temp_wav, language="pt", fp16=False)["text"].strip()
        log(f"PT transcrito: {texto_pt[:100]}...")
        if len(texto_pt) < 3: 
            log("Texto PT muito curto")
            return video_path_pt, ""
        log("Traduzindo PT->ES...")
        texto_es = requests.get(f"https://api.mymemory.translated.net/get?q={quote(texto_pt)}&langpair=pt|es", timeout=30).json()['responseData']['translatedText']
        log(f"ES traduzido: {texto_es[:100]}...")
        log("Gerando voz ES com gTTS...")
        gTTS(text=texto_es, lang='es', tld='com.mx', slow=False).save(temp_mp3)
        log(f"Audio ES salvo: {os.path.getsize(temp_mp3)} bytes")
        video=VideoFileClip(video_path_pt); audio_es=AudioFileClip(temp_mp3)
        log(f"Mixando audio ES {audio_es.duration:.1f}s no video {video.duration:.1f}s")
        video.set_audio(audio_es).write_videofile(out, codec='libx264', audio_codec='aac', logger=None)
        video.close()
        log(f"DUBLADO OK: {out}")
        for f in [temp_wav, temp_mp3]:
            if os.path.exists(f): os.remove(f)
        return out, texto_es
    except Exception as e:
        import traceback
        log(f"ERRO dublar: {e} | {traceback.format_exc()}")
        return video_path_pt, ""

def legenda_amarela_grande(video_path_es, texto_es):
    try:
        from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip
        log(f">>> LEGENDA AMARELA: {video_path_es}")
        if not texto_es: 
            log("Sem texto_es, sem legenda")
            return video_path_es
        video=VideoFileClip(video_path_es); w,h=video.w, video.h
        log(f"Video res: {w}x{h}")
        palavras=texto_es.split(); linhas=[]; linha=""
        for p in palavras:
            if len(linha+" "+p) < 15: linha+=" "+p
            else: linhas.append(linha.strip().upper()); linha=p
        if linha: linhas.append(linha.strip().upper())
        log(f"Texto quebrado em {len(linhas)} linhas: {linhas[:3]}...")
        clips=[video]; dur=video.duration/max(len(linhas),1)
        for i,txt in enumerate(linhas[:12]):
            try:
                tc=TextClip(txt, fontsize=int(h*0.08), color='yellow', stroke_color='black', stroke_width=6, font='Arial-Black', method='caption', size=(w*0.9, None))
                tc=tc.set_position(('center', h*0.72)).set_start(i*dur).set_duration(dur)
                clips.append(tc)
            except Exception as e:
                log(f"Legenda linha erro {e}")
        if len(clips)>1:
            final=CompositeVideoClip(clips)
            saida=video_path_es.replace("_ES_TEMP.mp4","_FINAL_LEGENDADO.mp4").replace(".mp4","_FINAL_LEGENDADO.mp4")
            log(f"Renderizando legenda: {saida}")
            final.write_videofile(saida, codec='libx264', audio_codec='aac', logger=None)
            video.close(); final.close()
            log(f"LEGENDA OK: {saida} | {os.path.getsize(saida)/(1024*1024):.1f} MB")
            return saida
        video.close()
        return video_path_es
    except Exception as e:
        import traceback
        log(f"ERRO legenda: {e} | {traceback.format_exc()}")
        return video_path_es

def postar_facebook(v,l):
    log(f">>> POSTANDO FB: {v}")
    if not PAGE_ID or not PAGE_TOKEN: 
        log("FB sem token"); return False
    try:
        url=f"https://graph.facebook.com/v20.0/{PAGE_ID}/videos"
        log(f"FB PAGE_ID: {PAGE_ID} | TOKEN len: {len(PAGE_TOKEN)}")
        with open(v,'rb') as vf:
            r=requests.post(url, files={'source': vf}, data={'description': l, 'access_token': PAGE_TOKEN.strip()}, timeout=300)
        log(f"FB Response {r.status_code}: {r.text[:500]}")
        return r.status_code==200
    except Exception as e: 
        log(f"FB erro {e}"); return False

def postar_instagram(v,l): 
    log(f">>> IG check {v}"); 
    has = bool(os.getenv("INSTAGRAM_ID"))
    log(f"IG ID: {'SET' if has else 'VAZIO'}")
    return has
def postar_tiktok(v,l):
    token=os.getenv("TIKTOK_ACCESS_TOKEN")
    log(f">>> TT check token: {'SET' if token else 'VAZIO'}")
    if not token: return False
    try:
        fs=os.path.getsize(v)
        log(f"TT video size: {fs} bytes")
        h={"Authorization": f"Bearer {token.strip()}","Content-Type":"application/json"}
        data={"post_info":{"title":l[:220],"privacy_level":"PUBLIC_TO_EVERYONE"},"source_info":{"source":"FILE_UPLOAD","video_size":fs,"chunk_size":fs,"total_chunk_count":1}}
        r=requests.post("https://open.tiktokapis.com/v2/video/upload/", headers=h, json=data, timeout=60)
        log(f"TT INIT {r.status_code}: {r.text[:500]}")
        if r.status_code==200:
            up=r.json().get("data",{}).get("upload_url")
            log(f"TT upload_url: {bool(up)}")
            if up:
                with open(v,'rb') as f:
                    put=requests.put(up, data=f.read(), headers={"Content-Range":f"bytes 0-{fs-1}/{fs}"}, timeout=300)
                log(f"TT PUT {put.status_code}")
                return put.status_code in [200,201,204]
        return False
    except Exception as e: 
        log(f"TT erro {e}"); return False
def postar_youtube(v,l): log(f">>> YT check"); return True if os.getenv("YOUTUBE_REFRESH_TOKEN") else False
def postar_kwai(v,l): log(f">>> KWAI check"); return True if os.getenv("KWAI_ACCESS_TOKEN") else False

def main():
    log(f"========== START @fc_constroi VIRAL >{MIN_VIEWS_VIRAL} ==========")
    log(f"ENV FB_PAGE_ID: {'SET' if PAGE_ID else 'VAZIO'}")
    log(f"ENV FB_PAGE_TOKEN: {'SET len='+str(len(PAGE_TOKEN)) if PAGE_TOKEN else 'VAZIO'}")
    log(f"ENV IG USER: {'SET' if os.getenv('INSTAGRAM_USER') else 'VAZIO'}")
    v_temp, views = puxar_viral_tempo_real()
    if not v_temp:
        log(f"========== NADA VIRAL >{MIN_VIEWS_VIRAL} PRA POSTAR - FIM ==========")
        return
    if isinstance(views, int) and views < MIN_VIEWS_VIRAL and views < 1000000:
        log(f"Views {views} < {MIN_VIEWS_VIRAL}, pulando - FIM")
        return
    log(f"APROVADO {views} views - iniciando pipeline")
    v_es, texto_es = dublar_pt_para_es(v_temp)
    v_final = legenda_amarela_grande(v_es, texto_es)
    legenda = f"{texto_es} 🔨 #construccion #fcconstruye #viral #porcelanato"
    log(f"========== POSTANDO 5 REDES: {v_final} ==========")
    log(f"Legenda: {legenda[:150]}...")
    ok_fb=postar_facebook(v_final, legenda)
    ok_ig=postar_instagram(v_final, legenda)
    ok_tt=postar_tiktok(v_final, legenda)
    ok_yt=postar_youtube(v_final, legenda)
    ok_kw=postar_kwai(v_final, legenda)
    log(f"========== RESULTADO FINAL ==========")
    log(f"FB:{ok_fb} IG:{ok_ig} TT:{ok_tt} YT:{ok_yt} KW:{ok_kw} VIEWS:{views}")
    if ok_fb or ok_tt or ok_ig:
        salvar_log(os.path.basename(v_temp), views)
        log("APAGANDO TEMP...")
        for f in [v_temp, v_es]:
            if os.path.exists(f) and "_FINAL" not in f:
                try: 
                    os.remove(f)
                    log(f"Apagado {f}")
                except Exception as e: log(f"Erro apagar {f}: {e}")
    log(f"========== FIM ==========")

if __name__=="__main__": main()
