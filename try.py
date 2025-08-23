import base64

from rsa import RSA
from aes import AES, decrypt_cbc

# 1️⃣ Decode RSA-encrypted AES key
enc_aes_key_bytes = base64.b64decode(
    "OCwxMCwxMywzLDAsNCwxLDUsOCw2LDExLDMsNyw4LDEwLDQsMTAsMTEsMTQsNiwxLDUsMiwyLDAsOSwzLDE0LDQsNywxMg=="
)

aes_key_digits = list(map(int, enc_aes_key_bytes.decode().split(",")))

# 2️⃣ Initialize RSA and decrypt AES key
rsa = RSA(publicKey={"e": 3, "n": 15}, privateKey={"d": 3, "n": 15})
decrypted_hex = rsa.decrypt(aes_key_digits)
decrypted_hex = decrypted_hex.zfill(32)  # pad to 32 hex chars = 16 bytes

print("Decrypted AES key (hex):", decrypted_hex)

# Convert hex key to integer for AES
aes_key_int = int(decrypted_hex, 16)
aes = AES(aes_key_int)

# 3️⃣ Decode AES-encrypted ciphertext
ciphertext_bytes = base64.b64decode(
    "pkuT8QgwNHJ4O6wqfYdxvzpB5fhfiaubyYpA9Li+grcekSCpM10gqdmlFJ4BBQOV"
)

print("Ciphertext bytes:", ciphertext_bytes)

# 4️⃣ Decrypt using AES CBC - pass AES instance and full ciphertext including IV
plaintext_bytes = decrypt_cbc(aes, ciphertext_bytes)

print("Plaintext bytes:", plaintext_bytes)

# 5️⃣ Decode bytes to string
plaintext = plaintext_bytes.decode("utf-8", errors="ignore")

print("Decrypted message:", plaintext)
