# CC5213 - TAREA 2 - RECUPERACIÓN DE INFORMACIÓN MULTIMEDIA
# Fecha: 08 de mayo de 2025
# Alumno: Francisco Gutiérrez Albornoz

import sys
import os
import util as util

def tarea2_parte3(carpeta_ventanas_similares, archivo_salida_detecciones_txt):
    if not os.path.isdir(carpeta_ventanas_similares):
        print("ERROR: no existe carpeta {}".format(carpeta_ventanas_similares))
        sys.exit(1)
    elif os.path.exists(archivo_salida_detecciones_txt):
        print("ERROR: ya existe {}".format(archivo_salida_detecciones_txt))
        sys.exit(1)
    #
    # Implementar la tarea con los siguientes pasos:
    #
    #  1-leer el o los archivos en carpeta_ventanas_similares (fue creado por tarea2_parte2)
    #    puede servir la funcion util.leer_objeto() que está definida en util.py
    #
    
    ventanas_similares = util.leer_objeto(carpeta_ventanas_similares, 'ventanas_similares.bin')
    
    #  2-crear un algoritmo para buscar secuencias similares entre audios
    #    ver material de la semanas 5 y 7
    #    identificar grupos de ventanas de Q y R que son similares y pertenecen a las mismas canciones con el mismo desfase
    
    #algoritmo que implementa sistema de votaciones (sacado de material docente y levemente adaptado)
    contadores = dict()
    for medicion in ventanas_similares:
        nombre_q, inicio_q, fin_q, nombre_r, inicio_r, fin_r, dist = medicion
        ventana_q = util.Ventana(nombre_archivo=nombre_q.split(" [")[0], segundos_desde=float(inicio_q), segundos_hasta=float(fin_q))
        ventana_r = util.Ventana(nombre_archivo=nombre_r.split(" [")[0], segundos_desde=float(inicio_r), segundos_hasta=float(fin_r))
        query = ventana_q
        conocido = ventana_r
        diferencia = abs(conocido.segundos_desde - query.segundos_desde)
        # llave para acumular (se podría mejorar la acumulación si la diferencia se redondea)
        key = "{}-{}-{:4.1f}".format(query.nombre_archivo, conocido.nombre_archivo, diferencia)
        # ver si hay votos anteriores
        votos = contadores.get(key)
        if votos is None:
            # se inicia votacion por ese desfase
            votos = util.Votos(key, query, conocido)
            contadores[key] = votos
        else:
            # suma un voto a una deteccion encontrada previamente con el mismo desfase
            votos.addVoto(query, conocido)
    #  3-escribir las detecciones encontradas en archivo_salida_detecciones_txt:
    #    columna 1: nombre de archivo Q (nombre de archivo en carpeta radio)
    #    columna 2: tiempo de inicio (número decimal, tiempo en segundos del inicio de la detección)
    #    columna 3: nombre de archivo R (nombre de archivo en carpeta canciones)
    #    columna 4: confianza (número decimal, mientras más alto mayor confianza que la respuesta es correcta)
    #   le puede servir la funcion util.escribir_lista_de_columnas_en_archivo() que está definida util.py
    allVotos = list(contadores.values())
    detecciones = []
    for v in sorted(allVotos, key = lambda x : x.numVotos, reverse=True):
        if v.numVotos > 5: #se considera toda ventana con votos > 5 que equivale a 0.5 segundos con los parámetros utilizados
            confianza = v.numVotos / len(allVotos)
            deteccion = [
                v.query_nombre,
                v.query_inicio,
                v.conocido_nombre,
                confianza]
            detecciones.append(deteccion)

    util.escribir_lista_de_columnas_en_archivo(detecciones, archivo_salida_detecciones_txt)



# inicio de la tarea
if len(sys.argv) != 3:
    print("Uso: {} [carpeta_ventanas_similares] [archivo_salida_detecciones_txt]".format(sys.argv[0]))
    sys.exit(1)

# lee los parametros de entrada
carpeta_ventanas_similares = sys.argv[1]
archivo_salida_detecciones_txt = sys.argv[2]

# llamar a la tarea
tarea2_parte3(carpeta_ventanas_similares, archivo_salida_detecciones_txt)
