import signal, sys, threading, socket
from queue import Queue

def handler(sig, frame):
    print("\n[!] Saliendo...\n")
    sys.exit(1)
# Ctrl + C
signal.signal(signal.SIGINT, handler)

target = "172.17.0.2"
queue = Queue()
open_ports = []

def portscan(port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((target, port))
        return True
    except:
        return False

def fill_queue(port_list):
    for port in port_list:
        queue.put(port)

def worker():
    while not queue.empty():
        port = queue.get()
        if portscan(port):
            print(f"[!] Port {port} is open!")
            open_ports.append(port)

port_list = range(1, 65535)
fill_queue(port_list)

thread_list = []

for t in range(100):
    thread = threading.Thread(target=worker)
    thread_list.append(thread)

for thread in thread_list:
    thread.start()

for thread in thread_list:
    thread.join()

print("[+] Open ports are:", open_ports)
