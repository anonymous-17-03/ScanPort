#!/usr/bin/python3
#coding: utf-8

import argparse
import subprocess

from rich.console import Console
from rich.progress import BarColumn, Progress, TextColumn, TimeRemainingColumn
from rich.table import Table

# Colores de Rich
console = Console()
red = "[red]"
yellow = "[yellow]"
gray = "[gray]"
green = "[green]"
blue = "[blue]"
turquoise = "[cyan]"

def ctrl_c_handler(sig, frame):
    console.print(f"\n\n{red}[!] Saliendo...{yellow}\n")
    exit(1)

def scan_port(ip):
    start_port = 1
    end_port = 65535
    open_ports = []

    console.print(f"\n{yellow}[!] {gray}Iniciando escaneo de puertos en la IP {red}{ip}{gray}\n")

    with Progress(
        TextColumn("{task.description}"),
        BarColumn(),
        "[progress.percentage]{task.percentage:>3.1f}%",
        TimeRemainingColumn(),
    ) as progress:
        task = progress.add_task(f"{red}[*] {blue}Escaneando -> {ip}", total=end_port - start_port + 1)

        for port in range(start_port, end_port + 1):
            result = subprocess.run(
                ["nc", "-nvv", "-w", "1", "-z", ip, str(port)],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
            if b"open" in result.stderr:
                open_ports.append(port)
            progress.update(task, advance=1)
    
    console.print(f"\n{green}[+] Puertos abiertos:\n", style="bold green")
    if open_ports:
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("Puerto", justify="right")
        for port in open_ports:
            table.add_row(str(port))
        console.print(table)
    else:
        console.print(f"{yellow}[!] No se encontraron puertos abiertos.", style="bold yellow")

    console.print(f"\n{green}[*] Escaneo completado.\n")

def main():
    parser = argparse.ArgumentParser(description="Escáner de puertos con barra de progreso usando Rich")
    parser.add_argument("-i", "--ip", type=str, required=True, help="IP a escanear")
    args = parser.parse_args()
    
    scan_port(args.ip)

if __name__ == "__main__":
    import signal
    signal.signal(signal.SIGINT, ctrl_c_handler)
    main()

