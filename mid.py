import streamlit as st
import base64
from math import gcd
from rsa import RSA as MyRSA
from aes import AES as MyAES

st.title("Shor's Quantum Attack Demo")

N_str = st.text_input("Enter RSA modulus N (decimal):")
enc_aes_key_b64 = st.text_input("Enter RSA-encrypted AES key (base64):")
enc_message_b64 = st.text_input("Enter AES-encrypted message (base64):")
iv_b64 = "AAAAAAAAAAAAAAAAAAAAAA=="


if st.button("Decrypt"):
    try:
        N = int(N_str)
        enc_aes_key_bytes = base64.b64decode(enc_aes_key_b64)
        ciphertext_bytes = base64.b64decode(enc_message_b64)
        iv_bytes = base64.b64decode(iv_b64)

        # Factor RSA modulus N
        def find_order(a, N):
            seen = {}
            x = 1
            for r in range(1, N):
                x = (x * a) % N
                if x in seen:
                    return r - seen[x]
                seen[x] = r
            return None

        def shor_factor(N):
            for a in range(2, N):
                if gcd(a, N) != 1:
                    return gcd(a, N), N // gcd(a, N)
                r = find_order(a, N)
                if r and r % 2 == 0:
                    factor1 = gcd(pow(a, r//2) - 1, N)
                    factor2 = gcd(pow(a, r//2) + 1, N)
                    if factor1 * factor2 == N:
                        return factor1, factor2
            return None, None

        p, q = shor_factor(N)
        if not p or not q:
            st.error("Failed to factor N.")
        else:
            phi = (p - 1) * (q - 1)
            e = 5
            d = pow(e, -1, phi)

            st.write(f"**RSA Private Exponent d:** `{d}`")

            # Decrypt AES key using custom RSA
            ciphertext_digits = [int(b) for b in enc_aes_key_bytes]
            rsa = MyRSA(publicKey={'e': e, 'n': N}, privateKey={'d': d, 'n': N})
            decrypted_hex = rsa.decrypt(ciphertext_digits)
            aes_key_bytes = bytes.fromhex(decrypted_hex)

            st.write(f"**Recovered AES Key:** `{aes_key_bytes.hex()}`")

            # Decrypt AES-encrypted message using custom AES
            key_int = int.from_bytes(aes_key_bytes, byteorder='big')
            cipher_int = int.from_bytes(ciphertext_bytes, byteorder='big')
            aes = MyAES(key_int)
            decrypted = aes.decrypt(cipher_int)
            plaintext_bytes = decrypted.to_bytes((decrypted.bit_length() + 7) // 8, byteorder='big')
            plaintext = plaintext_bytes.decode(errors='ignore')

            st.write("**Decrypted Message:**")
            st.code(plaintext)

    except Exception as err:
        st.error(f"Something went wrong: {err}")
