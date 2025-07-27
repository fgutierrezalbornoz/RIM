import re

def clave_orden(archivo):
    # Divide el nombre y los números entre corchetes
    nombre_match = re.match(r'^(.*?\.m4a)', archivo)
    num_match = re.search(r'\[(\d+\.\d+)-', archivo)

    nombre = nombre_match.group(1) if nombre_match else ''
    inicio = float(num_match.group(1)) if num_match else float('inf')
    return (nombre, inicio)

archivos = [
    'radio-disney-ar-1.m4a [10.774-11.146]',
    'radio-disney-ar-1.m4a [100.310-100.682]',
    'radio-disney-ar-1.m4a [100.682-101.053]',
    'radio-disney-ar-1.m4a [1000.130-1000.501]',
    'radio-disney-ar-1.m4a [1000.501-1000.873]',
    'radio-disney-ar-1.m4a [11.146-11.517]',
    'radio-disney-ar-2.m4a [5.000-5.500]',
    'radio-disney-ar-1.m4a [5.000-5.500]'
]

ordenados = sorted(archivos, key=clave_orden)
print(ordenados)
