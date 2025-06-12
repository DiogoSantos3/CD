# modulo2.py

import os
import zipfile
import math
import gzip
from collections import Counter
import pandas as pd
import matplotlib.pyplot as plt
import random

# Função auxiliar: calcular entropia

def calcular_entropia(probabilidades):
    return -sum(p * math.log2(p) for p in probabilidades if p > 0)

# Função CRC-4

def crc4(msg_bin_str):
    gen = '11111'  # g(x) = x^4 + x^3 + x^2 + x + 1
    m = msg_bin_str + '0000'
    m = list(m)
    for i in range(len(msg_bin_str)):
        if m[i] == '1':
            for j in range(len(gen)):
                m[i + j] = str(int(m[i + j] != gen[j]))
    return ''.join(m[-4:])

# Função checksum IP (soma de complemento de 1)

def ip_checksum(data):
    total = sum(data)
    total = (total & 0xFFFF) + (total >> 16)
    checksum = ~total & 0xFFFF
    return checksum

# Função BSC (Binary Symmetric Channel)

def bsc(filepath_in, filepath_out, p):
    with open(filepath_in, 'rb') as f:
        data = bytearray(f.read())

    total_bits = len(data) * 8
    error_bits = 0

    for i in range(len(data)):
        for bit in range(8):
            if random.random() < p:
                data[i] ^= (1 << bit)
                error_bits += 1

    with open(filepath_out, 'wb') as f:
        f.write(data)

    ber = error_bits / total_bits
    return ber

# Função de análise de ficheiro

def analyze_file(filepath, output_dir):
    with open(filepath, 'rb') as f:
        data = f.read()

    total = len(data)
    contagem = Counter(data)
    probs = [freq / total for freq in contagem.values()]
    entropia = calcular_entropia(probs)

    filename = os.path.basename(filepath)
    compressed_path = os.path.join(output_dir, f"{filename}.gz")
    with gzip.open(compressed_path, 'wb') as f_out:
        f_out.write(data)

    compressed_size = os.path.getsize(compressed_path)

    return {
        "filename": filename,
        "original size (bytes)": total,
        "compressed size (bytes)": compressed_size,
        "compression ratio": round(total / compressed_size, 4),
        "entropy (bits/symbol)": round(entropia, 4)
    }

# Execução principal

def main():
    base_dir = os.path.dirname(__file__)
    zip_path = os.path.join(base_dir, "cantrbry.zip")
    extract_dir = os.path.join(base_dir, "cantrbry_extracted")
    compressed_dir = os.path.join(base_dir, "cantrbry_compressed")
    output_bsc_dir = os.path.join(base_dir, "cantrbry_bsc")

    os.makedirs(extract_dir, exist_ok=True)
    os.makedirs(compressed_dir, exist_ok=True)
    os.makedirs(output_bsc_dir, exist_ok=True)

    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extract_dir)

    results = []
    for fname in os.listdir(extract_dir):
        fpath = os.path.join(extract_dir, fname)
        result = analyze_file(fpath, compressed_dir)

        # Aplica CRC-4 à primeira linha do ficheiro como demo
        with open(fpath, 'rb') as f:
            first_byte = f.read(1)
            if first_byte:
                bin_str = f"{first_byte[0]:08b}"
                result["CRC4"] = crc4(bin_str)

        # Aplica checksum IP (usando os 3 primeiros bytes)
        with open(fpath, 'rb') as f:
            dados = list(f.read(3))
            if len(dados) == 3:
                result["Checksum"] = f"0x{ip_checksum(dados):04X}"

        # Aplica BSC
        fout = os.path.join(output_bsc_dir, fname)
        ber = bsc(fpath, fout, p=0.01)
        result["BER (p=0.01)"] = round(ber, 6)

        results.append(result)

    df = pd.DataFrame(results)
    print(df)

    csv_path = os.path.join(base_dir, "modulo2_resultados.csv")
    df.to_csv(csv_path, index=False)
    print(f"\nResultados guardados em: {csv_path}")

    plt.figure(figsize=(8, 5))
    plt.scatter(df["entropy (bits/symbol)"], df["compression ratio"], color='blue')
    plt.title("Entropia vs Compressão")
    plt.xlabel("Entropia (bits/symbol)")
    plt.ylabel("Compression Ratio")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(os.path.join(base_dir, "grafico_entropia_vs_compressao.png"))
    plt.show()

if __name__ == "__main__":
    main()
