# auto_post_perpetuo.py v5.2 FIX - CRIA E POSTA AUTOMATICO NA PAGINA 61595702674802
import os, subprocess, json, random, datetime, requests
from pathlib import Path

OUTPUT_DIR = "/tmp/fc_perpetuo"
os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs("videos_es_final", exist_ok=True)

PAGE_ID = os.getenv("PAGE_ID", "61595702674802")
PAGE_TOKEN = os.getenv("PAGE_TOKEN", "")
LOG_FILE = "log_postagens.json"

def log(msg):
    print(f"[{datetime.datetime.now().strftime('%H:%M:%S')}] {msg}", flush=True)

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
    if "gaveta" in titulo_pt.lower(): return "¿GAVETA PORCELANATO SE ROMPIÓ? Evita pérdida de $8000"
    if "nivel" in titulo_pt.lower() or "parede" in titulo_pt.lower(): return "¿PARED DESNIVELADA? 100% nivelada sin burbuja"
    return "¿JUNTA MANCHADA? Junta que NO se mancha 10 años"

def montar_final_9x16(reel_id, titulo_es):
    final_path = f"videos_es_final/{reel_id}_FINAL_ES_9x16.mp4"
    try:
        from moviepy.editor import ColorClip, TextClip, CompositeVideoClip
        from gtts import gTTS
        audio_path = f"{OUTPUT_DIR}/{reel_id}_es.mp3"
        gTTS(text=titulo_es, lang='es').save(audio_path)
        clip = ColorClip(size=(1080,1920), color=(15,15,15), duration=8)
        txt = TextClip(titulo_es, fontsize=55, color='white', bg_color='black', size=(900,400), method='caption').set_duration(8).set_position('center')
        final = CompositeVideoClip([clip, txt])
        from moviepy.editor import AudioFileClip
        if os.path.exists(audio_path):
            final = final.set_audio(AudioFileClip(audio_path))
        final.write_videofile(final_path, fps=24, codec="libx264", audio_codec="aac", logger=None)
        final.close()
        log(f"✅ {final_path}")
    except Exception as e:
        log(f"Erro montar: {e}")
        Path(final_path).touch()
    return final_path

def postar_na_pagina_61595702674802(video_path, legenda):
    """POSTA AUTOMATICO NA FC CONSTRUYE"""
    if not PAGE_TOKEN:
        log("❌ ERRO: PAGE_TOKEN vazio! Vai em Settings > Secrets > PAGE_TOKEN")
        return False
    
    if not os.path.exists(video_path):
        log(f"Video nao existe: {video_path}")
        return False
    
    size = os.path.getsize(video_path)
    log(f"Postando {video_path} ({size} bytes) na pagina {PAGE_ID}")

    # Se video placeholder < 10KB, posta como texto
    if size < 10000:
        url = f"https://graph.facebook.com/v20.0/{PAGE_ID}/feed"
        r = requests.post(url, data={"message": legenda, "access_token": PAGE_TOKEN}, timeout=30)
        log(f"FB FEED {r.status_code}: {r.text[:500]}")
        return r.status_code == 200

    # Video real
    url = f"https://graph.facebook.com/v20.0/{PAGE_ID}/videos"
    try:
        with open(video_path, 'rb') as f:
            files = {'source': f}
            data = {'description': legenda, 'access_token': PAGE_TOKEN}
            r = requests.post(url, files=files, data=data, timeout=180)
            log(f"FB VIDEO {r.status_code}: {r.text[:800]}")
            if r.status_code == 200:
                log(f"✅ VIDEO POSTADO NA PAGINA 61595702674802! ID {r.json().get('id')}")
                return True
            else:
                # fallback
                url2 = f"https://graph.facebook.com/v20.0/{PAGE_ID}/feed"
                r2 = requests.post(url2, data={"message": legenda, "access_token": PAGE_TOKEN}, timeout=30)
                log(f"Fallback FEED {r2.status_code}: {r2.text[:500]}")
                return r2.status_code == 200
    except Exception as e:
        log(f"Exception postar: {e}")
        return False

def main():
    log(f"🚀 INICIANDO {datetime.datetime.now()}")
    log(f"PAGE_ID {PAGE_ID} | TOKEN {'OK' if PAGE_TOKEN else 'VAZIO'}")
    
    db = {"total_posts": 0}
    if os.path.exists(LOG_FILE):
        try:
            with open(LOG_FILE, "r") as f: db = json.load(f)
        except: pass

    for reel in puxar_3_reels_reais():
        titulo_es = gerar_es(reel['title'])
        legenda = f"{titulo_es}\n\nComenta YO QUIERO\n\n#construccion #fc_construye\n📲 Fc Construye - El Salvador - {datetime.datetime.now().strftime('%d/%m/%Y')}"
        video_path = montar_final_9x16(reel['id'], titulo_es)
        log(f"Legenda: {legenda}")

        # AQUI POSTA AUTOMATICO
        ok = postar_na_pagina_61595702674802(video_path, legenda)
        if ok:
            log("✅ POSTADO COM SUCESSO NA FC CONSTRUYE")
            db["total_posts"] = db.get("total_posts", 0) + 1
        else:
            log("❌ Falha ao postar")
        
        time.sleep(3) # pausa entre posts

    with open(LOG_FILE, "w", encoding="utf-8") as f:
        json.dump(db, f, indent=2, ensure_ascii=False)
    
    log("🎉 FIM CICLO - 5 plataformas ES estrutura pronta")

if __name__ == "__main__":
    import time
    main()
