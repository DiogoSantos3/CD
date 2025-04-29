import random
import math
import matplotlib.pyplot as plt
from collections import Counter


def calcular_entropia(probabilidades):
    return -sum(p * math.log2(p) for p in probabilidades if p > 0)


def plotar_histograma(ficheiro, titulo):
    with open(ficheiro, "r", encoding="utf-8") as f:
        texto = f.read()
    total = len(texto)
    contagem = Counter(texto)
    probs = {char: freq / total for char, freq in contagem.items()}

    entropia = calcular_entropia(probs.values())

    print(f"\n Ficheiro: {ficheiro}")
    print(f"Entropia: {entropia:.4f} bits/símbolo")

    plt.figure(figsize=(10, 4))
    plt.bar(probs.keys(), probs.values())
    plt.title(f"Histograma de {titulo}")
    plt.xlabel("Símbolos")
    plt.ylabel("Probabilidade")
    plt.grid(True)
    plt.tight_layout()
    plt.show()


def gerar_fonte_simbolos(alfabeto, N, probs, nome_ficheiro):
    simbolos = random.choices(alfabeto, weights=probs, k=N)
    with open(nome_ficheiro, "w", encoding="utf-8") as f:
        f.write("".join(simbolos))
    print(f"\n Ficheiro '{nome_ficheiro}' gerado com {N} símbolos.")


def gerar_ficheiro1():
    alfabeto = ['A', 'B', 'C', 'D']
    probs = [0.5, 0.25, 0.125, 0.125]
    gerar_fonte_simbolos(alfabeto, 100, probs, "ficheiro1.txt")


def gerar_ficheiro2():
    alfabeto = ['A', 'B', 'C', 'D']
    probs = [0.5, 0.25, 0.125, 0.125]
    gerar_fonte_simbolos(alfabeto, 1000, probs, "ficheiro2.txt")


def gerar_ficheiro3():
    alfabeto = [chr(i) for i in range(65, 65+16)]  # Letras A a P
    probs = [1/16] * 16
    gerar_fonte_simbolos(alfabeto, 1000, probs, "ficheiro3.txt")


def analisar_ficheiros_gerados():
    plotar_histograma("ficheiro1.txt", "ficheiro1.txt")
    plotar_histograma("ficheiro2.txt", "ficheiro2.txt")
    plotar_histograma("ficheiro3.txt", "ficheiro3.txt")


def main():
    # Parte 3c
    gerar_ficheiro1()
    gerar_ficheiro2()
    gerar_ficheiro3()

    # Parte 3d
    analisar_ficheiros_gerados()


if __name__ == "__main__":
    main()
