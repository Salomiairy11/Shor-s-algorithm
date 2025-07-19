import streamlit as st
import base64
from math import gcd
from qiskit.aqua.algorithms import Shor
from qiskit.aqua import QuantumInstance
from qiskit import Aer
from rsa import RSA as MyRSA
from aes import AES as MyAES

def set_custom_background():
    # Try to encode the background image as base64
    with open("bg.png", "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode()
        bg_image = f"data:image/png;base64,{encoded_string}"
    
    st.markdown(
        f"""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
        
        
        .stApp {{
            background: transparent;
        }}
        
        .stApp::before {{
            content: "";
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background-image: url("{bg_image}");
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            filter: blur(3px) brightness(0.7);
            z-index: -1;
        }}
        
        header[data-testid="stHeader"] {{
            display: none;
        }}
       
        .main .block-container {{
            padding: 2rem;
            max-width: 600px;
            margin: 0 auto;
        }}
        
        div[data-testid="stForm"] {{
            background: rgba(0, 0, 0, 0.4) !important;
            backdrop-filter: blur(20px) !important;
            -webkit-backdrop-filter: blur(20px) !important;
            border: 1px solid rgba(255, 255, 255, 0.1) !important;
            border-radius: 24px !important;
            padding: 2.5rem !important;
            margin: 2rem auto !important;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3) !important;
            font-family: 'Inter', sans-serif !important;
        }}
        
        .form-title {{
            color: white !important;
            font-size: 2.2rem !important;
            font-weight: 600 !important;
            margin-bottom: 0.5rem !important;
            text-align: center !important;
            white-space: nowrap !important;
        }}
        
        .form-subtitle {{
            color: rgba(255, 255, 255, 0.7) !important;
            font-size: 0.9rem !important;
            margin-bottom: 2rem !important;
            line-height: 1.4 !important;
            text-align: center !important;
        }}
        
        /* Input field styling - target within form */
        div[data-testid="stForm"] div[data-testid="stTextInput"] {{
            margin-bottom: 1rem !important;
        }}
        
        div[data-testid="stForm"] div[data-testid="stTextInput"] > label {{
            display: none !important;
        }}
        
        div[data-testid="stForm"] div[data-testid="stTextInput"] input {{
            background: rgba(255, 255, 255, 0.1) !important;
            border: 1px solid rgba(255, 255, 255, 0.2) !important;
            border-radius: 25px !important;
            color: white !important;
            padding: 0.8rem 1.2rem !important;
            font-size: 0.9rem !important;
            font-family: 'Inter', sans-serif !important;
        }}
        
        div[data-testid="stForm"] div[data-testid="stTextInput"] input::placeholder {{
            color: black;
        }}
        
        div[data-testid="stForm"] div[data-testid="stTextInput"] input:focus {{
            border-color: rgba(76, 175, 80, 0.5) !important;
            box-shadow: 0 0 0 2px rgba(76, 175, 80, 0.2) !important;
            outline: none !important;
        }}
        
        /* Form submit button styling */
        div[data-testid="stForm"] div[data-testid="stFormSubmitButton"] > button {{
            background: linear-gradient(135deg, #4CAF50 0%, #45a049 100%) !important;
            color: white !important;
            border: none !important;
            border-radius: 25px !important;
            padding: 0.8rem 2rem !important;
            font-weight: 600 !important;
            font-size: 0.95rem !important;
            width: 100% !important;
            margin-top: 1rem !important;
            transition: all 0.3s ease !important;
            font-family: 'Inter', sans-serif !important;
        }}
        
        div[data-testid="stForm"] div[data-testid="stFormSubmitButton"] > button:hover {{
            transform: translateY(-2px) !important;
            box-shadow: 0 8px 25px rgba(76, 175, 80, 0.3) !important;
        }}
        
        /* Results styling */
        .result-text {{
            color: white !important;
            background: rgba(255, 255, 255, 0.1) !important;
            padding: 1rem !important;
            border-radius: 12px !important;
            margin: 1rem 0 !important;
            border: 1px solid rgba(255, 255, 255, 0.1) !important;
        }}
        
        /* Code block styling */
        div[data-testid="stCode"] {{
            background: rgba(0, 0, 0, 0.6) !important;
            border: 1px solid rgba(76, 175, 80, 0.3) !important;
            border-radius: 12px !important;
        }}
        
        /* Error styling */
        div[data-testid="stAlert"] {{
            background: rgba(244, 67, 54, 0.2) !important;
            border: 1px solid rgba(244, 67, 54, 0.3) !important;
            border-radius: 12px !important;
            color: white !important;
        }}
        
        /* Spinner styling */
        div[data-testid="stSpinner"] > div {{
            border-color: #4CAF50 !important;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

set_custom_background()

def quantum_shor_factor(N):
    backend = Aer.get_backend('qasm_simulator')
    quantum_instance = QuantumInstance(backend, shots=20)
    
    for a in range(2, min(N, 10)):
        if gcd(a, N) != 1:
            factor = gcd(a, N)
            return factor, N // factor
        
        shor_instance = Shor(N=N, a=a, quantum_instance=quantum_instance)
        result = shor_instance.run()
        
        if hasattr(result, 'factors') and result.factors:
            factors = result.factors[0]
            if len(factors) == 2:
                p, q = factors
                if p * q == N and p > 1 and q > 1:
                    return p, q
    
    return None, None

# Use st.form to properly contain all elements
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
                enc_aes_key_bytes = base64.b64decode(enc_aes_key_b64)
                ciphertext_bytes = base64.b64decode(enc_message_b64)
                
                with st.spinner("Running Shor's quantum algorithm..."):
                    p, q = quantum_shor_factor(N)
                
                if not p or not q:
                    st.error("Failed to factor N using quantum algorithm")
                else:
                    st.markdown(f'<div class="result-text"><strong>Prime factors found:</strong> p = {p}, q = {q}</div>', unsafe_allow_html=True)
                    
                    phi = (p - 1) * (q - 1)
                    e = 5
                    d = pow(e, -1, phi)
                    
                    st.markdown(f'<div class="result-text"><strong>RSA Private Key:</strong> d = {d}</div>', unsafe_allow_html=True)
                    
                    ciphertext_digits = [int(b) for b in enc_aes_key_bytes]
                    rsa = MyRSA(publicKey={'e': e, 'n': N}, privateKey={'d': d, 'n': N})
                    decrypted_hex = rsa.decrypt(ciphertext_digits)
                    aes_key_bytes = bytes.fromhex(decrypted_hex)
                    
                    st.markdown(f'<div class="result-text"><strong>Recovered AES Key:</strong> {aes_key_bytes.hex()}</div>', unsafe_allow_html=True)
                    
                    key_int = int.from_bytes(aes_key_bytes, byteorder='big')
                    cipher_int = int.from_bytes(ciphertext_bytes, byteorder='big')
                    aes = MyAES(key_int)
                    decrypted = aes.decrypt(cipher_int)
                    plaintext_bytes = decrypted.to_bytes((decrypted.bit_length() + 7) // 8, byteorder='big')
                    plaintext = plaintext_bytes.decode(errors='ignore')
                    st.code(plaintext)
                    
            except Exception as err:
                st.error(f"Quantum decryption failed: {err}")
        else:
            st.error("Please fill in all required fields")
