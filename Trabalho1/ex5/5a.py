import os

def vigenere_encrypt(data: bytes, key: bytes) -> bytes:
    return bytes((b ^ key[i % len(key)]) for i, b in enumerate(data))

def encrypt_file(input_path: str, output_path: str, key: str):
    with open(input_path, 'rb') as f:
        data = f.read()
    encrypted = vigenere_encrypt(data, key.encode())
    with open(output_path, 'wb') as f:
        f.write(encrypted)

def decrypt_file(input_path: str, output_path: str, key: str):
    encrypt_file(input_path, output_path, key)


if __name__ == "__main__":
    key = "leic2025"

    base_dir = os.path.dirname(__file__)

    # Files to test
    files = ["alice29.txt", "fields.c"]
    for fname in files:
        original_path = os.path.join(base_dir, fname)
        encrypted_path = os.path.join(base_dir, f"{fname}.enc")
        decrypted_path = os.path.join(base_dir, f"{fname}.dec")

        encrypt_file(original_path, encrypted_path, key)
        decrypt_file(encrypted_path, decrypted_path, key)

        print(f"Encrypted and decrypted {fname}")
