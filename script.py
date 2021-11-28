import os
from procesador import parse

carpeta = "salas-vs-personas"
n = 2

AFOROS = [[5, 5], [4, 4], [2, 2]]
PERSONAS_SALAS = [[25, 5], [10, 2], [5, 1]]
REUNIONES = []

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
    n = 2
    for i in range(n):
        path_in = os.path.join("E3", "resultados", "utilidades", "outs", f"out_{i}.txt")
        path_out = os.path.join("E3", "resultados", "utilidades", "outs", f"out_parsed_{i}.txt")
        parse(path_in, path_out)
