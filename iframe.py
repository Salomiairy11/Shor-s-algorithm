import streamlit as st
import json
from finalShor import get_decrypted_values
import time
import os 

def load_css(file_name):
    with open(file_name) as f:
        css = f.read()
        st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)

load_css("iframe.css")

terminal_placeholder = st.empty()
terminal_lines = []
last_index = -1

waiting_text = f"<span class='spinner-red'></span><span class='loading-text'>Waiting For Messages...</span>\n\n"
terminal_lines = [waiting_text]  
terminal_output = "\n".join(terminal_lines)
terminal_placeholder.markdown(f'<div class="terminal"><pre>{terminal_output}</pre></div>', unsafe_allow_html=True)

time.sleep(50)

terminal_lines[0] = f"<span class='spinner-red'></span><span class='loading-text'>Running Shor's Algorithm...</span>\n\n"
terminal_output = "\n".join(terminal_lines)
terminal_placeholder.markdown(f'<div class="terminal"><pre>{terminal_output}</pre></div>', unsafe_allow_html=True)


while True:    
    with open ("packets.txt","rb") as f:
        data = f.read().decode()
        if not data:
            f.close()
            continue
        packet = json.loads(data)
        current_index = packet[0]["index"]
        if current_index > last_index:
            mode = packet[0]["enc"]
            for pkt in packet:
                if mode == "rsa": 
                        result = get_decrypted_values(pkt.get("enc_key"), pkt.get("content"))
                        formatted = "\n".join([f"<span class='prompt'>></span> {k}: {v}" for k, v in result.items()])
                        formatted = f"<span class='packet-header-captured blink-effect'>--- DECRYPTED A PACKET ---</span>\n{formatted}\n\n"
                        terminal_lines.append(formatted)
                else:
                    error_message = f"<span class='error-header blink-effect'>--- CRYPTOGRAPHIC EXCEPTION ---</span><br>" \
                            f"<span class='prompt'>>&nbsp;</span> Detected encryption scheme: {mode}<br>" \
                            f"<span class='prompt'>>&nbsp;</span> [FATAL] Attempted decryption aborted.<br>" \
                            f"<span class='prompt'>>&nbsp;</span> Reason: ML-KEM decryption is NP-hard; brute-force recovery infeasible.<br>" \
                            f"<span class='prompt'>>&nbsp;</span> Hint: Use supported asymmetric algorithm (e.g., RSA) for decryption.<br>" \
                            f"<span class='prompt'>>&nbsp;</span> StackTrace: MLKEMDecryptor -> validate_scheme -> abort()"
                    terminal_lines.append(error_message)
                
                terminal_output = "\n".join(terminal_lines)
                terminal_placeholder.markdown(f'<div class="terminal">{terminal_output}</div>', unsafe_allow_html=True)

                
                last_index = current_index       
        else:
            pass