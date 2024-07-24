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

