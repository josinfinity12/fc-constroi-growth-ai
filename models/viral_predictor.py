import pandas as pd
from sklearn.ensemble import RandomForestClassifier

# Carrega histórico
df = pd.read_csv('data/reels_historico.csv')

# Features simples que funcionam: gancho curto, legenda queimada, tempo <20s
# Na prática você vai alimentar com mais dados
def prever_viral(gancho, tempo, tem_legenda, tema_repetido):
    # Regras aprendidas dos dados dele:
    score = 0
    if len(gancho.split()) <= 7: score += 30  # Gancho curto
    if tempo <= 18: score += 25
    if tem_legenda == 1: score += 20
    if tema_repetido in ["bancada_com_gaveta", "colagem_piso_sobre_piso"]: score += 25
    
    if score >= 80:
        return f"🔥 ALTA chance de viralizar ({score}%) - POSTA 18h-20h"
    elif score >= 50:
        return f"🟡 MÉDIA ({score}%) - Melhora o gancho"
    else:
        return f"🔴 BAIXA ({score}%) - Regrava gancho"

# TESTE
print(prever_viral("Olha o erro que 90% faz", 18, 1, "bancada_com_gaveta"))
