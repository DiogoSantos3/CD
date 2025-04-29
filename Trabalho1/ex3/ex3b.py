#=============== i ===============
import random
import string

def calcular_entropia(probabilidades):
    return -sum(p * math.log2(p) for p in probabilidades if p > 0)


def plotar_histograma(ficheiro, titulo):
    with open(ficheiro, "r", encoding="utf-8") as f:
        texto = f.read()
    total = len(texto)
    contagem = Counter(texto)
    probs = {char: freq / total for char, freq in contagem.items()}

    entropia = calcular_entropia(probs.values())

    print(f"\nFicheiro: {ficheiro}")
    print(f"Entropia: {entropia:.4f} bits/símbolo")

    plt.figure(figsize=(10, 4))
    plt.bar(probs.keys(), probs.values())
    plt.title(f"Histograma de {titulo}")
    plt.xlabel("Símbolos")
    plt.ylabel("Probabilidade")
    plt.grid(True)
    plt.tight_layout()
    plt.show()


def gerar_palavra_passe():
    tamanho = random.randint(10, 14)
    alfabeto = string.ascii_letters + string.digits + "!@#$%&*?"
    return ''.join(random.choice(alfabeto) for _ in range(tamanho))

def gerar_exemplos_palavras_passe():
    print("\nPalavras-passe geradas:")
    for i in range(10):
        print(f"PW{i+1}: {gerar_palavra_passe()}")


#=============== ii ===============
def gerar_ipv4():
    return ".".join(str(random.randint(0, 255)) for _ in range(4))


def gerar_exemplos_ipv4():
    print("\nEndereços IPv4 gerados:")
    for _ in range(10):
        print(gerar_ipv4())

#=============== iii ===============
def gerar_ipv6():
    return ":".join(f"{random.randint(0, 65535):04x}" for _ in range(8))


def gerar_exemplos_ipv6():
    print("\nEndereços IPv6 gerados:")
    for _ in range(10):
        print(gerar_ipv6())


#=============== iv ===============
def gerar_tuplo_hex():
    return [f"{random.randint(0, 255):02X}" for _ in range(8)]


def gerar_exemplos_tuplos_hex():
    print("\nTuplos hexadecimais gerados:")
    for _ in range(10):
        print(gerar_tuplo_hex())


#=============== MAIN ===============

def main():
    gerar_exemplos_palavras_passe()  # 3bi
    gerar_exemplos_ipv4()        # 3bii
    gerar_exemplos_ipv6()        # 3biii
    gerar_exemplos_tuplos_hex()  # 3biv


if __name__ == "__main__":
    main()

