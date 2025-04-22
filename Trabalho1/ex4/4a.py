import os
import zipfile
import math
import gzip
from collections import Counter
import pandas as pd
import matplotlib.pyplot as plt


def analyze_file(filepath, output_dir):
    with open(filepath, 'rb') as f:
        data = f.read()

    total = len(data)
    contagem = Counter(data)
    probs = [freq / total for freq in contagem.values()]
    entropia = -sum(p * math.log2(p) for p in probs)

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

if __name__ == "__main__":
    base_dir = os.path.dirname(__file__)
    zip_path = os.path.join(base_dir, "cantrbry.zip")
    extract_dir = os.path.join(base_dir, "cantrbry_extracted")
    compressed_dir = os.path.join(base_dir, "cantrbry_compressed")

    os.makedirs(extract_dir, exist_ok=True)
    os.makedirs(compressed_dir, exist_ok=True)

    # Extract ZIP
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extract_dir)

    results = []
    for fname in os.listdir(extract_dir):
        fpath = os.path.join(extract_dir, fname)
        result = analyze_file(fpath, compressed_dir)
        results.append(result)

    df = pd.DataFrame(results)
    pd.set_option('display.max_columns', None)
    print(df)

# Save to CSV
csv_path = os.path.join(base_dir, "compressao_resultados.csv")
df.to_csv(csv_path, index=False)
print(f"\nResults saved to: {csv_path}")

# Plot entropy vs compression ratio
plt.figure(figsize=(8, 5))
plt.scatter(df["entropy (bits/symbol)"], df["compression ratio"], color='blue')
plt.title("Entropy vs Compression Ratio")
plt.xlabel("Entropy (bits/symbol)")
plt.ylabel("Compression Ratio")
plt.grid(True)
plt.tight_layout()
plt.savefig(os.path.join(base_dir, "grafico_entropia_vs_compressao.png"))
plt.show()
