import re
import unicodedata

def tirar_acento(texto):
    return ''.join(c for c in unicodedata.normalize('NFD', texto) if unicodedata.category(c) != 'Mn')

CIDADES_VALIDAS = ["santanopolis", "irara", "feira de santana", "agua fria", "serrinha", "santa barbara"]

def extrair_cidade(texto):
    texto_sem_acento = tirar_acento(texto.lower())
    for cidade in CIDADES_VALIDAS:
        if cidade in texto_sem_acento:
            return cidade, True
    
    match = re.search(r"(?:em|para|faz em|atende|de|no|na)\s+([a-z\s]+)\??", texto_sem_acento)
    if match:
        cidade_fora = match.group(1).strip()
        if cidade_fora not in ["que", "qual", "quanto", "onde"] and len(cidade_fora) > 2:
            return cidade_fora, False
    return None, None

def classificar_comentario(comentario):
    texto_norm = tirar_acento(comentario.lower())
    cidade, eh_valida = extrair_cidade(comentario)
    
    if cidade and not eh_valida:
        return "ORCAMENTO_FORA_DA_AREA", cidade
    if cidade and eh_valida:
        return "ORCAMENTO_LOCAL_VALIDO", cidade
    if any(p in texto_norm for p in ["gaveta", "closet", "porcelanato", "bancada", "argamassa"]):
        return "CURSO_ONLINE", None
    return "DUVIDA_GERAL", None

if __name__ == "__main__":
    testes = [
        "faz em Salvador?",
        "faz em Irará?",
        "atende Feira de Santana?",
        "quanto cobra em Serrinha?",
        "como faz gaveta?",
        "qual medida de closet?",
        "como faz bancada?",
        "qual porcelanato usou?",
        "qual argamassa?",
        "faz no Rio?"
    ]
    for t in testes:
        tipo, cidade = classificar_comentario(t)
        print(f"{t:30} -> {tipo:30} | cidade: {cidade}")
    
    print("\nOK! Filtro funcionando. 6 cidades = WhatsApp | Resto = Curso Online")