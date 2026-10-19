from PIL import Image, ImageDraw, ImageFont

LARANJA = "#FF8C1A"
GRAFITE = "#2F2F33"
COBRE = "#B87A4B"
BRANCO = "#FFFFFF"

def gerar_thumbnail(modelo="choque", texto_gancho="BANCADA EM PORCELANATO", preco="R$99,90", preco_remarketing="R$49,90"):
    W, H = 1080, 1920
    img = Image.new("RGB", (W, H), GRAFITE)
    draw = ImageDraw.Draw(img)
    try:
        font_giant = ImageFont.truetype("DejaVuSans-Bold.ttf", 110)
        font_big = ImageFont.truetype("DejaVuSans-Bold.ttf", 85)
        font_med = ImageFont.truetype("DejaVuSans-Bold.ttf", 55)
        font_small = ImageFont.truetype("DejaVuSans-Bold.ttf", 38)
    except:
        font_giant = ImageFont.load_default()
        font_big = font_giant
        font_med = font_giant
        font_small = font_giant

    if modelo == "choque":
        draw.rectangle([0, 0, W, 650], fill=COBRE)
        draw.text((50, 60), texto_gancho.upper(), fill=BRANCO, font=font_big)
        draw.text((50, 300), "EM PORCELANATO", fill=BRANCO, font=font_med)
        draw.text((50, 380), "SOB MEDIDA!", fill=LARANJA, font=font_giant)
        draw.rectangle([0, H-450, W, H-200], fill=BRANCO)
        draw.text((50, H-400), f"DE {preco_remarketing}", fill=GRAFITE, font=font_med)
        draw.text((50, H-340), f"POR {preco}", fill=LARANJA, font=font_giant)
        draw.rectangle([0, H-200, W, H], fill=LARANJA)
        draw.text((50, H-130), "PIA | BANCADA | CLOSET | NICHO", fill=BRANCO, font=font_small)
    elif modelo == "antes_depois":
        draw.rectangle([0, 0, W, H//2], fill="#4A4A4A")
        draw.text((50, 250), "MDF COMUM", fill=BRANCO, font=font_med)
        draw.rectangle([0, H//2, W, H], fill=BRANCO)
        draw.text((50, 1000), "PORCELANATO FC", fill=GRAFITE, font=font_med)
        draw.rectangle([0, H//2-90, W, H//2+90], fill=LARANJA)
        draw.text((50, H//2-40), texto_gancho.upper()[:22], fill=BRANCO, font=font_med)
    else:  # preco - FUNDO BRANCO LIMPO
        draw.rectangle([0, 0, W, H], fill=BRANCO)
        draw.text((50, 80), texto_gancho.upper(), fill=GRAFITE, font=font_big)
        draw.text((50, 250), "100% EM PORCELANATO", fill=GRAFITE, font=font_med)
        draw.text((50, 760), preco, fill=LARANJA, font=font_giant)
        draw.text((50, 900), f"REMARKETING {preco_remarketing}", fill=GRAFITE, font=font_med)
        draw.rectangle([0, H-250, W, H], fill=GRAFITE)
        draw.text((50, H-160), "COMENTA: BANCADA", fill=LARANJA, font=font_med)
    
    img.save(f"thumb_{modelo}.png")
    return f"thumb_{modelo}.png"

def gerar_todos_modelos(texto_gancho, preco="R$99,90", preco_remarketing="R$49,90"):
    return [gerar_thumbnail(m, texto_gancho, preco, preco_remarketing) for m in ["choque","antes_depois","preco"]]
