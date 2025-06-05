import random

def ler_letra_do_ficheiro(nome_ficheiro):
    with open(nome_ficheiro, 'r') as f:
        letra = f.read(1)
    return letra

def letra_para_binario(letra):
    ascii_code = ord(letra)
    binario = format(ascii_code, '08b')
    return binario

def gerar_vetor_erro(tamanho, ber):
    return ''.join('1' if random.random() < ber else '0' for _ in range(tamanho))

def aplicar_erro(binario, vetor_erro):
    b = int(binario, 2)
    e = int(vetor_erro, 2)
    resultado = b ^ e
    return format(resultado, f'0{len(binario)}b')


def binario_para_ascii(binario):
    return int(binario, 2)

def bsc(nome_ficheiro, ber):
    letra = ler_letra_do_ficheiro(nome_ficheiro)
    binario_original = letra_para_binario(letra)

    with open("dU.txt", "w") as f:
        f.write(f"Letra lida:              {letra}\n")
        f.write(f"Código binário original: {binario_original}\n")

        if ber == 0:
            f.write("BER é 0, sem erro aplicado.\n")
            return binario_original
        else:
            vetor_erro = gerar_vetor_erro(len(binario_original), ber)
            binario_com_erro = aplicar_erro(binario_original, vetor_erro)
            codigo_ascii_final = binario_para_ascii(binario_com_erro)

            f.write(f"Vetor de erro:            {vetor_erro}\n")
            f.write(f"Código binário com erro: {binario_com_erro}\n")
            f.write(f"Código ASCII (com erro): {codigo_ascii_final}\n")

            return binario_com_erro

if __name__ == "__main__":
    print(bsc("u.txt", 0) + "\n")
   ## print(bsc("u.txt", 1/4))
