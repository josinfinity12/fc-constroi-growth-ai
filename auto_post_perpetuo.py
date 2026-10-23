# auto_post_perpetuo.py v5.1 FIX - roda no Actions
import os, subprocess, json, random, datetime, requests
from pathlib import Path

OUTPUT_DIR = "/tmp/fc_perpetuo"
os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs("videos_es_final", exist_ok=True)

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
        print(f"yt-dlp: {e}")
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
        print(f"✅ {final_path}")
    except Exception as e:
        print(f"Erro montar: {e}")
        Path(final_path).touch()
    return final_path

def main():
    print(f"🚀 INICIANDO {datetime.datetime.now()}")
    for reel in puxar_3_reels_reais():
        titulo_es = gerar_es(reel['title'])
        legenda = f"{titulo_es}\n\nComenta YO QUIERO\n\n#construccion #fc_construye"
        montar_final_9x16(reel['id'], titulo_es)
        print(f"Legenda: {legenda}")
    print("🎉 FIM CICLO")

if __name__ == "__main__":
    main()
