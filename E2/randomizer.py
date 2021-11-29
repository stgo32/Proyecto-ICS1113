from os import write
import random
from faker import Faker
import parameters as p
from read_csv import read_simple_csv
import sys

#seed = random.randrange(sys.maxsize)
seed = 5933002158754574543
random.seed(seed)
Faker.seed(seed)
print("Seed was:", seed)


def set_personas(i):
    fake = Faker()
    return [f'{fake.name()}' for j in range(i)]


def set_espacios(j):
    esp = []
    for i in range(j):
        esp.append(f'{random.choice(p.salas)}{i + 1}')
    return esp


def set_modulos(k):
    return [f'{day}{i + 1}' for day in p.days for i in range(k)]


def set_reuniones(L):
    return [f'Reunion{i + 1}' for i in range(L)]


def disponibilidad_i_k(personas, modulos):
    disponibilidad = {}
    for i in personas:
        for m in modulos:
            disponibilidad[(i, m)] = random.randint(0, 1)
    return disponibilidad


def disponibilidad_j_k(espacios, modulos):
    disponibilidad = {}
    for e in espacios:
        for m in modulos:
            disponibilidad[(e, m)] = random.randint(0, 1)
    return disponibilidad


def clave_i_l(personas, reuniones):
    disponibilidad = {}
    for i in personas:
        for r in reuniones:
            disponibilidad[(i, r)] = random.randint(0, 1)
    return disponibilidad


def min_l(reuniones, min_, max_):
    min_l = []
    for r in reuniones:
        min_l.append(random.randint(min_, max_))
    return min_l


def max_l(reuniones, min_l, max_):
    max_l = []
    for r in range(len(reuniones)):
        max_l.append(random.randint(min_l[r], max_))
    return max_l


def aforo_j(espacios, min_, max_):
    aforos = []
    for e in espacios:
        aforos.append(random.randint(min_, max_))
    return aforos


def utilidades_i(personas):
    util = {}
    for i in personas:
        util[i] = round(random.uniform(0, 1), 3)
    return util


def utilidades_l(reuniones):
    util = {}
    for r in reuniones:
        util[r] = round(random.uniform(0, 1), 3)
    return util


def costos_l(reuniones):
    costo = {}
    for r in reuniones:
        costo[r] = round(random.uniform(0, 1), 3)
    return costo


def presencialidad(espacios):
    p = {}
    for e in espacios:
        if e == 'Remoto':
            p['Remoto'] = 0
        else:
            p[e] = 1
    return p


def randomize(i, j, k, L, new={"personas": 1, "salas": 1, "modulos": 1, "reuniones": 1}):
    """
    i -> int cantidad de personas
    j -> int cantidad de espacios
    k -> int cantidad de modulos
    l -> int cantidad de reuniones
    """
    if new["personas"]:
        personas = set_personas(i)
    else:
        personas = read_simple_csv('personas')

    if new["salas"]:
        espacios = set_espacios(j)
    else:
        espacios = read_simple_csv('espacios')

    if new["modulos"]:
        modulos = set_modulos(k)
    else:
        modulos = read_simple_csv('modulos')

    if new["reuniones"]:
        reuniones = set_reuniones(L)
    else:
        reuniones = read_simple_csv('reuniones')

    disp_i_k = disponibilidad_i_k(personas, modulos)
    disp_j_k = disponibilidad_j_k(espacios, modulos)
    clave = clave_i_l(personas, reuniones)
    m_l = min_l(reuniones, p.MIN_L, p.MAX_L)
    maxx_l = max_l(reuniones, m_l, p.MAX_L)
    af_j = aforo_j(espacios, p.MIN_A, p.MAX_A)
    util_i = utilidades_i(personas)
    util_l = utilidades_l(reuniones)
    costo_l = costos_l(reuniones)
    pre = presencialidad(espacios)

    """
    print('------------------------------------------------------')
    print(personas)
    print(espacios)
    print(modulos)
    print(reuniones)
    print('======================================================')
    print(f'disponibilidad_i_k: {disp_i_k}')
    print(f'disponibilidad_j_k: {disp_j_k}')
    print(f'clave_i_l: {clave}')
    print(f'min_l: {m_l}')
    print(f'max_l: {maxx_l}')
    print(f'aforo_j: {af_j}')
    print(f'utilidades_i: {util_i}')
    print(f'utilidades_l: {util_l}')
    print('------------------------------------------------------')
    """

    #i: Personas
    #j: Salas
    #k: Modulos
    #l: Reuniones
    with open('E2/DB/personas.csv', 'w') as file:
        for persona in personas:
            file.write(f'{persona}\n')
    with open('E2/DB/espacios.csv', 'w') as file:
        for esp in espacios:
            file.write(f'{esp}\n')
    with open('E2/DB/modulos.csv', 'w') as file:
        for mod in modulos:
            file.write(f'{mod}\n')
    with open('E2/DB/reuniones.csv', 'w') as file:
        for reu in reuniones:
            file.write(f'{reu}\n')
    with open('E2/DB/disponibilidad_i_k.csv', 'w') as file:
        file.write('Nombre,Modulo,Valor\n')
        for key, value in disp_i_k:
            a = (f'{key}', f'{value}')
            b = disp_i_k[a]
            file.write(f'{key},{value},{b}\n')
    with open('E2/DB/disponibilidad_j_k.csv', 'w') as file:
        file.write('Espacio,Modulo,Valor\n')
        for key, value in disp_j_k:
            a = (f'{key}', f'{value}')
            b = disp_j_k[a]
            file.write(f'{key},{value},{b}\n')
    with open('E2/DB/clave_i_l.csv', 'w') as file:
        file.write('Nombre,Reunion,Valor\n')
        for key, value in clave:
            a = (f'{key}', f'{value}')
            b = clave[a]
            file.write(f'{key},{value},{b}\n')
    with open('E2/DB/min_l.csv', 'w') as file:
        for reu in m_l:
            file.write(f'{reu}\n')
    with open('E2/DB/max_l.csv', 'w') as file:
        for reu in maxx_l:
            file.write(f'{reu}\n')
    with open('E2/DB/aforo_j.csv', 'w') as file:
        for reu in af_j:
            file.write(f'{reu}\n')
    with open('E2/DB/utilidades_i.csv', 'w') as file:
        file.write('Nombre,Utilidad\n')
        for key in util_i:
            file.write(f'{key},{util_i[str(key)]}\n')
    with open('E2/DB/utilidades_l.csv', 'w') as file:
        file.write('Reunion,Utilidad\n')
        for key in util_l:
            file.write(f'{key},{util_l[str(key)]}\n')
    with open('E2/DB/costos_l.csv', 'w') as file:
        file.write('Reunion,Costo\n')
        for key in costo_l:
            file.write(f'{key},{costo_l[str(key)]}\n')
    with open('E2/DB/presencialidad.csv', 'w') as file:
        file.write('Espacio,Valor\n')
        for key in pre:
            file.write(f'{key},{int(pre[str(key)])}\n')

    return personas, espacios, modulos, reuniones, disp_i_k, \
        disp_j_k, clave, m_l, maxx_l, af_j, util_i, util_l, costo_l, pre


if __name__ == '__main__':
    new = {"personas": 1, "salas": 0, "modulos": 0, "reuniones": 0}
    randomize(10, 12, 9, 8, new)
