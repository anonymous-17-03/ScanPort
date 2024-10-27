# PortScanner

Este es un script de Python para escanear puertos abiertos en una dirección IP objetivo y obtener información sobre los servicios y versiones que se están ejecutando en esos puertos. Además, el script detecta el sistema operativo de la máquina objetivo basándose en el valor TTL (Time to Live). También verifica vulnerabilidades comunes en los servicios de FTP, SSH y HTTP.


## Características

- Escaneo de puertos del 1 al 65535.
- Detección del sistema operativo objetivo (Linux o Windows) basado en TTL.
- Información de servicios y versiones utilizando `nmap`.
- Comprobación de vulnerabilidades en servicios de FTP y SSH.
- Detección de tecnologías HTTP utilizando `whatweb`.
- Salida de información formateada y coloreada en la terminal.
- Guardado de la evidencia en un archivo `Targeted.txt`.

## Requisitos

Asegúrate de tener instaladas las siguientes herramientas en tu sistema:

- Python 3.x
- Módulos de Python: `re`, `socket`, `subprocess`, `sys`, `colored`
- Herramientas externas: `nmap`, `whatweb`

## Instalación

1. Clona este repositorio en tu máquina local y asigna permisos de ejecución al script:

    ```bash
    git clone https://github.com/anonymous-17-03/ScanPort.git
    cd ScanPort
    chmod +x PortScanner.py
    ```

2. Instala las dependencias requeridas:

    - Instalación en un Entorno Virtual: Es recomendable utilizar un entorno virtual para evitar conflictos de dependencias con otros proyectos y mantener un ambiente de desarrollo limpio.

    - Crea un entorno virtual en el directorio del proyecto:

    ```sh
    python3 -m venv env
    ```

    - Activa el entorno virtual:

    ```sh
    source env/bin/activate
    pip install colored
    ```

    - Para desactivar el entorno virtual una vez hayas terminado:

    ```sh
    deactivate
    ```

3. Asegúrate de tener instalados `nmap` y `whatweb` en tu sistema. Puedes instalarlos usando el gestor de paquetes de tu sistema operativo. Por ejemplo, en Debian/Ubuntu puedes usar:

    ```bash
    sudo apt-get install nmap whatweb
    ```

## Uso

Ejecuta el script con el siguiente comando, reemplazando `<objetivo>` con la dirección IP que deseas escanear:

```bash
python3 PortScanner.py <objetivo>
```

## Ejemplo de Salida

A continuación, se muestra un ejemplo de cómo se ve la salida del script al ejecutarlo:

![Resultado con nmap](img.png)

## Notas

- Este script solo funciona en sistemas Unix-like debido al uso del comando ping con la opción -c.
- Asegúrate de tener permisos de red adecuados para ejecutar pings y escanear puertos en el objetivo especificado.
- Usa este script de manera ética y solo en sistemas sobre los que tengas permiso de realizar escaneos de red.
