import random

def ler_letra_do_ficheiro(nome_ficheiro):
    with open(nome_ficheiro, 'r') as f:
        letra = f.read(1)
    return letra

def letra_para_binario(letra):
    ascii_code = ord(letra)
    binario = format(ascii_code, '08b')  # 8 bits
    return binario

def gerar_vetor_erro(tamanho, ber):
    # BER = número de bits com erro / número total de bits transmitidos
    # Geramos um vetor de erro e com probabilidade 'ber' o bit é 1 (erro)
    return ''.join('1' if random.random() < ber else '0' for _ in range(tamanho))

def aplicar_erro(binario, vetor_erro):
    return ''.join('1' if b != e else '0' for b, e in zip(binario, vetor_erro))

def binario_para_ascii(binario):
    return int(binario, 2)

def processar_letra_com_ber(nome_ficheiro, ber):
    letra = ler_letra_do_ficheiro(nome_ficheiro)
    binario_original = letra_para_binario(letra)

    print("Letra original:", letra)
    print("Código binário original:", binario_original)

    if ber == 0:
        print("Sem erros (BER = 0).")
        print("Código ASCII:", ord(letra))
        return binario_original
    else:
        vetor_erro = gerar_vetor_erro(len(binario_original), ber)
        binario_com_erro = aplicar_erro(binario_original, vetor_erro)
        codigo_ascii_final = binario_para_ascii(binario_com_erro)

        print("Vetor de erro:            ", vetor_erro)
        print("Código binário com erro: ", binario_com_erro)
        print("Código ASCII (com erro): ", codigo_ascii_final)
        return binario_com_erro


def main():
    # Exemplos de uso:
    print("------ Exercício 1 (BER = 0) ------")
    processar_letra_com_ber("u.txt", 0)

    print("\n------ Exercício 2 (BER = 1/4) ------")
    processar_letra_com_ber("u.txt", 1/4)


if __name__ == "__main__":
    main()