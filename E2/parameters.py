from faker import Faker
from random import choice


# CONJUNTOS


def personas(i):
    fake = Faker()
    return [f'{fake.name()}' for j in range(i)]


def espacios(j):
    return [f'{choice(salas)}{i + 1}' for i in range(j)]


def modulos(k):
    return [f'{day}{i + 1}' for day in days for i in range(k)]


def reuniones(L):
    return [f'Reunion{i + 1}' for i in range(L)]


# PARAMETROS FIJOS
days = ['L', 'M', 'W', 'J', 'V']
salas = ['A', 'B', 'C', 'D', 'E', 'F', 'G']

MIN_L = 0
MAX_L = 5

MIN_A = 0
MAX_A = 25

M_GRANDE = 999999
