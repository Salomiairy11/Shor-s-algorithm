import streamlit as st
import json
from finalShor import get_decrypted_values
import time

def load_css(file_name):
    with open(file_name) as f:
        css = f.read()
        st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)

load_css("shor.css")

terminal_placeholder = st.empty()
terminal_lines = []
last_index = -1

while True:
    with open ("packets.txt","rb") as f:
        data = f.read().decode()
        if not data:
            f.close()
            continue
        packet = json.loads(data)
        current_index = packet[0]["index"]
        if current_index > last_index:
            for pkt in packet: 
                loading_text = f"<span class='spinner-red'></span><span class='loading-text'>Getting decrypted text...</span>\n\n"
                # loading_text = (
                #     "<span class='spinner-red'></span>"
                #     "<span class='loading-text'>Getting decrypted text...</span><br><br>"
                # )
                terminal_lines.append(loading_text)
                terminal_output = "\n".join(terminal_lines)
                terminal_placeholder.markdown(f'<div class="terminal"><pre>{terminal_output}</pre></div>', unsafe_allow_html=True)
                time.sleep(0.5)
                
                result = get_decrypted_values(pkt.get("enc_key"), pkt.get("content"))
                
                terminal_lines.pop() 
                formatted = "\n".join([f"<span class='prompt'>></span> {k}: {v}" for k, v in result.items()])
                formatted = f"<span class='packet-header'>--- DECRYPTED A PACKET ---</span>\n{formatted}\n\n"
                terminal_lines.append(formatted)
                terminal_output = "\n".join(terminal_lines)
                terminal_placeholder.markdown(f'<div class="terminal"><pre>{terminal_output}</pre></div>', unsafe_allow_html=True)
            last_index = current_index 
        else:
            pass