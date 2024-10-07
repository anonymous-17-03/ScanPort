#!/usr/bin/python3
#coding: utf-8

import argparse
import re
import socket
import subprocess
import sys

import colored
from colored import attr, fg

# Definir colores
color_cyan = fg('cyan')
color_green = fg('green')
color_verdec = fg('48')
color_yellow = fg('yellow')
color_red = fg('red')
color_blue = fg('blue')
color_magenta = fg('magenta')
reset = attr('reset')

top_10_ports = [21, 22, 25, 80, 110, 135, 139, 443, 445, 3306]
top_100_ports = [
    7, 9, 13, 21, 22, 23, 25, 37, 42, 43, 49, 53, 70, 79, 80, 81, 88, 109, 110, 113,
    115, 117, 119, 135, 137, 139, 143, 161, 179, 199, 389, 427, 443, 465, 512, 513, 514,
    515, 540, 554, 587, 631, 636, 873, 990, 992, 993, 995, 1080, 1194, 1433, 1434, 1494,
    1521, 1720, 1723, 2049, 2375, 2376, 3306, 3389, 5000, 5432, 5631, 5900, 6000, 6379,
    6667, 8000, 8008, 8080, 8443, 8888, 9090, 9999, 10000, 32768, 49152, 49153, 49154,
    49155, 49156, 49157, 51493, 52673, 52822, 52848, 52869, 54045, 54328, 55055, 55555,
    55600, 56738, 57797, 58080, 60020, 61532, 61900, 63331

]
top_1000_ports = [
    1, 3, 4, 6, 7, 9, 13, 17, 19, 20, 21, 22, 23, 24, 25, 26, 30, 32, 33, 37, 42, 43,
    49, 53, 70, 79, 80, 81, 82, 83, 84, 85, 88, 89, 90, 99, 100, 106, 109, 110, 111,
    113, 119, 125, 135, 139, 143, 144, 146, 161, 163, 179, 199, 211, 212, 222, 254, 255,
    256, 259, 264, 280, 301, 306, 311, 340, 366, 389, 406, 407, 416, 425, 427, 443, 444,
    445, 458, 464, 465, 481, 497, 500, 512, 513, 514, 515, 524, 541, 543, 544, 545, 548,
    554, 556, 563, 587, 593, 616, 617, 625, 631, 636, 646, 648, 666, 667, 683, 687, 691,
    700, 705, 711, 714, 720, 722, 726, 749, 765, 777, 783, 787, 800, 801, 808, 843, 873,
    880, 888, 898, 900, 901, 902, 903, 911, 912, 981, 987, 990, 992, 993, 995, 999, 1000,
    1001, 1002, 1007, 1009, 1010, 1021, 1022, 1023, 1024, 1025, 1026, 1027, 1028, 1029,
    1030, 1031, 1032, 1033, 1034, 1035, 1036, 1037, 1038, 1039, 1040, 1041, 1042, 1043,
    1044, 1045, 1046, 1047, 1048, 1049, 1050, 1051, 1052, 1053, 1054, 1056, 1058, 1059,
    1064, 1065, 1066, 1069, 1070, 1071, 1074, 1080, 1081, 1083, 1085, 1086, 1087, 1088,
    1090, 1091, 1093, 1094, 1095, 1096, 1098, 1099, 1100, 1102, 1104, 1105, 1106, 1107,
    1108, 1110, 1111, 1112, 1113, 1114, 1117, 1119, 1121, 1122, 1123, 1126, 1130, 1131,
    1137, 1138, 1141, 1145, 1147, 1148, 1149, 1151, 1152, 1154, 1163, 1164, 1165, 1169,
    1174, 1175, 1183, 1185, 1186, 1187, 1192, 1198, 1199, 1201, 1213, 1216, 1217, 1218,
    1233, 1234, 1236, 1244, 1247, 1259, 1271, 1272, 1277, 1287, 1296, 1300, 1301, 1309,
    1310, 1311, 1322, 1328, 1334, 1352, 1417, 1433, 1434, 1443, 1455, 1461, 1494, 1500,
    1501, 1503, 1521, 1524, 1533, 1556, 1580, 1583, 1594, 1600, 1641, 1658, 1666, 1687,
    1688, 1700, 1717, 1718, 1719, 1720, 1721, 1723, 1755, 1761, 1782, 1783, 1801, 1805,
    1812, 1839, 1840, 1862, 1863, 1864, 1875, 1900, 1914, 1935, 1947, 1971, 1972, 1974,
    1984, 1998, 1999, 2000, 2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010,
    2013, 2020, 2021, 2022, 2030, 2033, 2034, 2035, 2038, 2040, 2041, 2042, 2043, 2045,
    2046, 2047, 2048, 2049, 2065, 2068, 2099, 2100, 2103, 2105, 2106, 2107, 2111, 2119,
    2121, 2126, 2135, 2144, 2160, 2161, 2170, 2179, 2190, 2191, 2196, 2200, 2222, 2251,
    2260, 2288, 2301, 2323, 2366, 2381, 2382, 2393, 2394, 2399, 2401, 2492, 2500, 2522,
    2525, 2557, 2601, 2602, 2604, 2605, 2607, 2608, 2638, 2701, 2702, 2710, 2717, 2718,
    2725, 2800, 2809, 2811, 2869, 2875, 2909, 2920, 2967, 2998, 3000, 3001, 3003, 3005,
    3006, 3007, 3011, 3013, 3017, 3030, 3031, 3050, 3071, 3077, 3128, 3168, 3211, 3221,
    3260, 3268, 3283, 3300, 3306, 3322, 3323, 3324, 3325, 3333, 3351, 3367, 3369, 3370,
    3371, 3372, 3389, 3390, 3404, 3476, 3493, 3517, 3527, 3546, 3551, 3580, 3659, 3689,
    3690, 3703, 3737, 3766, 3784, 3800, 3801, 3809, 3814, 3826, 3827, 3828, 3851, 3869,
    3871, 3878, 3880, 3889, 3905, 3914, 3918, 3920, 3945, 3971, 3986, 3995, 3998, 4000,
    4001, 4002, 4003, 4004, 4005, 4045, 4111, 4125, 4126, 4129, 4224, 4242, 4279, 4321,
    4343, 4443, 4444, 4445, 4449, 4550, 4567, 4662, 4848, 4899, 4900, 4998, 5000, 5001,
    5002, 5003, 5004, 5009, 5030, 5033, 5050, 5051, 5054, 5060, 5061, 5080, 5087, 5100,
    5101, 5120, 5190, 5200, 5214, 5221, 5222, 5225, 5226, 5269, 5280, 5298, 5357, 5405,
    5414, 5432, 5440, 5500, 5510, 5544, 5550, 5555, 5560, 5566, 5631, 5633, 5666, 5678,
    5679, 5718, 5730, 5800, 5801, 5810, 5811, 5822, 5862, 5900, 5901, 5902, 5903, 5906,
    5907, 5910, 5911, 5915, 5922, 5925, 5950, 5952, 5959, 5960, 5961, 5962, 5987, 5988,
    5989, 5998, 6000, 6001, 6002, 6003, 6004, 6005, 6006, 6007, 6009, 6025, 6059, 6100,
    6101, 6106, 6112, 6123, 6129, 6156, 6346, 6347, 6379, 6400, 6401, 6432, 6443, 6444,
    6445, 6446, 6461, 6463, 6467, 6502, 6510, 6511, 6543, 6547, 6565, 6566, 6567, 6580,
    6646, 6666, 6667, 6668, 6669, 6689, 6692, 6699, 6779, 6788, 6789, 6792, 6839, 6881,
    6901, 6969, 6970, 7000, 7001, 7002, 7004, 7007, 7019, 7025, 7070, 7100, 7103, 7106,
    7200, 7201, 7402, 7435, 7443, 7496, 7512, 7625, 7627, 7676, 7741, 7777, 7778, 7800,
    7911, 7920, 7921, 7937, 7938, 7999, 8000, 8001, 8002, 8007, 8008, 8009, 8010, 8011,
    8021, 8022, 8031, 8042, 8045, 8080, 8081, 8082, 8083, 8088, 8090, 8093, 8099, 8100,
    8180, 8181, 8192, 8193, 8194, 8200, 8222, 8254, 8290, 8291, 8300, 8333, 8383, 8400,
    8402, 8443, 8500, 8600, 8649, 8651, 8652, 8654, 8701, 8800, 8873, 8880, 8888, 8899,
    8994, 9000, 9001, 9002, 9003, 9009, 9010, 9040, 9050, 9071, 9080, 9081, 9090, 9091,
    9099, 9100, 9101, 9102, 9103, 9110, 9111, 9200, 9207, 9220, 9290, 9415, 9418, 9443,
    9500, 9502, 9503, 9527, 9535, 9575, 9593, 9594, 9595, 9618, 9666, 9876, 9877, 9878,
    9879, 9880, 9881, 9882, 9884, 9886, 9887, 9888, 9889, 9890, 9891, 9893, 9895, 9897,
    9898, 9900, 9917, 9929, 9943, 9944, 9968, 9998, 9999, 10000, 10001, 10002, 10003,
    10004, 10009, 10010, 10012, 10024, 10025, 10082, 10180, 10215, 10243, 10566, 10616,
    10617, 10621, 10626, 10628, 10629, 10630, 10631, 10778, 11110, 11111, 11967, 12000,
    12174, 12265, 12345, 13456, 13722, 13782, 13783, 14000, 14238, 14441, 14442, 15000,
    15002, 15003, 15004, 15660, 15742, 16000, 16001, 16012, 16016, 16018, 16080, 16113,
    16992, 16993, 17877, 17988, 18040, 18101, 18988, 19101, 19283, 19315, 19350, 19780,
    19801, 19842, 20000, 20005, 20031, 20221, 20222, 20828, 20997, 21421, 21571, 22939,
    23502, 24444, 24800, 25734, 25735, 26214, 27000, 27352, 27353, 27355, 27356, 27715,
    27725, 27730, 27777, 27781, 27788, 28100, 28201, 30000, 30718, 30951, 31038, 31337,
    32768, 32769, 32770, 32771, 32772, 32773, 32774, 32775, 32776, 32777, 32778, 32779,
    32780, 32781, 32782, 32783, 32784, 33354, 33899, 34571, 34572, 34573, 35500, 38292,
    40193, 40911, 41524, 42510, 44276, 44442, 44443, 44501, 45100, 48080, 49152, 49153,
    49154, 49155, 49156, 49157, 49158, 49159, 49160, 49161, 49163, 49165, 49167, 49175,
    49176, 49400, 49999, 50000, 50001, 50002, 50003, 50006, 50300, 50389, 50500, 50636,
    50800, 51103, 51493, 52673, 52822, 52848, 52869, 54045, 54328, 55055, 55056, 55555,
    55600, 56737, 56738, 57294, 57797, 58080, 60020, 60443, 61532, 61900, 62078, 63331,
    65129, 65389, 65390, 65397, 65399, 65400, 65421, 65422, 65467, 65488, 65491, 65501,
    65510, 65511, 65517, 65519, 65520, 65522, 65529, 65535
]

