# ScanPort

Este repositorio contiene dos scripts de Python para escanear puertos en una máquina objetivo. Cada script utiliza diferentes métodos para realizar el escaneo de puertos y tiene su propia implementación. 

## Contenido

- [Descripción](#descripción)
- [Requisitos](#requisitos)
- [Uso](#uso)
- [Script 1: Escaneo de puertos sencillo](#script-1-escanear-puertos-sencillo)
- [Script 2: Escaneo de puertos con threading](#script-2-escanear-puertos-con-threading)

## Descripción

1. **Script 1**: Realiza un escaneo de puertos secuencial en un rango de puertos (1-65535) para una máquina objetivo especificada.
2. **Script 2**: Utiliza threading para realizar un escaneo de puertos más rápido y eficiente en una máquina objetivo, también en el rango de puertos (1-65535).

## Requisitos

- Python 3.x

## Uso

Para usar cualquiera de los scripts, asegúrate de tener Python 3.x instalado y sigue las instrucciones a continuación para cada script.

### Script 1: Escaneo de puertos sencillo

Este script escanea puertos de manera secuencial y muestra los puertos abiertos.

#### Uso

1. Guarda el siguiente código en un archivo llamado `PortScanner.py`:
    ```python
    import socket
    import sys

    def escanear_puertos(objetivo):
        print("[+] Escaneando la máquina host:", objetivo)

        try:
            for port in range(1, 65536):
                print("[+] Port:", port, "/ 65535 ", end="\r")
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                socket.setdefaulttimeout(1)
                resultado = s.connect_ex((objetivo, port))
                if resultado == 0:
                    print("  [!] {} Port abierto".format(port))
                s.close()

        except KeyboardInterrupt:
            print("\n[!] Escaneo interrumpido por el usuario.\n")
            sys.exit(0)
        except socket.gaierror:
            print("\n[!] No se pudo resolver el nombre del objetivo.\n")
            sys.exit(1)
        except socket.error:
            print("\n[!] No se pudo conectar al objetivo.\n")
            sys.exit(1)

    if __name__ == "__main__":
        if len(sys.argv) != 2:
            print("Uso: python PortScanner.py <objetivo>")
            sys.exit(1)

        objetivo = socket.gethostbyname(sys.argv[1])
        escanear_puertos(objetivo)
    ```

2. Ejecuta el script desde la línea de comandos:
    ```bash
    python PortScanner.py <objetivo>
    ```

### Script 2: Escaneo de puertos con threading

Este script utiliza múltiples hilos para escanear puertos de manera más rápida.

#### Uso

1. Guarda el siguiente código en un archivo llamado `portscan.py`:
    ```python
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
    ```

2. Cambia la variable `target` al objetivo deseado.

3. Ejecuta el script desde la línea de comandos:
    ```bash
    python portscan.py
    ```

## Enlace del Repositorio

Para más detalles y actualizaciones, visita el [repositorio en GitHub](https://github.com/anonymous-17-03/ScanPort).

