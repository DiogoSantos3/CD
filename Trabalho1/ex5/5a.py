import os  # Module used to work with file paths

# Function that applies a Vigenère-style encryption using XOR
# It cycles through the key and XORs each byte of the data with a byte from the key
def vigenere_encrypt(data: bytes, key: bytes) -> bytes:
    return bytes((b ^ key[i % len(key)]) for i, b in enumerate(data))

# Encrypts a file using the vigenere_encrypt function
def encrypt_file(input_path: str, output_path: str, key: str):
    with open(input_path, 'rb') as f:  # Open input file in binary read mode
        data = f.read()  # Read entire file contents
    encrypted = vigenere_encrypt(data, key.encode())  # Encrypt using key
    with open(output_path, 'wb') as f:  # Open output file in binary write mode
        f.write(encrypted)  # Write encrypted data to output

# Decrypts a file by reusing the same encrypt function
# Since XOR is symmetric, encryption and decryption are identical
def decrypt_file(input_path: str, output_path: str, key: str):
    encrypt_file(input_path, output_path, key)

# Main execution block
if __name__ == "__main__":
    key = "leic2025"  # Encryption key

    base_dir = os.path.dirname(__file__)  # Get current directory

    # List of files to encrypt and decrypt
    files = ["alice29.txt", "fields.c"]
    for fname in files:
        # Build full paths for original, encrypted, and decrypted files
        original_path = os.path.join(base_dir, fname)
        encrypted_path = os.path.join(base_dir, f"{fname}.enc")
        decrypted_path = os.path.join(base_dir, f"{fname}.dec")

        # Encrypt original file and write to .enc file
        encrypt_file(original_path, encrypted_path, key)

        # Decrypt .enc file and write to .dec file
        decrypt_file(encrypted_path, decrypted_path, key)

        # Confirm result
        print(f"Encrypted and decrypted {fname}")
