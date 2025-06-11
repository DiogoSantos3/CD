#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ex2.py

Pipeline de Codificação de Fonte, Cifra e Canal (Repetição + BSC) para A.txt, usando as funções de Trabalho1/ex5.

1) Executa o pipeline completo com p = 0 para gerar A, B, C, D, E sem erros e salvar 5 histogramas:
     - hist_A.png
     - hist_B_0.png
     - hist_C_0.png
     - hist_D_0.png
     - hist_E_0.png

2) Depois testa BER ∈ {0.001, 0.01, 0.1, 0.25}, imprimindo apenas:
     BER=<valor> → A == E? SIM/NÃO

Intermediários são apagados (exceto os 5 histogramas do passo p = 0).
"""

import os
import sys
import gzip
import struct
import random
from collections import Counter
import importlib.util
import matplotlib.pyplot as plt

# ————— Caminho absoluto deste script (Trabalho2/ex2) —————
PASTA_EX2 = os.path.dirname(os.path.abspath(__file__))

# ————— Caminho até “CD/Trabalho1/ex5” —————
PASTA_CD = os.path.abspath(os.path.join(PASTA_EX2, "..", ".."))
PASTA_EX5 = os.path.join(PASTA_CD, "Trabalho1", "ex5")

if not os.path.isdir(PASTA_EX5):
    print(f"Erro: não encontrei {PASTA_EX5}")
    sys.exit(1)
if PASTA_EX5 not in sys.path:
    sys.path.insert(0, PASTA_EX5)

# ————— Importar encrypt_file e decrypt_file de ex5/5a.py —————
spec_5a = importlib.util.spec_from_file_location(
    "mod_5a", os.path.join(PASTA_EX5, "5a.py")
)
mod_5a = importlib.util.module_from_spec(spec_5a)
spec_5a.loader.exec_module(mod_5a)
encrypt_file = mod_5a.encrypt_file
decrypt_file = mod_5a.decrypt_file


# ————— Funções de Codificação de Fonte (gzip) —————
def source_encode(input_path: str, output_path: str) -> None:
    with open(input_path, "rb") as f:
        data = f.read()
    with gzip.open(output_path, "wb") as f_out:
        f_out.write(data)

def source_decode(input_path: str, output_path: str) -> None:
    with gzip.open(input_path, "rb") as f_in:
        data = f_in.read()
    with open(output_path, "wb") as f_out:
        f_out.write(data)


# ————— Repetição (3,1) —————
def _bytes_to_bitstring(data: bytes) -> str:
    return "".join(f"{b:08b}" for b in data)

def _bitstring_to_bytes(bits: str) -> bytes:
    rem = len(bits) % 8
    if rem:
        bits += "0" * (8 - rem)
    return bytes(int(bits[i:i+8], 2) for i in range(0, len(bits), 8))

def channel_encode_repetition_3_1(input_path: str, output_path: str) -> None:
    with open(input_path, "rb") as f:
        raw = f.read()
    bits = _bytes_to_bitstring(raw)
    encoded_bits = "".join(b * 3 for b in bits)
    encoded_bytes = _bitstring_to_bytes(encoded_bits)
    header = struct.pack(">I", len(raw))
    with open(output_path, "wb") as f_out:
        f_out.write(header)
        f_out.write(encoded_bytes)

def channel_decode_repetition_3_1(input_path: str, output_path: str) -> None:
    with open(input_path, "rb") as f:
        hdr = f.read(4)
        orig_len = struct.unpack(">I", hdr)[0]
        payload = f.read()
    bits = _bytes_to_bitstring(payload)
    expected = orig_len * 8 * 3
    bits = bits[:expected]
    decoded = []
    for i in range(0, len(bits), 3):
        trio = bits[i:i+3]
        decoded.append("1" if trio.count("1") >= 2 else "0")
    decoded_bytes = _bitstring_to_bytes("".join(decoded))
    decoded_bytes = decoded_bytes[:orig_len]
    with open(output_path, "wb") as f_out:
        f_out.write(decoded_bytes)


# ————— BSC por ficheiro inteiro —————
def bsc_full_file(input_path: str, output_path: str, p: float) -> None:
    with open(input_path, "rb") as f:
        header = f.read(4)
        payload = f.read()
    bits = _bytes_to_bitstring(payload)
    erro_bits = ["1" if random.random() < p else "0" for _ in range(len(bits))]
    mod_bits = [
        ("0" if (b == "1" and e == "1") else
         "1" if (b == "0" and e == "1") else
         b)
        for b, e in zip(bits, erro_bits)
    ]
    new_payload = _bitstring_to_bytes("".join(mod_bits))
    with open(output_path, "wb") as f_out:
        f_out.write(header)
        f_out.write(new_payload)


# ————— Gerar histograma de um ficheiro —————
def plot_histogram_of_file(path: str, png_name: str) -> None:
    data = open(path, "rb").read()
    freqs = Counter(data)
    xs = sorted(freqs.keys())
    ys = [freqs[x] for x in xs]

    plt.figure(figsize=(7, 3))
    plt.bar(xs, ys, width=1.0)
    plt.title(os.path.basename(path))
    plt.xlabel("Byte (0–255)")
    plt.ylabel("Frequência")
    plt.tight_layout()

    out_png = os.path.join(PASTA_EX2, png_name)
    plt.savefig(out_png)
    plt.close()


# ————— Utilitários —————
def files_are_identical(path1: str, path2: str) -> bool:
    if not os.path.isfile(path1) or not os.path.isfile(path2):
        return False
    if os.path.getsize(path1) != os.path.getsize(path2):
        return False
    with open(path1, "rb") as f1, open(path2, "rb") as f2:
        while True:
            b1 = f1.read(4096)
            b2 = f2.read(4096)
            if not b1:
                return True
            if b1 != b2:
                return False

def remove_if_exists(path: str) -> None:
    try:
        if os.path.isfile(path):
            os.remove(path)
    except:
        pass


# ————— Pipeline para um valor de p e opcional geração de histogramas —————
def run_pipeline(p: float, gen_histograms: bool):
    path_A = os.path.join(PASTA_EX2, "A.txt")
    base, ext = os.path.splitext(os.path.basename(path_A))
    key = "leic2025"

    # nomes temporários
    B     = os.path.join(PASTA_EX2, f"{base}_B_{p:.3f}.gz")
    C     = os.path.join(PASTA_EX2, f"{base}_C_{p:.3f}.enc")
    D     = os.path.join(PASTA_EX2, f"{base}_D_{p:.3f}.rpt")
    Echan = os.path.join(PASTA_EX2, f"{base}_Echan_{p:.3f}.bsc")
    Ddec  = os.path.join(PASTA_EX2, f"{base}_Ddec_{p:.3f}.rpt")
    Cdec  = os.path.join(PASTA_EX2, f"{base}_Cdec_{p:.3f}.enc")
    E     = os.path.join(PASTA_EX2, f"{base}_E_{p:.3f}{ext}")

    # 1) Fonte → B (gzip)
    source_encode(path_A, B)

    tamanho_A = os.path.getsize(path_A)
    tamanho_B = os.path.getsize(B)
    razao = tamanho_B / tamanho_A if tamanho_A>0 else float('nan')
    if gen_histograms:
        print(f"Razão de compressão |B|/|A| = {tamanho_B}/{tamanho_A} = {razao:.4f}")

    # 2) B → C (XOR)
    encrypt_file(B, C, key)
    # 3) C → D (repetição 3,1)
    channel_encode_repetition_3_1(C, D)
    # 4) D → Echan (BSC)
    bsc_full_file(D, Echan, p)
    # 5) Echan → Ddec (decod repetição)
    channel_decode_repetition_3_1(Echan, Ddec)
    # 6) Ddec → Cdec (decifra XOR)
    decrypt_file(Ddec, Cdec, key)
    # 7) Cdec → E (gzip descompressão)
    sucesso = True
    try:
        source_decode(Cdec, E)
    except:
        sucesso = False

    # se pediram histograma, gera 5 (A, B, C, D, E quando existir)
    if gen_histograms:
        plot_histogram_of_file(path_A, f"hist_A_0.png")
        plot_histogram_of_file(B,      f"hist_B_0.png")
        plot_histogram_of_file(C,      f"hist_C_0.png")
        plot_histogram_of_file(D,      f"hist_D_0.png")
        if sucesso and os.path.isfile(E):
            plot_histogram_of_file(E, f"hist_E_0.png")

    # apagar intermediários (mantém hist_*.png)
    for tmp in (B, C, D, Echan, Ddec, Cdec, E):
        remove_if_exists(tmp)

    return sucesso


# ————— Programa Principal —————
def main():
    # Primeiro, roda pipeline com p = 0 e gera 5 histogramas
    path_A = os.path.join(PASTA_EX2, "A.txt")
    if not os.path.isfile(path_A):
        print("Erro: não encontrei ‘A.txt’ na pasta atual.")
        sys.exit(1)

    run_pipeline(0.0, gen_histograms=True)

    # Agora testa p ∈ {0.001, 0.01, 0.1, 0.25}, sem gerar histogramas
    BER_values = [0.001, 0.01, 0.1, 0.25]
    for p in BER_values:
        sucesso = run_pipeline(p, gen_histograms=False)
        # Se pipeline não reconstruiu E, então A != E
        print(f"BER={p:.3f} → A == E? {'SIM' if sucesso else 'NÃO'}")

    sys.exit(0)


if __name__ == "__main__":
    main()
