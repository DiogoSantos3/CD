import math
import matplotlib.pyplot as plt 
from collections import Counter

def analisar_fonte(caminho):
    try:
        with open(caminho, 'r', encoding='utf-8') as f:
            texto = f.read()
    except UnicodeDecodeError:
        with open(caminho, 'r', encoding='latin-1') as f:
            texto = f.read()
    total = len(texto)
    contagem = Counter(texto)
    probs = {char: freq / total for char, freq in contagem.items()}

    # (a) ================== Símbolo mais frequente, Probabilidade, Informação própria ==================
    simbolo_mais_freq = max(probs, key=probs.get)
    prob_max = probs[simbolo_mais_freq]
    info_propria = -math.log2(prob_max)

    print(f"\nAnálise de: {caminho}")
    print(f"Símbolo mais frequente: {repr(simbolo_mais_freq)}")
    print(f"Probabilidade: {prob_max:.4f}")
    print(f"Informação própria: {info_propria:.4f} bits")

    # (b)  ================== Entropia ==================
    entropia = -sum(p * math.log2(p) for p in probs.values())
    print(f"Entropia da fonte: {entropia:.4f} bits/símbolo")

    # (c) ================== Histograma ==================
    plt.figure(figsize=(10, 4))
    plt.bar(probs.keys(), probs.values())
    plt.title(f"Histograma de {caminho}")
    plt.xlabel("Símbolos")
    plt.ylabel("Probabilidade")
    plt.grid(True)
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    analisar_fonte("a.txt")
    analisar_fonte("alice29.txt")
    