import random

# ---------- Funções Auxiliares ----------

def gerar_vetor_erro(tamanho, ber):
    return ''.join('1' if random.random() < ber else '0' for _ in range(tamanho))

def aplicar_erro(binario, vetor_erro):
    return ''.join('1' if b != e else '0' for b, e in zip(binario, vetor_erro))

# ---------- Exercício 1(a) e 1(b): BSC ----------

def bsc(ficheiro_entrada, ficheiro_saida, p):
    with open(ficheiro_entrada, 'rb') as f_in:
        dados = f_in.read()

    dados_binarios = ''.join(format(byte, '08b') for byte in dados)
    vetor_erro = gerar_vetor_erro(len(dados_binarios), p)

    print(f"Vetor de erro (BSC p={p}): {vetor_erro}")

    dados_com_erro = aplicar_erro(dados_binarios, vetor_erro)

    dados_saida = bytearray()
    for i in range(0, len(dados_com_erro), 8):
        byte = dados_com_erro[i:i+8]
        if len(byte) == 8:
            dados_saida.append(int(byte, 2))

    with open(ficheiro_saida, 'wb') as f_out:
        f_out.write(dados_saida)

    total_bits = len(dados_binarios)
    bits_errados = sum(1 for b1, b2 in zip(dados_binarios, dados_com_erro) if b1 != b2)
    ber = bits_errados / total_bits

    total_simbolos = len(dados)
    simbolos_errados = sum(1 for o, e in zip(dados, dados_saida) if o != e)
    ser = simbolos_errados / total_simbolos

    print(f"--- BSC (p = {p}) ---")
    print(f"Ficheiro original: {ficheiro_entrada}")
    print(f"Ficheiro com erros: {ficheiro_saida}")
    print(f"Bits transmitidos: {total_bits}")
    print(f"Símbolos transmitidos: {total_simbolos}")
    print(f"Símbolo recebido (em binário): {dados_com_erro[:8]}")
    print(f"BER: {ber:.4f}")
    print(f"SER: {ser:.4f}\n")

# ---------- Exercício 1(c): Codificação (3,1) ----------

def codificar_repeticao_3_1(bits):
    return ''.join(bit * 3 for bit in bits)

def descodificar_repeticao_3_1(bits):
    return ''.join(
        '1' if grupo.count('1') >= 2 else '0'
        for grupo in [bits[i:i+3] for i in range(0, len(bits), 3)]
    )

# ---------- Exercício 1(c): Codificação Hamming (7,4) ----------

def codificar_hamming_7_4(bits4):
    G = [
        [1, 0, 0, 0, 0, 1, 1],
        [0, 1, 0, 0, 1, 0, 1],
        [0, 0, 1, 0, 1, 1, 0],
        [0, 0, 0, 1, 1, 1, 1]
    ]
    return ''.join(
        str(sum(int(bits4[j]) * G[j][i] for j in range(4)) % 2)
        for i in range(7)
    )

def codificar_hamming_stream(bits):
    result = ''
    for i in range(0, len(bits), 4):
        bloco = bits[i:i+4].ljust(4, '0')
        result += codificar_hamming_7_4(bloco)
    return result

def descodificar_hamming_stream(bits):
    def corrigir(grupo):
        H = [
            [1, 1, 1, 0, 1, 0, 0],
            [1, 1, 0, 1, 0, 1, 0],
            [1, 0, 1, 1, 0, 0, 1]
        ]
        s = [sum(int(grupo[j]) * H[i][j] for j in range(7)) % 2 for i in range(3)]
        pos = int(''.join(map(str, s)), 2)
        if pos != 0 and pos <= 7:
            i = pos - 1
            grupo = grupo[:i] + ('0' if grupo[i] == '1' else '1') + grupo[i+1:]
        return grupo[0] + grupo[1] + grupo[2] + grupo[3]

    return ''.join(
        corrigir(bits[i:i+7])
        for i in range(0, len(bits), 7)
        if len(bits[i:i+7]) == 7
    )

# ---------- Exercício 1(c): Simulação com codificação ----------

def simular_transmissao(dados, p, modo):
    original_bin = ''.join(format(b, '08b') for b in dados)

    if modo == 'repeticao':
        codificado = codificar_repeticao_3_1(original_bin)
    elif modo == 'hamming':
        codificado = codificar_hamming_stream(original_bin)
    else:
        codificado = original_bin

    vetor_erro = gerar_vetor_erro(len(codificado), p)

    print(f"Vetor de erro ({modo}, p={p}): {vetor_erro}")  # <- NOVO

    recebido = aplicar_erro(codificado, vetor_erro)

    if modo == 'repeticao':
        descodificado = descodificar_repeticao_3_1(recebido)
    elif modo == 'hamming':
        descodificado = descodificar_hamming_stream(recebido)
    else:
        descodificado = recebido

    descodificado = descodificado[:len(original_bin)]

    total_bits = len(original_bin)
    bits_errados = sum(1 for a, b in zip(original_bin, descodificado) if a != b)
    ber = bits_errados / total_bits

    original_bytes = [int(original_bin[i:i+8], 2) for i in range(0, len(original_bin), 8)]
    final_bytes = [int(descodificado[i:i+8], 2) for i in range(0, len(descodificado), 8)]
    total_simbolos = len(original_bytes)
    simbolos_errados = sum(1 for a, b in zip(original_bytes, final_bytes) if a != b)
    ser = simbolos_errados / total_simbolos

    print(f"[{modo.upper():>9}] p={p:.2f} | BER={ber:.4f} | SER={ser:.4f}")

# ---------- Main ----------

def main():
    print("------ Exercício 1(a) e (b): Função BSC ------")
    bsc("u.txt", "u_bsc_00.txt", 0.0)
    bsc("u.txt", "u_bsc_01.txt", 0.1)
    bsc("u.txt", "u_bsc_05.txt", 0.5)
    bsc("u.txt", "u_bsc_08.txt", 0.8)

    print("------ Exercício 1(c): Comparação de modos de transmissão ------")
    with open("u.txt", "rb") as f:
        dados = f.read()

    for p in [0.1, 0.2, 0.3, 0.4]:
        simular_transmissao(dados, p, modo='sem')
        simular_transmissao(dados, p, modo='repeticao')
        simular_transmissao(dados, p, modo='hamming')

if __name__ == "__main__":
    main()
