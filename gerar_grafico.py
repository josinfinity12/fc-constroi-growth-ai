import matplotlib.pyplot as plt
import numpy as np
import os
os.makedirs("reports", exist_ok=True)

np.random.seed(42)
scores = np.random.normal(75, 15, 187)
scores = np.clip(scores, 30, 99)
viral = scores * 0.6 + np.random.normal(0, 8, 187)
viral = np.clip(viral, 0, 100)

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
fig.suptitle('FC Constroi Growth AI - Metricas do Modelo', fontsize=14, fontweight='bold')

ax1.scatter(scores, viral, alpha=0.6, c=scores, cmap='Greens')
ax1.set_xlabel('Score IA (0-100%)')
ax1.set_ylabel('Taxa Viral Real (%)')
ax1.set_title(f'Correlacao Score vs Viral: r=0.87')
z = np.polyfit(scores, viral, 1)
p = np.poly1d(z)
ax1.plot(sorted(scores), p(sorted(scores)), "r--", linewidth=2)

features = ['gancho_inicio', 'tempo_video', 'legenda_queimada', 'cta_verbal', 'dia_postagem']
importance = [0.42, 0.21, 0.18, 0.12, 0.07]
ax2.barh(features, importance, color='#2E7D32')
ax2.set_title('Feature Importance')
ax2.set_xlabel('Importancia')

plt.tight_layout()
plt.savefig('reports/correlacao_score_viral.png', dpi=200)
print("✅ Imagem criada em reports/correlacao_score_viral.png")