class CustomHelpFormatter(argparse.HelpFormatter):
    def _format_action_invocation(self, action):
        if action.option_strings:
            options = ', '.join(action.option_strings)
            return options
        else:
            return super()._format_action_invocation(action)

def log_output(file, message, to_print=True):
    if to_print:
        print(message)
    file.write(message + "\n")
    # Uso:
    # with open(output, "w") as file:
    #    log_output(file, colored.fg('green') + "\n[+] Autor: " + colored.fg('blue') + "Anonymous17" + colored.attr('reset'))

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

def escanear_puertos(objetivo, ports, file, add):
    print(colored.fg('green') + "\n[+] Autor: " + colored.fg('blue') + "Anonymous17" + colored.attr('reset'))
    print(colored.fg('green') + "[+] Targeted: " + colored.fg('red') + objetivo + colored.attr('reset'))
    print(colored.fg('green') + "[+] (TTL -> %s): " % (ttl) + colored.fg('yellow') + "%s" % os_name + colored.attr('reset'))
    print(colored.fg('magenta') + "[!] Escaneo de puertos (socket):\n" + colored.attr('reset'))
    file.write(colored.fg('green') + "\n[+] Autor: " + colored.fg('blue') + "Anonymous17" + colored.attr('reset') + "\n")
    file.write(colored.fg('green') + "[+] Targeted: " + colored.fg('red') + objetivo + colored.attr('reset') + "\n")
    file.write(colored.fg('green') + "[+] (TTL -> %s): " % (ttl) + colored.fg('yellow') + "%s" % os_name + colored.attr('reset') + "\n")
    file.write(colored.fg('magenta') + "[!] Escaneo de puertos (socket):\n" + colored.attr('reset') + "\n")
    current_ports = 0
    total_ports = len(ports)

    try:
        for port in ports:
            current_ports += 1
            print(colored.fg('red') + "  [+]" + colored.fg('blue') + f" Port: {current_ports} / {total_ports} " + colored.attr('reset'), end="\r")
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
        if add:
            if 'V' in add:
                if open_ports:
                    print(colored.fg('cyan') + "[+] Información de servicios y versiones:\n" + colored.attr('reset'))
                    file.write(colored.fg('cyan') + "[+] Información de servicios y versiones:\n\n" + colored.attr('reset'))
                for port in open_ports:
                    get_service_info(objetivo, port, file)
            if 'C' in add:
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

