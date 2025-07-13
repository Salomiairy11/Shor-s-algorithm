from aes import AES
from rsa import RSA
import base64

# 1. AES key and plaintext
key_hex = "2b7e151628aed2a6abf7158809cf4f3c"  # 16 bytes, 32 hex chars
key_int = int(key_hex, 16)
aes = AES(key_int)

plaintext = b'i am fine' + b'\x00' * (16 - len('i am fine'))  # pad to 16 bytes
plaintext_int = int.from_bytes(plaintext, 'big')

# 2. AES encryption
cipher_int = aes.encrypt(plaintext_int)
cipher_bytes = cipher_int.to_bytes(16, 'big')
cipher_b64 = base64.b64encode(cipher_bytes).decode()

print("AES-encrypted message (base64):", cipher_b64)

# 3. RSA-encrypt the AES key (digit-by-digit)
rsa = RSA(publicKey={"e": 5, "n": 35})  # Use your toy RSA's public key
cipher_chunks = rsa.encrypt(key_hex)     # List of integers, one per hex digit

# Turn each chunk into a byte
rsa_enc_aes_key_bytes = bytes(cipher_chunks)
rsa_enc_aes_key_b64 = base64.b64encode(rsa_enc_aes_key_bytes).decode()

print("RSA-encrypted AES key (base64):", rsa_enc_aes_key_b64)

# 4. IV (16 bytes of zero)
iv_bytes = b'\x00' * 16
iv_b64 = base64.b64encode(iv_bytes).decode()

print("AES IV (base64):", iv_b64)
