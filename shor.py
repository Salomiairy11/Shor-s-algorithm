import streamlit as st
import base64
from qiskit.aqua.algorithms import Shor
from qiskit.aqua import QuantumInstance
from qiskit import Aer
from rsa import RSA as MyRSA
from aes import AES as MyAES
from aes import decrypt_cbc

def load_css(file_name):
    with open(file_name) as f:
        css = f.read()
        with open("bg.png", "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode()
            bg_image = f"data:image/png;base64,{encoded_string}"
            css = css.replace("REPLACE_WITH_IMAGE", bg_image)
        st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)

load_css("style.css")

def quantum_shor_factor(N):
    backend = Aer.get_backend('qasm_simulator')
    quantum_instance = QuantumInstance(backend, shots=50)
    
    shor_instance = Shor(N=N, quantum_instance=quantum_instance)
    result = shor_instance.run()
    
    # Access factors from the dictionary
    if 'factors' in result and result['factors']:
        p, q = result['factors'][0]
        if p * q == N and p > 1 and q > 1:
            return p, q
    return None, None

# st.form to properly contain all elements
with st.form("quantum_form"):
    # Title and subtitle
    st.markdown('<div class="form-title">Shor\'s Quantum Attack Demo</div>', unsafe_allow_html=True)
    st.markdown('<div class="form-subtitle">Break RSA encryption using quantum computing algorithms</div>', unsafe_allow_html=True)
    
    # Input fields
    N_str = st.text_input("Enter RSA modulus N", placeholder="Enter RSA modulus N (decimal)", key="n_input")
    enc_aes_key_b64 = st.text_input("Enter RSA-encrypted AES key", placeholder="Enter RSA-encrypted AES key (base64)", key="aes_key_input")
    enc_message_b64 = st.text_input("Enter AES-encrypted message", placeholder="Enter AES-encrypted message (base64)", key="message_input")
    
    # Form submit button
    submitted = st.form_submit_button("DECRYPT WITH SHOR")
    
    if submitted:
        if N_str and enc_aes_key_b64 and enc_message_b64:
            try:
                N = int(N_str)
                
                #convert the base64 to raw bytes
                enc_aes_key_bytes = base64.b64decode(enc_aes_key_b64)
                ciphertext_bytes = base64.b64decode(enc_message_b64)
                
                with st.spinner("Running Shor's quantum algorithm..."):
                    p, q = quantum_shor_factor(N)
                
                if not p or not q:
                    st.error("Failed to factor N using quantum algorithm")
                else:
                    st.markdown(f'<div class="result-text"><strong>Prime factors found:</strong> p = {p}, q = {q}</div>', unsafe_allow_html=True)
                    
                    phi = (p - 1) * (q - 1)
                    e = 3
                    #getting private key using public key
                    d = pow(e, -1, phi)
                    st.markdown(f'<div class="result-text"><strong>RSA Private Key:</strong> d = {d}</div>', unsafe_allow_html=True)
                    
                    #convert each byte to int 
                    aes_key_digits = list(map(int, enc_aes_key_bytes.decode().split(",")))
                    
                    #get decrypted AES Key in str form
                    rsa = MyRSA(publicKey={'e': e, 'n': N}, privateKey={'d': d, 'n': N})
                    decrypted_hex = rsa.decrypt(aes_key_digits)
                    decrypted_hex = decrypted_hex.zfill(32)  # pad to 32 hex chars = 16 bytes
                    
                    aes_key_int = int(decrypted_hex, 16)
                    aes = MyAES(aes_key_int)
                    
                    st.markdown(f'<div class="result-text"><strong>Recovered AES Key:</strong> {decrypted_hex}</div>', unsafe_allow_html=True)
                    
                    plaintext_bytes = decrypt_cbc(aes, ciphertext_bytes)
                    plaintext = plaintext_bytes.decode("utf-8", errors="ignore")
                    st.code(plaintext)
                    
            except Exception as err:
                st.error(f"Quantum decryption failed: {err}")
        else:
            st.error("Please fill in all required fields")
