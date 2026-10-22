# v7.2 FIX TOTAL - @fc_constroi - SEM ERRO DE SINTAXE
import argparse, subprocess, random, shutil
from pathlib import Path

BASE_DIR = Path(__file__).parent
OUTPUT_DIR = BASE_DIR / "output"
OUTPUT_CURSO = OUTPUT_DIR / "CURSO_NACIONAL"
OUTPUT_OBRA = OUTPUT_DIR / "OBRAS_LOCAL"
OUTPUT_REJEITADO = OUTPUT_DIR / "_REJEITADOS_CURIOSOS"
VIDEOS_DIR = BASE_DIR / "videos_brutos"
CONFIG_DIR = BASE_DIR / "config"
for p in [OUTPUT_DIR, OUTPUT_CURSO, OUTPUT_OBRA, OUTPUT_REJEITADO, VIDEOS_DIR, CONFIG_DIR]:
    p.mkdir(exist_ok=True)

CIDADES_LOCAL_RAIO = ["Santanopolis", "Irara", "Feira de Santana", "Serrinha", "Ouricangas", "Santa Barbara", "Tanquinho", "Coracao de Maria"]

BLACKLIST_CURIOSOS = [
    "de onde vc e", "onde vc mora", "vc e de onde", "moro em fortaleza", 
    "moro em sao paulo", "tem alguem aqui em", "atende em", "vc vem pra",
    "qual disco", "qual ferramenta", "que disco usa", "passo a passo gratis",
    "manda o passo a passo", "ensina de graca", "pdf", "apostila gratis",
    "deve custar um rim", "muito caro", "nao tenho dinheiro", "um dia eu faco",
    "sonho", "quando eu tiver casa", "pinterest", "so inspiracao",
    "curso gratis", "de graca", "gratis", "0800", "free", "vazado",
    "meme", "dancinha", "trend", "humor", "engracado", "fofoca", "asmr",
    "satisfatorio", "receita", "futebol", "politica",
    "nao presta", "golpe", "fraude", "enganacao"
]

WHITELIST_CURSO = ["curso", "academia", "aprenda", "tecnica", "fature", "renda extra", "pia esculpida", "nicho", "90x90", "fc constroi"]
WHITELIST_OBRA = ["orcamento", "m2", "quanto custa", "obra", "pedreiro", "instalacao", "feira", "irara", "serrinha"]

def detectar_idioma(texto):
    t = texto.lower()
    if any(p in t for p in ["how to build", "my house tour", "free course", "como hacer"]):
        return False, "Idioma estrangeiro"
    return True, "PT OK"

def is_curioso(texto):
    txt = texto.lower()
    for palavra in BLACKLIST_CURIOSOS:
        if palavra in txt:
            return True, f"CURIOSO: {palavra}"
    return False, "OK"

def classificar_funil(titulo, descricao, cidade_param):
    texto_full = f"{titulo} {descricao} {cidade_param}".lower()
    ok_idioma, motivo = detectar_idioma(texto_full)
    if not ok_idioma:
        return None, None, motivo
    eh_curioso, motivo = is_curioso(texto_full)
    if eh_curioso:
        if any(k in texto_full for k in WHITELIST_CURSO):
            pass
        else:
            return None, None, motivo
    cidade_encontrada = None
    for cid in CIDADES_LOCAL_RAIO:
        if cid.lower() in texto_full:
            cidade_encontrada = cid
            break
    if cidade_encontrada:
        return "OBRAS_LOCAL", cidade_encontrada, "OK LOCAL"
    return "CURSO_NACIONAL", "nacional", "OK NACIONAL"

def baixar_do_instagram(url):
    print(f"\nBAIXANDO: {url}")
    if "COLE_SEU_LINK" in url or "XXXX" in url:
        print("Link fake! Use link real do seu Reels")
        return None, "", ""
    try:
        out = str(VIDEOS_DIR / "%(title).30s.%(ext)s")
        cmd = ["yt-dlp", url, "-o", out, "--merge-output-format", "mp4", "--no-playlist", "--write-description"]
        subprocess.run(cmd, check=True, capture_output=True)
        vids = sorted(VIDEOS_DIR.glob("*.mp4"), key=lambda x: x.stat().st_mtime, reverse=True)
        if not vids:
            return None, "", ""
        video_path = str(vids[0])
        desc_file = Path(video_path).with_suffix('.description')
        descricao = desc_file.read_text(encoding='utf-8', errors='ignore')[:500] if desc_file.exists() else ""
        titulo = Path(video_path).stem
        print(f"Baixado: {Path(video_path).name}")
        return video_path, titulo, descricao
    except Exception as e:
        print(f"Erro: {e}")
        return None, "", ""

def gerar_com_filtro(video_path, titulo, descricao, cidade_param):
    funil, cidade_real, motivo = classificar_funil(titulo, descricao, cidade_param)
    if funil is None:
        print(f"REJEITADO: {motivo} | {Path(video_path).name}")
        shutil.copy2(video_path, OUTPUT_REJEITADO / Path(video_path).name)
        (OUTPUT_REJEITADO / f"{Path(video_path).stem}_MOTIVO.txt").write_text(f"Motivo: {motivo}\nTitulo: {titulo}\nDesc: {descricao[:200]}", encoding='utf-8')
        return
    print(f"APROVADO: {funil} | {cidade_real}")
    pasta_destino = OUTPUT_CURSO if funil == "CURSO_NACIONAL" else OUTPUT_OBRA
    for rede in ["instagram", "facebook", "youtube", "tiktok", "kwai"]:
        nome_limpo = "".join(c if c.isalnum() else "_" for c in Path(video_path).stem[:20])
        saida = pasta_destino / f"{rede}_{cidade_real.lower().replace(' ','_')}_{nome_limpo}.mp4"
        shutil.copy2(video_path, saida)
        legenda = f"FUNIL: {funil}\nCIDADE: {cidade_real}\nTITULO: {titulo}\nFILTRO: {motivo}\nDESC: {descricao[:150]}\n"
        saida.with_suffix('.txt').write_text(legenda, encoding='utf-8')
        print(f"  {rede}: {saida.name}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--instagram", default="")
    parser.add_argument("--cidade", default="nacional")
    parser.add_argument("--lote", action="store_true")
    args = parser.parse_args()

    if args.lote:
        links_file = CONFIG_DIR / "links_instagram.txt"
        if not links_file.exists():
            links_file.write_text("# Cole 1 link por linha\nhttps://www.instagram.com/reel/XXXX\n", encoding='utf-8')
            print(f"Criei {links_file} - Cole seus links la")
        else:
            links = [l.strip() for l in links_file.read_text(encoding='utf-8').splitlines() if l.strip() and not l.startswith("#")]
            print(f"LOTE: {len(links)} videos")
            for url in links:
                v, titulo, desc = baixar_do_instagram(url)
                if v:
                    gerar_com_filtro(v, titulo, desc, args.cidade)
    elif args.instagram:
        v, titulo, desc = baixar_do_instagram(args.instagram)
        if v:
            gerar_com_filtro(v, titulo, desc, args.cidade)
    else:
        print("Uso: python criador-de-conteudo.py --instagram LINK --cidade Irara")
        print("Ou: python criador-de-conteudo.py --lote --cidade nacional")
        
        

        
