import os  # File system path utilities
import zipfile  # To extract ZIP files
import math  # For log2 function used in entropy calculation
import gzip  # For compressing files using gzip
from collections import Counter  # To count byte frequencies
import pandas as pd  # For tabular data manipulation
import matplotlib.pyplot as plt  # For plotting

# Function to analyze a file: compute entropy and compress it
def analyze_file(filepath, output_dir):
    with open(filepath, 'rb') as f:
        data = f.read()  # Read the entire file as bytes

    total = len(data)  # Total number of bytes
    contagem = Counter(data)  # Count the frequency of each byte value
    probs = [freq / total for freq in contagem.values()]  # Compute probabilities
    entropia = -sum(p * math.log2(p) for p in probs)  # Shannon entropy

    # Compress the file using gzip
    filename = os.path.basename(filepath)
    compressed_path = os.path.join(output_dir, f"{filename}.gz")
    with gzip.open(compressed_path, 'wb') as f_out:
        f_out.write(data)

    compressed_size = os.path.getsize(compressed_path)

    # Return analysis results as a dictionary
    return {
        "filename": filename,
        "original size (bytes)": total,
        "compressed size (bytes)": compressed_size,
        "compression ratio": round(total / compressed_size, 4),
        "entropy (bits/symbol)": round(entropia, 4)
    }

# Main execution block
if __name__ == "__main__":
    base_dir = os.path.dirname(__file__)  # Get current directory
    zip_path = os.path.join(base_dir, "cantrbry.zip")  # Path to ZIP archive
    extract_dir = os.path.join(base_dir, "cantrbry_extracted")  # Extraction output directory
    compressed_dir = os.path.join(base_dir, "cantrbry_compressed")  # Where to store compressed files

    # Ensure output folders exist
    os.makedirs(extract_dir, exist_ok=True)
    os.makedirs(compressed_dir, exist_ok=True)

    # Extract the contents of the ZIP archive
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extract_dir)

    results = []  # List to store analysis results
    for fname in os.listdir(extract_dir):  # Loop through all extracted files
        fpath = os.path.join(extract_dir, fname)
        result = analyze_file(fpath, compressed_dir)  # Analyze each file
        results.append(result)

    # Convert results to a DataFrame for easier viewing
    df = pd.DataFrame(results)
    pd.set_option('display.max_columns', None)
    print(df)  # Print the table to console

# Save the DataFrame to a CSV file
csv_path = os.path.join(base_dir, "compressao_resultados.csv")
df.to_csv(csv_path, index=False)
print(f"\nResults saved to: {csv_path}")

# Plot entropy vs. compression ratio
plt.figure(figsize=(8, 5))
plt.scatter(df["entropy (bits/symbol)"], df["compression ratio"], color='blue')
plt.title("Entropy vs Compression Ratio")
plt.xlabel("Entropy (bits/symbol)")
plt.ylabel("Compression Ratio")
plt.grid(True)
plt.tight_layout()
# Save the plot to a PNG file
plt.savefig(os.path.join(base_dir, "grafico_entropia_vs_compressao.png"))
plt.show()
