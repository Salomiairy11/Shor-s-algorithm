import pyshark
from multiprocessing import Queue

def capture_tcp_packets(queue, interface, port=8000):
    try: 
        capture = pyshark.LiveCapture(
            interface=interface, 
            bpf_filter=f'tcp port {port}', 
            display_filter='websocket'
        )
        capture.sniff(timeout=2)
        for i, packet in enumerate(capture):
            if hasattr(packet, 'websocket'):
                ws = packet.websocket
                payload_length = getattr(ws, 'payload_length', '0')
                payload_data = getattr(ws, 'payload_text', 'N/A')
                if 'id' in payload_data:
                    print(f"Packet {i+1}: Payload Length = {payload_length}, Payload = {payload_data}")
                    queue.put(payload_data)
                    # yield payload_data
                    #print(f"Packet {i+1}: Payload Length = {payload_length}, Payload = {payload_data}")
    except KeyboardInterrupt:
        print("\nCapture stopped.")
        capture.close()

if __name__ == "__main__":
    queue = Queue()
    capture_tcp_packets(queue,interface=r"\Device\NPF_Loopback",port=8000)
