from random import randint, uniform
import parameters as p


def disponibilidad_i_k(personas, modulos):
    disponibilidad = {}
    for i in personas:
        for m in modulos:
            disponibilidad[(i, m)] = randint(0, 1)
    return disponibilidad


def disponibilidad_j_k(espacios, modulos):
    disponibilidad = {}
    for e in espacios:
        for m in modulos:
            disponibilidad[(e, m)] = randint(0, 1)
    return disponibilidad


def reuniones_i_l(personas, reuniones):
    disponibilidad = {}
    for i in personas:
        for r in reuniones:
            disponibilidad[(i, r)] = randint(0, 1)
    return disponibilidad


def min_l(reuniones, min_, max_):
    min_l = []
    for r in reuniones:
        min_l.append(randint(min_, max_))
    return min_l


def aforo_j(espacios, min_, max_):
    aforos = []
    for e in espacios:
        aforos.append(randint(min_, max_))
    return aforos


def utilidades_i(personas):
    util = {}
    for i in personas:
        util[i] = round(uniform(0, 1), 3)
    return util


def utilidades_l(reuniones):
    util = {}
    for r in reuniones:
        util[r] = round(uniform(0, 1), 3)
    return util


def randomize(i, j, k, L):
    personas = p.personas(i)
    espacios = p.espacios(j)
    modulos = p.modulos(k)
    reuniones = p.reuniones(L)

    disp_i_k = disponibilidad_i_k(personas, modulos)
    disp_j_k = disponibilidad_j_k(espacios, modulos)
    reu_i_l = reuniones_i_l(personas, reuniones)
    m_l = min_l(reuniones, p.MIN_L, p.MAX_L)
    af_j = aforo_j(espacios, p.MIN_A, p.MAX_A)
    util_i = utilidades_i(personas)
    util_l = utilidades_l(reuniones)

    print('------------------------------------------------------')
    print(personas)
    print(espacios)
    print(modulos)
    print(reuniones)
    print('======================================================')
    print(f'disponibilidad_i_k: {disp_i_k}')
    print(f'disponibilidad_j_k: {disp_j_k}')
    print(f'reuniones_i_l: {reu_i_l}')
    print(f'min_l: {m_l}')
    print(f'aforo_j: {af_j}')
    print(f'utilidades_i: {util_i}')
    print(f'utilidades_l: {util_l}')
    print('------------------------------------------------------')

    return personas, espacios, modulos, reuniones, \
        disp_i_k, disp_j_k, reu_i_l, m_l, af_j, util_i, util_l
