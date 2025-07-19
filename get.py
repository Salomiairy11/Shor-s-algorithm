from aes import AES
from rsa import RSA
import base64

# 1. AES key and plaintext
key_hex = "2b7e151628aed2a6abf7158809cf4f3c"  # 16 bytes, 32 hex chars
key_int = int(key_hex, 16)
aes = AES(key_int)

plaintext = b'hello rojal' + b'\x00' * (16 - len('hello rojal'))  # pad to 16 bytes
plaintext_int = int.from_bytes(plaintext, 'big')

# 2. AES encryption
cipher_int = aes.encrypt(plaintext_int)
cipher_bytes = cipher_int.to_bytes(16, 'big')
cipher_b64 = base64.b64encode(cipher_bytes).decode()

print("AES-encrypted message (base64):", cipher_b64)

# 3. RSA-encrypt the AES key (digit-by-digit) with N=21
# N=21 = 3×7, φ(21) = 2×6 = 12, e=5, d=5 (since 5×5 ≡ 1 mod 12)
rsa = RSA(publicKey={"e": 5, "n": 21})  # Using N=21 to allow all hex digits 0-f
cipher_chunks = rsa.encrypt(key_hex)     # List of integers, one per hex digit

# Turn each chunk into a byte
rsa_enc_aes_key_bytes = bytes(cipher_chunks)
rsa_enc_aes_key_b64 = base64.b64encode(rsa_enc_aes_key_bytes).decode()

print("RSA-encrypted AES key (base64):", rsa_enc_aes_key_b64)

# 4. IV (16 bytes of zero)
iv_bytes = b'\x00' * 16
iv_b64 = base64.b64encode(iv_bytes).decode()

print("AES IV (base64):", iv_b64)

print("\n=== For use in Streamlit app ===")
print("RSA modulus N: 21")
print(f"RSA-encrypted AES key (base64): {rsa_enc_aes_key_b64}")
print(f"AES-encrypted message (base64): {cipher_b64}")
print(f"AES IV (base64): {iv_b64}")
