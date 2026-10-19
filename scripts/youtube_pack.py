import re

CIDADES_SERVICO = ["santanopolis", "irara", "feira de santana", "agua fria", "ouricanga", "santa barbara", "serrinha"]

PALAVRAS_CURIOSOS = ["gratis", "grátis", "de graça", "free", "sem pagar", "como fazer sem curso", "pirata", "torrent", "crackeado"]

def detectar_intencao(texto_usuario, cidade_selecionada=""):
    texto = texto_usuario.lower()
    
    # 1. Filtro de curiosos
    for palavra in PALAVRAS_CURIOSOS:
        if palavra in texto:
            return "CURIOSO"
    
    # 2. Detecta se é serviço local
    if cidade_selecionada:
        return "SERVICO_LOCAL"
    for cidade in CIDADES_SERVICO:
        if cidade in texto:
            return "SERVICO_LOCAL"
    if any(x in texto for x in ["pedreiro", "orçamento", "obra", "instalação", "sob medida", "feira", "irará", "medida na sua casa"]):
        return "SERVICO_LOCAL"
    
    # 3. Se não for serviço, é curso
    return "CURSO_ONLINE"

def gerar_pack_youtube(gancho, score=9.0, preco_cheio="R$99,90", preco_rem="R$49,90", cidade="", tipo_forcado="AUTO"):
    
    if tipo_forcado == "AUTO":
        tipo = detectar_intencao(gancho, cidade)
    else:
        tipo = tipo_forcado

    # === FILTRO CURIOSOS ===
    if tipo == "CURIOSO":
        return {
            "titulo": "⛔ NÃO GERAR - Lead curioso filtrado",
            "descricao": f"Esse gancho '{gancho}' contém palavra de curioso (grátis, pirata, etc). Não gasta anúncio com ele. Lead desqualificado.",
            "tags": ["curioso filtrado"],
            "tipo": "CURIOSO",
            "preco_cheio": preco_cheio,
            "preco_remarketing": preco_rem,
            "recomendacao": "FILTRAR - Não investe"
        }

    # === TIPO 1: SERVIÇO LOCAL - PEDREIRO PORCELANATO ===
    if tipo == "SERVICO_LOCAL":
        cidade_formatada = cidade.title() if cidade else "Irará / Feira de Santana e região"
        titulo = f"BANCADA / PIA / CLOSET / FACHADA em PORCELANATO sob medida em {cidade_formatada} | FC Constrói"
        
        descricao = f"""🔨 SERVIÇO DE PEDREIRO ESPECIALISTA EM PORCELANATO - {cidade_formatada.upper()}

Fazemos na sua casa em {cidade_formatada} e região:
✅ Pia de banheiro em porcelanato
✅ Bancada de cozinha em porcelanato estrutural
✅ Closet em porcelanato
✅ Nicho, prateleira, armário
✅ Pisos e fachadas em porcelanato
✅ Corte 45 graus sem erro - 100% porcelanato

📍 ATENDEMOS: Santanópolis, Irará, Feira de Santana, Água Fria, Ouriçanga, Santa Bárbara, Serrinha e toda região

NÃO vendemos placa. Fazemos o projeto COMPLETO sob medida e instalado.
Mais resistente que MDF.

💬 Comenta BANCADA ou chama no WhatsApp pra orçamento grátis na sua cidade
📲 Atendimento local - Orçamento presencial

#porcelanato #bancadaem porcelanato {cidade_formatada.lower()} #pedreiro #fcconstroi
Score: {score}/10
"""
        tags = [
            f"bancada porcelanato {cidade_formatada.lower()}",
            f"pia banheiro porcelanato {cidade_formatada.lower()}",
            f"closet porcelanato {cidade_formatada.lower()}",
            f"pedreiro porcelanato {cidade_formatada.lower()}",
            "fachada porcelanato", "piso porcelanato", "bancada cozinha sob medida",
            f"fc constrói {cidade_formatada.lower()}", "porcelanato estrutural"
        ]

    # === TIPO 2: CURSO ONLINE NACIONAL R$99,90 ===
    else:
        titulo = f"CURSO PORCELANATO FC CONSTRÓI - Do Zero ao Avançado | PIA BANCADA CLOSET NICHO | {gancho}"
        
        descricao = f"""🎓 CURSO 100% ONLINE - PORCELANATO FC CONSTRÓI - DO ZERO AO AVANÇADO

Aprenda a fazer e VENDER:
✅ Pia de banheiro em porcelanato
✅ Bancada de cozinha em porcelanato estrutural
✅ Closet em porcelanato
✅ Nicho, prateleira, armário, gaveta
✅ Pisos e fachadas - Corte 45 graus sem erro

Tudo em porcelanato puro, sem MDF. Sob medida.

💰 PAGAMENTO ÚNICO R$99,90 pela Kiwify - Acesso vitalício Brasil todo
Não é mensalidade. Curso completo do zero ao avançado.

👉 Comenta BANCADA que mando o link oficial ou acessa:
Catalogo: https://fcconstroi.kiwify.com.br

🚫 NÃO é grátis. Não tem pirata. Só original FC Constrói.

#curso porcelanato #fcconstroi #bancada porcelanato #pia porcelanato
Score: {score}/10 | {gancho}
"""
        tags = [
            "curso porcelanato", "fc constrói curso", "curso porcelanato online",
            "bancada porcelanato curso", "pia banheiro porcelanato curso",
            "closet porcelanato curso", "porcelanato do zero ao avançado",
            "curso porcelanato 99,90", "kiwify porcelanato"
        ]

    return {
        "titulo": titulo[:100], # SEO YouTube max 100 chars
        "descricao": descricao,
        "tags": tags,
        "tipo": tipo,
        "preco_cheio": "Sob consulta (serviço local)" if tipo == "SERVICO_LOCAL" else preco_cheio,
        "preco_remarketing": "N/A serviço" if tipo == "SERVICO_LOCAL" else preco_rem,
        "recomendacao": "INVESTE Google Meu Negócio + Instagram Local" if tipo == "SERVICO_LOCAL" else "INVESTE Meta ADS Brasil todo - R$99,90"
    }
