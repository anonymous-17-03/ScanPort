# PortScanner

Este es un script en Python para escanear puertos abiertos en un objetivo específico y determinar el sistema operativo basado en el valor TTL (Time To Live)

## Descripción

El script realiza las siguientes funciones:

1. **Obtener el TTL (Time To Live)**: Utiliza el comando `ping` para obtener el valor TTL de la IP objetivo.
2. **Determinar el Sistema Operativo**: Basado en el valor TTL, intenta identificar el sistema operativo del objetivo.
3. **Escaneo de Puertos**: Escanea los puertos del 1 al 65535 para identificar cuáles están abiertos.

## Dependencias

El script requiere los siguientes módulos de Python:

- `re`
- `socket`
- `subprocess`
- `sys`
- `colored`

Puedes instalar el módulo `colored` usando pip:

```sh
pip install colored
```

## Ejemplo de uso:

![Resultado con nmap](img1.png)

## Uso

1. Clonar el repositorio:
    
    ```sh
    git clone https://github.com/anonymous-17-03/ScanPort.git
    cd ScanPort
    ```

2. Asignar permisos de ejecución al script:
    
    ```sh
    chmod +x PortScanner.py
    ```

3. Para ejecutar el script, utiliza el siguiente comando:
    
    ```sh
    ./PortScanner.py <objetivo>
    ```

## Notas

Este script solo funciona en sistemas Unix-like debido al uso del comando ping con la opción -c.
Asegúrate de tener permisos de red adecuados para ejecutar pings y escanear puertos en el objetivo especificado.
Usa este script de manera ética y solo en sistemas sobre los que tengas permiso de realizar escaneos de red.
