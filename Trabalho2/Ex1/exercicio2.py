import random
from collections import Counter
from math import log2
import os
import matplotlib.pyplot as plt

# ---------- Codificação de canal (repetição 3,1) ----------
def codificar_repeticao_3_1(bits):
    return ''.join(bit * 3 for bit in bits)

def descodificar_repeticao_3_1(bits):
    return ''.join(
        '1' if grupo.count('1') >= 2 else '0'
        for grupo in [bits[i:i+3] for i in range(0, len(bits), 3)]
    )

# ---------- Canal BSC ----------
def gerar_vetor_erro(tamanho, ber):
    return ''.join('1' if random.random() < ber else '0' for _ in range(tamanho))

def aplicar_erro(binario, vetor_erro):
    return ''.join('1' if b != e else '0' for b, e in zip(binario, vetor_erro))

# ---------- Cifra Vigenère com XOR ----------
def vigenere_encrypt(data: bytes, key: bytes) -> bytes:
    return bytes((b ^ key[i % len(key)]) for i, b in enumerate(data))

# ---------- Codificação de fonte ----------
def texto_para_bits(texto):
    return ''.join(format(ord(c), '08b') for c in texto)

def bits_para_texto(bits):
    return ''.join(chr(int(bits[i:i+8], 2)) for i in range(0, len(bits), 8))

# ---------- Análise: entropia, histograma, compressão ----------
def calcular_entropia(data):
    total = len(data)
    freq = Counter(data)
    return -sum((f / total) * log2(f / total) for f in freq.values())

def analisar_ficheiro(path):
    with open(path, 'rb') as f:
        data = f.read()
    tamanho = len(data)
    entropia = calcular_entropia(data)
    histograma = Counter(data)
    return tamanho, entropia, histograma

# ---------- Geração de gráfico de histograma ----------
def plotar_histograma(histograma, filename, title):
    # histograma: Counter de bytes → contagem
    keys = sorted(histograma.keys())
    values = [histograma[k] for k in keys]
    plt.figure()
    plt.bar(keys, values)
    plt.title(title)
    plt.xlabel('Valor do byte')
    plt.ylabel('Frequência')
    plt.tight_layout()
    plt.savefig(filename)  # Guarda o gráfico como imagem
    plt.close()

# ---------- Sistema de transmissão completo A → E ----------
def sistema_transmissao(a_path, e_path, chave, p):
    # Leitura do ficheiro A (original)
    with open(a_path, "r", encoding="utf-8") as f:
        texto_A = f.read()

    # Codificação de fonte → B (texto para bits e gravação)
    bits_B = texto_para_bits(texto_A)
    with open("B.txt", "wb") as f:
        f.write(bits_B.encode())

    # Cifra Vigenère → C
    data_A_bytes = texto_A.encode("utf-8")
    encrypted_bytes = vigenere_encrypt(data_A_bytes, chave.encode())
    with open("C.txt", "wb") as f:
        f.write(encrypted_bytes)

    # Codificação de canal → D (bits codificados)
    bits_C = ''.join(format(byte, '08b') for byte in encrypted_bytes)
    bits_D = codificar_repeticao_3_1(bits_C)
    with open("D.txt", "wb") as f:
        f.write(bits_D.encode())

    # Canal BSC → D_erro (com erros)
    vetor_erro = gerar_vetor_erro(len(bits_D), p)
    bits_D_com_erro = aplicar_erro(bits_D, vetor_erro)
    with open("D_erro.txt", "wb") as f:
        f.write(bits_D_com_erro.encode())

    # Decodificação de canal → bits_C_decod
    bits_C_decod = descodificar_repeticao_3_1(bits_D_com_erro)

    # Decifra da cifra Vigenère
    decrypted_bytes = vigenere_encrypt(
        bytes(int(bits_C_decod[i:i+8], 2) for i in range(0, len(bits_C_decod), 8)),
        chave.encode()
    )
    texto_B_decod = decrypted_bytes.decode("utf-8", errors="replace")

    # Decodificação de fonte → E (texto final)
    bits_E = texto_para_bits(texto_B_decod)
    texto_E = bits_para_texto(bits_E)
    with open(e_path, "w", encoding="utf-8") as f:
        f.write(texto_E)

    # Verificação final
    sucesso = texto_A == texto_E
    ber = sum(a != b for a, b in zip(bits_B, bits_E)) / len(bits_B)

    print("------ Resultados do Exercício 2 ------")
    print(f"Canal BSC com p = {p}")
    print(f"Chave da cifra: {chave}")
    print(f"Reconstrução correta? {'SIM' if sucesso else 'NÃO'}")
    print(f"BER final (A vs E): {ber:.4f}\n")

    # Análise de cada ficheiro: dimensão, entropia, histograma e gráfico
    for label, path in zip(['A', 'B', 'C', 'D', 'D_erro', 'E'],
                           [a_path, 'B.txt', 'C.txt', 'D.txt', 'D_erro.txt', e_path]):
        tamanho, entropia, hist = analisar_ficheiro(path)
        print(f"Ficheiro {label}: {tamanho} bytes, entropia = {entropia:.4f}")
        # Gerar gráfico de histograma para este ficheiro
        plotar_histograma(hist, f"hist_{label}.png", f"Histograma {label}")
    print()

# ---------- Main ----------
def main():
    chave = "ISEL"
    sistema_transmissao("../Ex1/A.txt", "E.txt", chave, p=0.1)

if __name__ == "__main__":
    main()