def main():
    parser = argparse.ArgumentParser(
        description=color_red + "Script de escaneo de puertos y detección de vulnerabilidades" + reset,
        formatter_class=CustomHelpFormatter)
    parser.add_argument('-i', '--ip', required=True, help=color_blue + "Dirección IP del objetivo (ej: --ip 192.168.0.1)" + reset)
    parser.add_argument('-t', '--top-ports', type=int, choices=[10, 100, 1000, 65535], default=65535, help=color_blue + "Número de puertos a escanear: 10, 100, 1000, 65535" +reset)
    parser.add_argument('-s', '--scan', type=int, choices=[1, 2, 3], default=2, help=color_blue + "Escanear con: 1 = netcat, 2 = socket, 3 = nmap" + reset)
    parser.add_argument('-a', '--add', choices=['V','C'], nargs='+', help=color_blue + "Pruebas adicionales (ej: -a V C): V = version, C = check vuln" + reset)
    parser.add_argument('-o', '--output', default="output.txt", help=color_blue + "Archivo de salida (ej: -o output.txt)" + reset)
    args = parser.parse_args()

    global ttl, os_name

    objetivo = args.ip
    ttl = get_ttl(objetivo)
    os_name = get_os(ttl)
    ports = []

    if args.top_ports:
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

    if args.scan == 1:
        scan_nc(args.output, args.ip, ports, args.add)
    elif args.scan == 2:
        scan_socket(args.output ,args.ip, ports, args.add)
    elif args.scan == 3:
        scan_nmap(args.output, args.ip, ports, args.add)

