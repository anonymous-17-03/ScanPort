#!/usr/bin/python3
#coding: utf-8

import re
import socket
import subprocess
import sys

import colored


def get_ttl(ip_address):
    try:
        proc = subprocess.Popen(["/usr/bin/ping", "-c", "1", ip_address], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = proc.communicate()
        if proc.returncode != 0:
            print(colored.fg('red') + "\n[!] Error ejecutando el comando ping.\n" + colored.attr('reset'))
            sys.exit(1)
        out = out.split()
        out = out[12].decode('utf-8')
        ttl_value = re.findall(r"\d{1,3}", out)[0]
        return ttl_value
    except Exception as e:
        print(colored.fg('red') + f"\n[!] Error: {str(e)}\n" + colored.attr('reset'))
        sys.exit(1)

def get_os(ttl):
    ttl = int(ttl)
    if ttl >= 0 and ttl <= 64:
        return "Linux"
    elif ttl >= 65 and ttl <= 128:
        return "Windows"
    else:
        return "Not Found"

def check_ftp_vulnerability(ip, port, file):
    try:
        proc = subprocess.Popen(["nmap", "-p", str(port), "--script", "ftp-anon", ip], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = proc.communicate()
        if b'Anonymous FTP login allowed' in out:
            print(colored.fg('red') + "  [!] FTP Vulnerable: Login como anonymous exitoso" + colored.attr('reset'))
            file.write(colored.fg('red') + "  [!] FTP Vulnerable: Login como anonymous exitoso" + colored.attr('reset') + "\n")
        else:
            print(colored.fg('green') + "  [+] FTP parece seguro contra login anonymous" + colored.attr('reset'))
            file.write(colored.fg('green') + "  [+] FTP parece seguro contra login anonymous" + colored.attr('reset') + "\n")
    except Exception as e:
        print(colored.fg('red') + f"\n  [!] Error comprobando vulnerabilidad FTP: {str(e)}\n" + colored.attr('reset'))

def check_ssh_vulnerability(ip, port, file):
    try:
        proc = subprocess.Popen(["nmap", "-sCV", "-p", str(port), ip], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = proc.communicate()
        if b'OpenSSH' in out:
            version_line = next(line for line in out.split(b'\n') if b'OpenSSH' in line)
            version_match = re.search(rb'OpenSSH\s(\d+\.\d+)', version_line)
            if version_match:
                version = version_match.group(1).decode('utf-8')
                version_number = float(version)
                if version_number <= 7.7:
                    print(colored.fg('red') + "  [!] SSH Vulnerable: Enumeración de usuarios " + colored.attr('reset'))
                    file.write(colored.fg('red') + "  [!] SSH Vulnerable: Enumeración de usuarios " + colored.attr('reset') + "\n")
                else:
                    print(colored.fg('green') + "  [+] SSH parece seguro contra enumeración de usuarios  " + colored.attr('reset'))
                    file.write(colored.fg('green') + "  [+] SSH parece seguro contra enumeración de usuarios  " + colored.attr('reset') + "\n")
            else:
                print(colored.fg('yellow') + "  [!] No se pudo determinar la versión de SSH" + colored.attr('reset'))
                file.write(colored.fg('yellow') + "  [!] No se pudo determinar la versión de SSH" + colored.attr('reset') + "\n")
        else:
            print(colored.fg('yellow') + "  [!] No se pudo determinar la versión de SSH" + colored.attr('reset'))
            file.write(colored.fg('yellow') + "  [!] No se pudo determinar la versión de SSH" + colored.attr('reset') + "\n")
    except Exception as e:
        print(colored.fg('red') + f"  [!] Error comprobando vulnerabilidad SSH: {str(e)}" + colored.attr('reset'))
        file.write(colored.fg('red') + f"  [!] Error comprobando vulnerabilidad SSH: {str(e)}" + colored.attr('reset') + "\n")

def check_http_technologies(ip, port, file):
    try:
        proc = subprocess.Popen(["whatweb", f"http://{ip}:{port}"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = proc.communicate(timeout=10)
        if proc.returncode == 0:
            output = out.decode('utf-8').strip()
            if output:
                items = [item.strip() for item in output.split(',')]
                formatted_output = "\n".join(f"        {item}," for item in items)
                print(colored.fg('48') + "  [+] Tecnologías detectadas en HTTP:\n" + colored.attr('reset'))
                file.write(colored.fg('48') + "  [+] Tecnologías detectadas en HTTP:\n" + colored.attr('reset') + "\n")
                print(formatted_output)
                file.write(formatted_output + "\n\n")
            else:
                print(colored.fg('red') + "  [!] Error: No se detectaron tecnologías HTTP." + colored.attr('reset'))
                file.write(colored.fg('red') + "  [!] Error: No se detectaron tecnologías HTTP." + colored.attr('reset') + "\n")
        else:
            print(colored.fg('red') + "  [!] Error: No se pudieron detectar tecnologías HTTP." + colored.attr('reset'))
            file.write(colored.fg('red') + "  [!] Error: No se pudieron detectar tecnologías HTTP." + colored.attr('reset') + "\n")
    except subprocess.TimeoutExpired:
        print(colored.fg('red') + "  [!] Error: Tiempo de espera excedido para detectar tecnologías HTTP." + colored.attr('reset'))
        file.write(colored.fg('red') + "  [!] Error: Tiempo de espera excedido para detectar tecnologías HTTP." + colored.attr('reset') + "\n")
    except Exception as e:
        print(colored.fg('red') + f"  [!] Error detectando tecnologías HTTP: {str(e)}" + colored.attr('reset'))
        file.write(colored.fg('red') + f"  [!] Error detectando tecnologías HTTP: {str(e)}" + colored.attr('reset') + "\n")

def escanear_puertos(objetivo, file):

    print(colored.fg('green') + "\n[+] Autor: " + colored.fg('blue') + "Anonymous17" + colored.attr('reset'))
    print(colored.fg('green') + "[+] Targeted: " + colored.fg('red') + objetivo + colored.attr('reset'))
    print(colored.fg('green') + "[+] (TTL -> %s): " % (ttl) + colored.fg('yellow') + "%s" % os_name + colored.attr('reset'))
    print(colored.fg('magenta') + "[!] Escaneo de puertos:\n" + colored.attr('reset'))
    file.write(colored.fg('green') + "\n[+] Autor: " + colored.fg('blue') + "Anonymous17" + colored.attr('reset') + "\n")
    file.write(colored.fg('green') + "[+] Targeted: " + colored.fg('red') + objetivo + colored.attr('reset') + "\n")
    file.write(colored.fg('green') + "[+] (TTL -> %s): " % (ttl) + colored.fg('yellow') + "%s" % os_name + colored.attr('reset') + "\n")
    file.write(colored.fg('magenta') + "[!] Escaneo de puertos:\n" + colored.attr('reset') + "\n")

    try:
        for port in range(1, 65536):
            print(colored.fg('red') + "  [+]" + colored.fg('blue'), "Port:", port, "/ 65535 " + colored.attr('reset'), end="\r")
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            socket.setdefaulttimeout(1)
            resultado = s.connect_ex((objetivo, port))
            if resultado == 0:
                print(colored.fg('yellow') + "  [!]" + colored.fg('48'), "Puerto {} abierto!".format(port) + colored.attr('reset'))
                file.write(colored.fg('yellow') + "  [!]" + colored.fg('48') + "Puerto {} abierto!\n".format(port) + colored.attr('reset'))
                open_ports.append(port)
            s.close()
        if open_ports:
            print(colored.fg('magenta') + "\n\n[+] Lista de puertos abiertos:" + colored.fg('48'), open_ports)
            file.write(colored.fg('magenta') + "\n[+] Lista de puertos abiertos:" + colored.fg('48') + " {}\n".format(open_ports))
        if open_ports:
            print(colored.fg('cyan') + "[+] Información de servicios y versiones:\n" + colored.attr('reset'))
            file.write(colored.fg('cyan') + "[+] Información de servicios y versiones:\n\n" + colored.attr('reset'))
            for port in open_ports:
                get_service_info(objetivo, port, file)
        print(colored.fg('cyan') + "\n[+] Comprobando vulnerabilidades:\n" + colored.attr('reset'))
        file.write(colored.fg('cyan') + "\n[+] Comprobando vulnerabilidades:\n\n" + colored.attr('reset'))
        for port in open_ports:
            if port == 21:
                check_ftp_vulnerability(objetivo, port, file)
            elif port == 22:
                check_ssh_vulnerability(objetivo, port, file)
            elif port in [80, 8080, 8000, 443, 8443]:
                check_http_technologies(objetivo, port, file)
    except KeyboardInterrupt:
        print(colored.fg('red') + "\n\n[!] Saliendo...\n" + colored.attr('reset'))
        sys.exit(0)
    except socket.gaierror:
        print(colored.fg('red') + "\n\n[!] No se pudo resolver el nombre del objetivo.\n" + colored.attr('reset'))
        sys.exit(1)
    except socket.error:
        print(colored.fg('red') + "\n\n[!] No se pudo conectar al objetivo.\n" + colored.attr('reset'))
        sys.exit(1)

def get_service_info(ip, port, file):
    try:
        proc = subprocess.Popen(["nmap", "-p", str(port), "-sV", ip], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = proc.communicate()
        if proc.returncode != 0:
            print(colored.fg('red') + "\n[!] Error ejecutando el comando nmap.\n" + colored.attr('reset'))
            sys.exit(1)
        output_lines = out.decode('utf-8').split('\n')
        for line in output_lines:
            if '/tcp' in line:
                line = line.replace('open', '').strip()
                if line:
                    parts = line.split()
                    if len(parts) > 2:
                        port_info = parts[0]
                        service_info = parts[1]
                        version_info = ' '.join(parts[2:])
                        formatted_line = f"{port_info:<8} {service_info:<8} {version_info}"
                        print(colored.fg('blue') + "  [+] " + colored.fg('yellow') + formatted_line[:8] + " " + colored.fg('red') + formatted_line[8:16] + " " + colored.fg(48) + formatted_line[16:] + colored.attr('reset'))
                        file.write(colored.fg('blue') + "  [+] " + colored.fg('yellow') + formatted_line[:8] + " " + colored.fg('red') + formatted_line[8:16] + " " + colored.fg(48) + formatted_line[16:] + colored.attr('reset') + "\n")
    except Exception as e:
        print(colored.fg('red') + f"\n[!] Error: {str(e)}\n" + colored.attr('reset'))

if __name__ == "__main__":

    if len(sys.argv) != 2:
        print(colored.fg('blue') + "\n  [!] Uso: " + colored.fg('green') + "python PortScanner.py " + colored.fg('red') + "<objetivo>\n" + colored.attr('reset'))
        sys.exit(1)

    ip_address = sys.argv[1]
    ttl = get_ttl(ip_address)
    os_name = get_os(ttl)
    open_ports = []
    objetivo = socket.gethostbyname(sys.argv[1])
    output_file = 'Targeted.txt'
    with open(output_file, 'w') as file:
        escanear_puertos(objetivo, file)
    print(colored.fg('green') + f"\n[*] Evidencia guardada en" + colored.fg('red') + f" {output_file}" + colored.attr('reset') + "\n")

