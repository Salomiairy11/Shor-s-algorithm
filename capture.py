import pyshark
from multiprocessing import Queue
import json

def safe_json_loads(data):
    try:
        if not data or not data.strip():  
            return None
        return json.loads(data)
    except json.JSONDecodeError:
        return None

def capture_tcp_packets(queue, interface, port=8000):
    try: 
        capture = pyshark.LiveCapture(
            interface=interface, 
            bpf_filter=f'tcp port {port}', 
            display_filter='websocket'
        )
        capture.sniff(timeout=2)    
        skip = False
        for i, packet in enumerate(capture):
            if skip:
                skip = False
                continue
                
            if hasattr(packet, 'websocket'):
                ws = packet.websocket
                payload_length = getattr(ws, 'payload_length', '0')
                payload_data = getattr(ws, 'payload_text', '')
                if int(payload_length) > 30:
                    skip = True
                    print(f"Packet {i+1}: Payload Length = {payload_length}, Payload = {payload_data}")
                    queue.put(payload_data)
    except KeyboardInterrupt:
        print("\nCapture stopped.")
        capture.close()

if __name__ == "__main__":
    queue = Queue()
    capture_tcp_packets(queue,interface=r"\Device\NPF_{A58318F4-6CC1-4328-B113-B6E19D5EDC18}",port=8000)
