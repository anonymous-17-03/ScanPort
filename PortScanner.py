#!/usr/bin/python3
#coding: utf-8

import re
import socket
import subprocess
import sys

import colored


def get_ttl(ip_address):
    proc = subprocess.Popen(["/usr/bin/ping -c 1 %s" % ip_address, ""], stdout=subprocess.PIPE, shell=True)
    (out,err) = proc.communicate()
    out = out.split()
    out = out[12].decode('utf-8')
    ttl_value = re.findall(r"\d{1,3}", out)[0]
    return ttl_value

def get_os(ttl):
    ttl = int(ttl)
    if ttl >= 0 and ttl <= 64:
        return "Linux"
    elif ttl >= 65 and ttl <= 128:
        return "Windows"
    else:
        return "Not Found"

def escanear_puertos(objetivo):
    print(colored.fg('green') + "\n[+] Targeted: " + colored.fg('red') + objetivo + colored.attr('reset'))
    print(colored.fg('green') + "[+] (TTL -> %s): " % (ttl) + colored.fg('red') + "%s\n" % os_name + colored.attr('reset'))

    try:
        for port in range(1, 65536):
            print(colored.fg('red') + "  [+]" + colored.fg('blue'), "Port:", port, "/ 65535 " + colored.attr('reset'), end="\r")
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            socket.setdefaulttimeout(1)
            resultado = s.connect_ex((objetivo, port))
            if resultado == 0:
                print(colored.fg('yellow') + "  [!]" + colored.fg('48'), "Puerto {} abierto!".format(port) + colored.attr('reset'))
                open_ports.append(port)
            s.close()
            if port == 65535:
                print(colored.fg('magenta') + "\n\n[+] Lista de puertos abiertos:" + colored.fg('48'), open_ports, "\n")

    except KeyboardInterrupt:
        print(colored.fg('red') + "\n\n[!] Saliendo...\n" + colored.attr('reset'))
        sys.exit(0)
    except socket.gaierror:
        print(colored.fg('red') + "\n\n[!] No se pudo resolver el nombre del objetivo.\n" + colored.attr('reset'))
        sys.exit(1)
    except socket.error:
        print(colored.fg('red') + "\n\n[!] No se pudo conectar al objetivo.\n" + colored.attr('reset'))
        sys.exit(1)

if __name__ == "__main__":

    if len(sys.argv) != 2:
        print(colored.fg('blue') + "\n  [!] Uso: " + colored.fg('green') + "python PortScanner.py " + colored.fg('red') + "<objetivo>\n" + colored.attr('reset'))
        sys.exit(1)

    ip_address = sys.argv[1]
    ttl = get_ttl(ip_address)
    os_name = get_os(ttl)
    open_ports = []

    objetivo = socket.gethostbyname(sys.argv[1])
    escanear_puertos(objetivo)

