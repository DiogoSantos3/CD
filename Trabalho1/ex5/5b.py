import os  # Module to handle file system paths
import math  # Provides the log2 function used in entropy calculation
from collections import Counter  # Used to count byte frequencies
import matplotlib.pyplot as plt  # Used to generate and display/save histograms

# Function to calculate the Shannon entropy of a byte sequence
def calculate_entropy(data: bytes) -> float:
    total = len(data)  # Total number of bytes
    # Compute probabilities of each unique byte
    probs = [count / total for count in Counter(data).values()]
    # Return Shannon entropy formula: -∑p * log2(p)
    return -sum(p * math.log2(p) for p in probs)

# Function to generate and save a histogram of byte frequencies
def plot_histogram(data: bytes, title: str):
    counts = Counter(data)  # Count occurrences of each byte
    plt.figure(figsize=(10, 4))  # Create a new figure with defined size
    plt.bar(counts.keys(), counts.values(), width=1.0)  # Bar chart
    plt.title(title)
    plt.xlabel("Byte Value")
    plt.ylabel("Frequency")
    plt.grid(True)
    plt.tight_layout()

    # Define output folder and ensure it exists
    output_dir = os.path.join(os.path.dirname(__file__), "histograms")
    os.makedirs(output_dir, exist_ok=True)

    # Save the histogram to a file with a filename based on the title
    filename = os.path.join(output_dir, f"{title.replace(' ', '_')}.png")
    plt.savefig(filename)

    # Display the plot interactively
    plt.show()
    plt.close()  # Close the figure to free memory

# Function to analyze a file: calculate entropy and generate histogram
def analyze_file(path: str, label: str):
    with open(path, "rb") as f:
        data = f.read()  # Read file in binary mode
    entropy = calculate_entropy(data)  # Calculate entropy
    print(f"{label} - Entropy: {entropy:.4f} bits/symbol")
    plot_histogram(data, f"{label} - Histogram")  # Plot and save histogram

# Main execution block
if __name__ == "__main__":
    base = os.path.dirname(__file__)  # Get current script directory
    files = ["alice29.txt", "fields.c"]  # Files to analyze

    for fname in files:
        # Define paths for original, encrypted, and decrypted versions
        original = os.path.join(base, fname)
        encrypted = os.path.join(base, f"{fname}.enc")
        decrypted = os.path.join(base, f"{fname}.dec")

        print(f"\nAnalyzing: {fname}")
        # Analyze original, encrypted, and decrypted versions of each file
        analyze_file(original, f"{fname} - Original")
        analyze_file(encrypted, f"{fname} - Encrypted")
        analyze_file(decrypted, f"{fname} - Decrypted")
