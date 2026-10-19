import pandas as pd
from datetime import datetime, timedelta

def filtrar_remarketing_30d(arquivo_kiwify="kiwify_vendas.csv", arquivo_manychat="manychat_leads.csv"):
    try:
        kiwify = pd.read_csv(arquivo_kiwify)
    except:
        kiwify = pd.DataFrame({
            'email': ['cliente1@email.com', 'cliente2@email.com'],
            'data_compra': [(datetime.now() - timedelta(days=5)).strftime('%Y-%m-%d'), (datetime.now() - timedelta(days=40)).strftime('%Y-%m-%d')],
            'produto': ['Bancada Gourmet', 'Pia Porcelanato']
        })
    kiwify['data_compra'] = pd.to_datetime(kiwify['data_compra'])
    limite = datetime.now() - timedelta(days=30)
    comprou_30d = kiwify[kiwify['data_compra'] >= limite]['email'].tolist()
    try:
        manychat = pd.read_csv(arquivo_manychat)
    except:
        manychat = pd.DataFrame({
            'email': ['cliente1@email.com', 'cliente4@email.com', 'cliente5@email.com'],
            'nome': ['Joao', 'Maria', 'Pedro'],
            'tag': ['BANCADA', 'BANCADA', 'BANCADA']
        })
    remarketing = manychat[~manychat['email'].isin(comprou_30d)]
    print(f"Bloqueados (comprou <30d): {len(comprou_30d)}")
    print(f"Remarketing R$49,90: {len(remarketing)}")
    return remarketing
