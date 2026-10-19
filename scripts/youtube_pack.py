def gerar_pack_youtube(gancho, score=8.5, preco="R$99,90", preco_remarketing="R$49,90", link_kiwify="https://fcconstroi.kiwify.com.br"):
    KEYWORDS = ["bancada em porcelanato","pia de porcelanato","closet de porcelanato","nicho porcelanato","banheiro porcelanato","armario porcelanato","bancada gourmet porcelanato","pia porcelanato sob medida","fc constrói"]
    if score >= 9.0:
        titulo = f"{gancho.upper()} 100% PORCELANATO por {preco} - SOB MEDIDA | FC Constrói"
    elif score >= 8.0:
        titulo = f"{gancho} em Porcelanato | De {preco_remarketing} por {preco} - Remarketing"
    else:
        titulo = f"{gancho} - Pia, Bancada, Closet Tudo em Porcelanato | FC Constrói"
    titulo = titulo[:95]
    descricao = f"""{gancho} 100% PORCELANATO - SOB MEDIDA!
Nao vendemos placa. Criamos: PIA, BANCADA, CLOSET, BANHEIRO, ARMARIO, GAVETA, NICHO
Tudo em porcelanato, mais resistente que MDF!
PRECO: {preco} | REMARKETING: {preco_remarketing}
COMENTA BANCADA que mando catalogo!
Catalogo: {link_kiwify}
Score: {score}/10
"""
    return {"titulo": titulo, "descricao": descricao, "tags": KEYWORDS, "preco_cheio": preco, "preco_remarketing": preco_remarketing}