def scan_nc(output, ip, ports, add):
    current_ports = 0
    total_ports = len(ports)
    open_ports = []
    try:
        with open(output, "w") as file:
            print(colored.fg('green') + "\n[+] Autor: " + colored.fg('blue') + "Anonymous17" + colored.attr('reset'))
            print(colored.fg('green') + "[+] Targeted: " + colored.fg('red') + ip + colored.attr('reset'))
            print(colored.fg('green') + "[+] (TTL -> %s): " % (ttl) + colored.fg('yellow') + "%s" % os_name + colored.attr('reset'))
            print(colored.fg('magenta') + "[!] Escaneo de puertos (netcat):\n" + colored.attr('reset'))
            file.write(colored.fg('green') + "\n[+] Autor: " + colored.fg('blue') + "Anonymous17" + colored.attr('reset') + "\n")
            file.write(colored.fg('green') + "[+] Targeted: " + colored.fg('red') + ip + colored.attr('reset') + "\n")
            file.write(colored.fg('green') + "[+] (TTL -> %s): " % (ttl) + colored.fg('yellow') + "%s" % os_name + colored.attr('reset') + "\n")
            file.write(colored.fg('magenta') + "[!] Escaneo de puertos (netcat):\n" + colored.attr('reset') + "\n")
            for port in ports:
                current_ports += 1
                print(colored.fg('red') + "  [+]" + colored.fg('blue') + f" Port: {current_ports} / {total_ports} " + colored.attr('reset'), end="\r")
                try:
                    result = subprocess.run(["nc", "-zvw1", ip, str(port)], capture_output=True)
                    if result.returncode == 0:
                        print(f"{color_verdec}  [!] Puerto {port} abierto! {reset}")
                        file.write(f"{color_verdec}  [!] Puerto {port} abierto! {reset}\n")
                        open_ports.append(port)
                except subprocess.CalledProcessError as e:
                    print(colored.fg('red') + f"\n[!] Error al ejecutar el comando `nc` en el puerto {port}: {e}" + colored.attr('reset'))
                    file.write(colored.fg('red') + f"\n[!] Error al ejecutar el comando `nc` en el puerto {port}: {e}" + colored.attr('reset') + "\n")
                except Exception as e:
                    print(colored.fg('red') + f"\n[!] Error inesperado al escanear el puerto {port}: {e}" + colored.attr('reset'))
                    file.write(colored.fg('red') + f"\n[!] Error inesperado al escanear el puerto {port}: {e}" + colored.attr('reset') + "\n")
            if open_ports:
                print(colored.fg('magenta') + "\n\n[+] Lista de puertos abiertos:" + colored.fg('48'), open_ports)
                file.write(colored.fg('magenta') + "\n[+] Lista de puertos abiertos:" + colored.fg('48') + " {}\n".format(open_ports))
            if add:
                if 'V' in add:
                    if open_ports:
                        print(colored.fg('cyan') + "[+] Información de servicios y versiones:\n" + colored.attr('reset'))
                        file.write(colored.fg('cyan') + "[+] Información de servicios y versiones:\n\n" + colored.attr('reset'))
                    for port in open_ports:
                        get_service_info(ip, port, file)
                if 'C' in add:
                    print(colored.fg('cyan') + "\n[+] Comprobando vulnerabilidades:\n" + colored.attr('reset'))
                    file.write(colored.fg('cyan') + "\n[+] Comprobando vulnerabilidades:\n\n" + colored.attr('reset'))
                    for port in open_ports:
                        if port == 21:
                            check_ftp_vulnerability(ip, port, file)
                        elif port == 22:
                            check_ssh_vulnerability(ip, port, file)
                        elif port in [80, 8080, 8000, 443, 8443]:
                            check_http_technologies(ip, port, file)
        print(colored.fg('green') + f"\n[*] Evidencia guardada en" + colored.fg('red') + f" {output}" + colored.attr('reset') + "\n")
    except KeyboardInterrupt:
        print(colored.fg('red') + "\n\n[!] Saliendo..." + colored.attr('reset'))
        sys.exit(0)
    except IOError as e:
        print(colored.fg('red') + f"\n[!] Error al escribir en el archivo {output}: {e}" + colored.attr('reset'))
    except Exception as e:
        print(colored.fg('red') + f"\n[!] Error inesperado: {e}" + colored.attr('reset'))

def scan_socket(output, ip, ports, add):
    with open(output, "w") as file:
        escanear_puertos(ip, ports, file, add)
    print(colored.fg('green') + f"\n[*] Evidencia guardada en" + colored.fg('red') + f" {output}" + colored.attr('reset') + "\n")

def scan_nmap(output, ip, ports, add):
    print("[!] Pronto disponible...")

if __name__ == "__main__":
    open_ports = []
    main()
