import os

carpeta = "salas-vs-personas"
n = 2

AFOROS = [[80, 100], [50, 60], [30, 40], [2, 5]]
PERSONAS_SALAS = [[25, 5], [10, 2], [5, 1]]
REUNIONES = []

n = 0

analisis = "personas-salas"

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
        os.system(f"python E2\\model.py 8 8 9 8 0 25 {personas} {salas} > E3\\resultados\\{analisis}\\outs\\out_parsed_{n}.txt")

elif analisis == "reuniones":
    for personas_salas in PERSONAS_SALAS:
        personas = personas_salas[0]
        salas = personas_salas[1]
        os.system(f"python E2\\model.py 8 8 9 8 0 25 {personas} {salas} > E3\\resultados\\{analisis}\\outs\\out_parsed_{n}.txt")

#os.system(f"python parser.py > E3\\resultados\\{carpeta}\\out_parsed{n}.txt")
