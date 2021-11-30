import os
from procesador import parse

carpeta = "salas-vs-personas"
n = 2

AFOROS = [[5, 5], [4, 4], [2, 2]]
# Al variar los aforos el modelo sigue funcionando hasta que son tan restringidos que
# no se pueden realizar las reuniones
PERSONAS_SALAS = [[25, 5], [25, 3], [25, 1]]
# [Cantidad de personas, cantidad de salas]
# Al variar las salas el modelo sigue funcionando hasta que son tan restringidas que
# no se pueden realizar las reuniones

n = 0

analisis = "parse"

if analisis == "aforos":
    for aforo in AFOROS:
        aforo_min = aforo[0]
        aforo_max = aforo[1]
        os.system(f"python E2\\model.py 8 8 9 8 {aforo_min} {aforo_max} 0 5 > E3\\resultados\\{analisis}\\outs\\out_parsed_{n}.txt")
        n += 1

elif analisis == "personas-salas":
    for personas_salas in PERSONAS_SALAS:
        personas = personas_salas[0]
        salas = personas_salas[1]
        print(personas)
        print(salas)
        os.system(f"python E2\\model.py 8 8 9 8 0 25 {personas} {salas} > E3\\resultados\\{analisis}\\outs\\out_parsed_{n}.txt")
        #os.system(f"python E2\\model.py 8 8 9 8 0 25 {personas} {salas} > E3\\resultados\\{analisis}\\outs\\out_parsed_{n}.txt")

elif analisis == "reuniones":
    for personas_salas in PERSONAS_SALAS:
        personas = personas_salas[0]
        salas = personas_salas[1]
        os.system(f"python E2\\model.py 8 8 9 8 0 25 {personas} {salas} > E3\\resultados\\{analisis}\\outs\\out_parsed_{n}.txt")


if analisis == "parse":
    
    path_in = os.path.join("E3", "resultados", "utilidades_reuniones", f"out_3.txt")
    path_out = os.path.join("E3", "resultados", "utilidades_reuniones", f"out_parsed_3.txt")
    parse(path_in, path_out)
    n = 2
    #for i in range(n):
    #    path_in = os.path.join("E3", "resultados", "utilidades_reuniones", f"out_{i}.txt")
    #    path_out = os.path.join("E3", "resultados", "utilidades_reuniones", f"out_parsed_{i}.txt")
    #    parse(path_in, path_out)
