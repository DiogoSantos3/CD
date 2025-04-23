import os
import math
from collections import Counter
import matplotlib.pyplot as plt

def calculate_entropy(data: bytes) -> float:
    total = len(data)
    probs = [count / total for count in Counter(data).values()]
    return -sum(p * math.log2(p) for p in probs)

def plot_histogram(data: bytes, title: str):
    counts = Counter(data)
    plt.figure(figsize=(10, 4))
    plt.bar(counts.keys(), counts.values(), width=1.0)
    plt.title(title)
    plt.xlabel("Byte Value")
    plt.ylabel("Frequency")
    plt.grid(True)
    plt.tight_layout()

    output_dir = os.path.join(os.path.dirname(__file__), "histograms")
    os.makedirs(output_dir, exist_ok=True)

    filename = os.path.join(output_dir, f"{title.replace(' ', '_')}.png")
    plt.savefig(filename)

    plt.show()
    plt.close()

def analyze_file(path: str, label: str):
    with open(path, "rb") as f:
        data = f.read()
    entropy = calculate_entropy(data)
    print(f"{label} - Entropy: {entropy:.4f} bits/symbol")
    plot_histogram(data, f"{label} - Histogram")

if __name__ == "__main__":
    base = os.path.dirname(__file__)
    files = ["alice29.txt", "fields.c"]

    for fname in files: 
        original = os.path.join(base, fname)
        encrypted = os.path.join(base, f"{fname}.enc")
        decrypted = os.path.join(base, f"{fname}.dec")

        print(f"\nAnalyzing: {fname}")
        analyze_file(original, f"{fname} - Original")
        analyze_file(encrypted, f"{fname} - Encrypted")
        analyze_file(decrypted, f"{fname} - Decrypted")

