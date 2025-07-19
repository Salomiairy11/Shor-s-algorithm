import streamlit as st
import base64
from math import gcd
from qiskit.aqua.algorithms import Shor
from qiskit.aqua import QuantumInstance
from qiskit import Aer
from rsa import RSA as MyRSA
from aes import AES as MyAES

st.title("Shor's Quantum Attack Demo")

N_str = st.text_input("Enter RSA modulus N (decimal):")
enc_aes_key_b64 = st.text_input("Enter RSA-encrypted AES key (base64):")
enc_message_b64 = st.text_input("Enter AES-encrypted message (base64):")
iv_b64 = "AAAAAAAAAAAAAAAAAAAAAA=="

def quantum_shor_factor(N):
    """
    Use Qiskit's Shor algorithm to factor N
    """
    # Set up quantum backend
    backend = Aer.get_backend('qasm_simulator')
    quantum_instance = QuantumInstance(backend, shots=5)
    
    # Try different values of 'a' for Shor's algorithm
    for a in range(2, min(N, 10)):
        if gcd(a, N) != 1:
            factor = gcd(a, N)
            return factor, N // factor
        
        # Create Shor instance
        shor_instance = Shor(N=N, a=a, quantum_instance=quantum_instance)
        
        # Run Shor's algorithm
        result = shor_instance.run()
        
        # Extract factors from result
        if hasattr(result, 'factors') and result.factors:
            factors = result.factors[0]
            if len(factors) == 2:
                p, q = factors
                if p * q == N and p > 1 and q > 1:
                    return p, q
    return None, None

if st.button("Decrypt"):
    try:
        N = int(N_str)
        enc_aes_key_bytes = base64.b64decode(enc_aes_key_b64)
        ciphertext_bytes = base64.b64decode(enc_message_b64)
        iv_bytes = base64.b64decode(iv_b64)

        # Use quantum Shor's algorithm to factor RSA modulus N
        p, q = quantum_shor_factor(N)
        
        if not p or not q:
            st.error("Failed to factor N.")
        else:
            st.write(f"**Prime factors:** p = {p}, q = {q}")
            
            # Calculate private key
            phi = (p - 1) * (q - 1)
            e = 5  # Changed to e=5 for N=21
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
