import sys

print("DEBUG", sys.argv)

days = ['L', 'M', 'W', 'J', 'V']
salas = ['A', 'B', 'C', 'D', 'E', 'F', 'G']

CAMBIAR_PERSONAS = 1
CAMBIAR_SALAS = 1
CAMBIAR_MODULOS = 1
CAMBIAR_REUNIONES = 1

if len(sys.argv) > 1:
    CANTIDAD_PERSONAS = int(sys.argv[1])
    CANTIDAD_ESPACIOS_FISICOS = int(sys.argv[2])
    CANTIDAD_MODULOS = int(sys.argv[3])
    CANTIDAD_REUNIONES = int(sys.argv[4])

    MIN_A = int(sys.argv[5])
    MAX_A = int(sys.argv[6])

    MIN_L = int(sys.argv[7])
    MAX_L = int(sys.argv[8])

else:
    CANTIDAD_PERSONAS = 8
    CANTIDAD_ESPACIOS_FISICOS = 9
    CANTIDAD_MODULOS = 9
    CANTIDAD_REUNIONES = 5

    MIN_A = 0
    MAX_A = 25

    MIN_L = 0
    MAX_L = 5

M_GRANDE = 999999
