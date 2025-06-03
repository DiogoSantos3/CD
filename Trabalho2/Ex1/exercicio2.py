import random

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

# ---------- Cifra Vigenère ----------

def vigenere_encode(texto, chave):
    chave_full = (chave * ((len(texto) // len(chave)) + 1))[:len(texto)]
    return ''.join(chr((ord(c) + ord(k)) % 256) for c, k in zip(texto, chave_full))

def vigenere_decode(texto, chave):
    chave_full = (chave * ((len(texto) // len(chave)) + 1))[:len(texto)]
    return ''.join(chr((ord(c) - ord(k)) % 256) for c, k in zip(texto, chave_full))

# ---------- Codificação de fonte (simples em binário) ----------

def texto_para_bits(texto):
    return ''.join(format(ord(c), '08b') for c in texto)

def bits_para_texto(bits):
    return ''.join(chr(int(bits[i:i+8], 2)) for i in range(0, len(bits), 8))

# ---------- Sistema de transmissão completo A → E ----------

def sistema_transmissao(a_path, e_path, chave, p):
    # Ficheiro A (original)
    with open(a_path, "r", encoding="utf-8") as f:
        texto_A = f.read()

    # Codificação de fonte → B (texto para bits)
    bits_B = texto_para_bits(texto_A)

    # Cifra Vigenère → C
    texto_C = vigenere_encode(texto_A, chave)
    bits_C = texto_para_bits(texto_C)

    # Codificação de canal → D
    bits_D = codificar_repeticao_3_1(bits_C)

    # Canal BSC → bits com erro
    vetor_erro = gerar_vetor_erro(len(bits_D), p)
    bits_D_com_erro = aplicar_erro(bits_D, vetor_erro)

    # Decodificação de canal
    bits_C_decod = descodificar_repeticao_3_1(bits_D_com_erro)

    # Decifra → B'
    texto_C_decod = bits_para_texto(bits_C_decod)
    texto_B_decod = vigenere_decode(texto_C_decod, chave)

    # Decodificação de fonte → E
    bits_E = texto_para_bits(texto_B_decod)
    texto_E = bits_para_texto(bits_E)

    # Guardar E
    with open(e_path, "w", encoding="utf-8") as f:
        f.write(texto_E)

    # Resultados
    sucesso = texto_A == texto_E
    ber = sum(a != b for a, b in zip(bits_B, bits_E)) / len(bits_B)

    print("------ Resultados do Exercício 2 ------")
    print(f"Canal BSC com p = {p}")
    print(f"Chave da cifra: {chave}")
    print(f"Reconstrução correta? {'SIM ✅' if sucesso else 'NÃO ❌'}")
    print(f"BER final (A vs E): {ber:.4f}")
    print()

# ---------- Exemplo de uso ----------

def main():
    chave = "ISEL"
    sistema_transmissao("A.txt", "E.txt", chave, p=0.1)

if __name__ == "__main__":
    main()
