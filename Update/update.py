#!/usr/bin/python3
#coding: utf-8

import argparse
import socket
import subprocess
import sys

from colored import attr, fg

# Definir colores
color_title = fg('cyan')
color_option = fg('green')
color_result_open = fg('green')
color_result_closed = fg('red')
reset = attr('reset')

def scan_nc(ip, ports):
    for port in ports:
        result = subprocess.run(["nc", "-zv", ip, str(port)], capture_output=True)
        if result.returncode == 0:
            print(f"{color_result_open}Port {port} is open{reset}")
        else:
            print(f"{color_result_closed}Port {port} is closed{reset}")

def scan_sockat(ip, ports):
    for port in ports:
        result = subprocess.run(["sockat", "CONNECT", f"{ip}:{port}"], capture_output=True)
        if result.returncode == 0:
            print(f"{color_result_open}Port {port} is open{reset}")
        else:
            print(f"{color_result_closed}Port {port} is closed{reset}")

def scan_nmap(ip, ports, top_ports=False):
    if top_ports:
        ports_arg = ",".join(map(str, ports))
        result = subprocess.run(["nmap", "-p", ports_arg, "--open", "-sS", "--min-rate", "5000", "-vvv", "-n", "-Pn", ip], capture_output=True)
    else:
        result = subprocess.run(["nmap", "-p-", "--open", "-sS", "--min-rate", "5000", "-vvv", "-n", "-Pn", ip], capture_output=True)
    print(result.stdout.decode())

def main():
    # Argumentos del programa
    parser = argparse.ArgumentParser(description=color_title + "Herramienta de escaneo de puertos" + reset)
    parser.add_argument("-i", "--ip", required=True, help=color_option + "IP a escanear" + reset, action="store_true")
    parser.add_argument("-o", "--output", help=color_option + "Archivo de salida" + reset, action="store_true")
    parser.add_argument("-t", "--top-ports", help=color_option + "Número de top ports a escanear" + reset, action="store_true")
    parser.add_argument("-s", "--scan", default=1, help=color_option + "1: nc, 2: sockat, 3: nmap optimizado" + reset, action="store_true")
    parser.add_argument("-p", "--ports", help=color_option + "Puerto o puertos específicos a escanear (ej. '22' o '1-65535')" + reset, default=None, action="store_true")
    
    args = parser.parse_args()
    
    # Listas de puertos por plantilla
    top_10_ports = [80, 443, 22, 21, 25, 110, 139, 445, 135, 3306]
    top_100_ports = [7, 9, 13, 21, 22, 23, 25, 37, 42, 43, 49, 53, 70, 79, 80, 81, 88, 109, 110, 113, 115, 117, 119, 135, 137, 139, 143, 161, 179, 199, 389, 427, 443, 465, 512, 513, 514, 515, 540, 554, 587, 631, 636, 873, 990, 992, 993, 995, 1080, 1194, 1433, 1434, 1494, 1521, 1720, 1723, 2049, 2375, 2376, 3306, 3389, 5000, 5432, 5631, 5900, 6000, 6379, 6667, 8000, 8008, 8080, 8443, 8888, 9090, 9999, 10000, 32768, 49152, 49153, 49154, 49155, 49156, 49157]
    top_1000_ports = top_10_ports + top_100_ports

    # Selección de puertos
    if args.ports:
        if "-" in args.ports:
            start_port, end_port = map(int, args.ports.split('-'))
            ports = range(start_port, end_port + 1)
        else:
            ports = [int(args.ports)]
    elif args.top_ports:
        if args.top_ports == 10:
            ports = top_10_ports
        elif args.top_ports == 100:
            ports = top_100_ports
        elif args.top_ports == 1000:
            ports = top_1000_ports
        elif args.top_ports == 65535:
            ports = range(1, 65536)
    else:
        ports = range(1, 65536)

    # Ejecución del escaneo
    if args.scan == 1:
        print(f"{color_title}Escaneando con Netcat en {args.ip}{reset}")
        scan_nc(args.ip, ports)
    elif args.scan == 2:
        print(f"{color_title}Escaneando con Sockat en {args.ip}{reset}")
        scan_sockat(args.ip, ports)
    elif args.scan == 3:
        print(f"{color_title}Escaneando con Nmap en {args.ip}{reset}")
        scan_nmap(args.ip, ports, top_ports=(args.top_ports is not None))

    # Guardar en archivo
    if args.output:
        with open(args.output, "w") as f:
            sys.stdout = f
            if args.scan == 1:
                scan_nc(args.ip, ports)
            elif args.scan == 2:
                scan_sockat(args.ip, ports)
            elif args.scan == 3:
                scan_nmap(args.ip, ports, top_ports=(args.top_ports is not None))

if __name__ == "__main__":
    main()

