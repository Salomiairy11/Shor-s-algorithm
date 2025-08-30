import streamlit as st
import base64
from qiskit.aqua.algorithms import Shor
from qiskit.aqua import QuantumInstance
from qiskit import Aer
from rsa import RSA as MyRSA
from aes import AES as MyAES
from aes import decrypt_cbc

def quantum_shor_factor(N):
    backend = Aer.get_backend('qasm_simulator')
    quantum_instance = QuantumInstance(backend, shots=50)
    
    shor_instance = Shor(N=N, quantum_instance=quantum_instance)
    result = shor_instance.run()
    
    if 'factors' in result:
        p, q = result['factors'][0]
        if p * q == N and p > 1 and q > 1:
            return p, q
    return None, None

N_str = 15
def get_decrypted_values (enc_aes_key_b64, enc_message_b64):
    try:
        N = int(N_str)
        enc_aes_key_bytes = base64.b64decode(enc_aes_key_b64)
        ciphertext_bytes = base64.b64decode(enc_message_b64)
        
        p, q = quantum_shor_factor(N)
        
        print(f'p::: {p}')
        print(f'q::: {q}')
        if not p or not q:
            
            raise ValueError("Failed to factor N using quantum algorithm")
        else:
            phi = (p - 1) * (q - 1)
            e = 3
            d = pow(e, -1, phi)
            
            
            aes_key_digits = list(map(int, enc_aes_key_bytes.decode().split(",")))
            
            rsa = MyRSA(publicKey={'e': e, 'n': N}, privateKey={'d': d, 'n': N})
            decrypted_hex = rsa.decrypt(aes_key_digits)
            decrypted_hex = decrypted_hex.zfill(32) 
            
            print(f'decrypted_hex::: {decrypted_hex}')
            aes_key_int = int(decrypted_hex, 16)
            aes = MyAES(aes_key_int)
            
            
            plaintext_bytes = decrypt_cbc(aes, ciphertext_bytes)
            plaintext = plaintext_bytes.decode("utf-8", errors="ignore")
            result =  {
                "rsa_private_key":[d,N],
                "aes_decrypted_key":decrypted_hex,
                "decrypted_text":plaintext
            }
            
            return result  
           
    except Exception as err:
       
        print(f"Quantum decryption failed: {err}")
        raise err

if __name__ == "__main__":
    result =  get_decrypted_values("OCwxMCwxMywzLDAsNCwxLDUsOCw2LDExLDMsNyw4LDEwLDQsMTAsMTEsMTQsNiwxLDUsMiwyLDAsOSwzLDE0LDQsNywxMg==","mtZqUJSCWEGjJg9WN4TF2XJy3E8+TdRmasUbiDY4Bc0=") 
    print(result)