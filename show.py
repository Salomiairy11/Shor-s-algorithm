from multiprocessing import Process, Queue
import streamlit as st
from capture import capture_tcp_packets
import json
import streamlit.components.v1 as components

def load_css(file_name):
        with open(file_name) as f:
            css = f.read()
            st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)

if __name__ == "__main__":
    
    st.set_page_config(
        page_title="Shor's Attack Demo", 
        layout="wide",
        initial_sidebar_state="collapsed"
    )
    
    load_css("main_page.css")

    interface = r"\Device\NPF_Loopback"
    #interface = r"\Device\NPF_{A58318F4-6CC1-4328-B113-B6E19D5EDC18}"

    packet_queue = Queue(1)
    
    if 'capturing' not in st.session_state:
        st.session_state.capturing = False
    if 'packet_count' not in st.session_state:
        st.session_state.packet_count = 0
    
    terminal_lines = []
    packet_counter_placeholder = st.empty()
    
    c1, c2, c3 = st.columns([1,2,1])
    with c2:
        button_text = "Stop Capturing" if st.session_state.capturing else "Capture Data"
        if st.button(button_text):
            st.session_state.capturing = not st.session_state.capturing
    
    if st.session_state.capturing:
        packet_counter_placeholder.markdown(f"""
        <div class="packet-counter">Packets Captured: {st.session_state.packet_count}</div>
        <div style="color: #00FF00; font-family: 'Courier New', monospace;">
            <span class="spinner"></span>Capturing TCP packets on {interface}:8000...
        </div>
        """, unsafe_allow_html=True)

        capture_process = Process(target=capture_tcp_packets, args=(packet_queue, interface, 8000))
        capture_process.start()
        
        col1, col2 = st.columns([1, 1])
        with col1:
            terminal_placeholder = st.empty()
            
        with col2:
            iframe_code = """
            <div style="
                width: 99vw; 
                height: 99vh; 
                border-radius: 20px; 
                overflow: hidden; 
                margin: 0; 
                padding: 0;
                box-shadow: 0 0 10px rgba(0,0,0,0.2); /* optional shadow */
            ">
            <iframe src="http://localhost:8502" 
                style="border:none; width:100%; height:100%;" 
                frameborder="0" 
                scrolling="no">
            </iframe>
            """
            components.html(iframe_code, height=690)
            
        index = 1
        try:    
            while st.session_state.capturing:
                pkt = packet_queue.get()
                if pkt:
                    try:
                        payload_dict = json.loads(pkt.replace("'", '"'))
                        extracted = {
                            "enc_key": payload_dict.get("enc_key"),
                            "content": payload_dict.get("content"),
                            "sender_id": payload_dict.get("sender_id"),
                            "receiver_id": payload_dict.get("receiver_id"),
                            "rsa_mod": payload_dict.get("rsa_mod")
                        }
                        to_write = dict(extracted)
                        to_write["index"] = index
                        
                        with open("packets.txt", "wb") as f:
                            f.write(json.dumps([to_write]).encode())
                        
                        st.session_state.packet_count = index
                        index += 1
                        
                        formatted = "\n".join([f"<span class='prompt'>></span> {k}: {v}" for k, v in extracted.items()])
                        formatted = f"<span class='packet-header-captured'>--- CAPTURED A PACKET ---</span>\n{formatted}\n\n"
                        terminal_lines.append(formatted)
                        terminal_output = "\n".join(terminal_lines)
                        terminal_placeholder.markdown(f'<div class="terminal"><pre>{terminal_output}</pre></div>', unsafe_allow_html=True)

                    except Exception as e:
                        st.error(f"Quantum decryption failed: {e}")
        
        except KeyboardInterrupt:
            capture_process.terminate()
            st.warning("Capture stopped.")
            st.session_state.capturing = False
            exit(1)
    
    st.markdown("---")
    st.markdown("""<div style="text-align: center; color: #00ff00; font-family: 'Courier New', monospace; font-size: 0.8rem;">
        🔒 SECURE CONNECTION ESTABLISHED | PACKET ANALYSIS IN PROGRESS | SYSTEM STATUS: OPERATIONAL
    </div>""", unsafe_allow_html=True)