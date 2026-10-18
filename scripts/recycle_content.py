# Automação: Pega 1 Reel por dia e transforma em 3 conteúdos
# 1 Reel Vertical (IG) -> 1 YouTube Short + 1 Título Longo + 1 Post Carrossel

import os

def rotina_reciclagem(reel_path):
    print(f"Processando: {reel_path}")
    # 1. YouTube Short (mesmo vídeo, título otimizado)
    titulo_short = f"{reel_path} - ERRO que custa caro | FC Constrói"
    
    # 2. Vídeo Longo YouTube (compilação de 3 reels do mesmo tema)
    titulo_longo = f"Como fazer BANCADA COM GAVETA do zero - Passo a passo completo"
    
    # 3. Legenda com SEO para YouTube
    descricao = """
    🔗 E-book Bancadas: link
    🔗 Lista de materiais: link
    #construção #bancada #obra
    """
    
    # Salva na fila
    with open(f"content_queue/{reel_path}_youtube.txt", "w", encoding="utf-8") as f:
        f.write(f"{titulo_short}\n{titulo_longo}\n{descricao}")
    
    print(f"✅ Gerado: {titulo_short}")

# Uso diário
# rotina_reciclagem("bancada_001.mp4")
