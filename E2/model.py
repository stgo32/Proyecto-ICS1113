from gurobipy import GRB, Model, quicksum
from randomizer import randomize
from parameters import M_GRANDE


personas, espacios, modulos, reuniones, disponibilidad_i_k, disponibilidad_j_k, \
    clave_i_l, min_l, max_l, aforo_j, utilidades_i, utilidades_l = randomize(3, 3, 2, 3)

model = Model('Optimizacion del Uso de Espacios en los Colegios dado el Contexto en Pandemia')

# variables
x = model.addVars(
    personas, espacios, modulos, reuniones,
    vtype=GRB.BINARY,
    name='asistencia'
    )
de = model.addVars(
    espacios, modulos, reuniones,
    vtype=GRB.BINARY,
    name='disponibilidad_espacio'
)
pr = model.addVars(
    reuniones,
    vtype=GRB.BINARY,
    name='presencialidad'
)

# se agregan variables al modelo
model.update()

# RESTRICCIONES
# 2.5.1. cantidad de participantes
model.addConstrs(
    (quicksum(
        x[persona, espacio, modulo, reunion]
        for persona in personas
        for espacio in espacios
        for modulo in modulos
        # for reunion in reuniones
    ) >= min_l[r_index]
        for r_index, reunion in enumerate(reuniones)),
    name='cantidad_participantes(1)'
)

# model.addConstrs(
#     (quicksum(
#         x[persona, espacio, modulo, reunion]
#         for persona in personas
#         for espacio in espacios
#         for modulo in modulos
#         # for reunion in reuniones
#     ) >= pr[reunion]
#         for reunion in reuniones),
#     name='cantidad_participantes(2)'
# )

# 2.5.2. disponibilidad participantes
model.addConstrs(
    (disponibilidad_i_k[persona, modulo] >= x[persona, espacio, modulo, reunion]
        for persona in personas
        for espacio in espacios
        for modulo in modulos
        for reunion in reuniones),
    name='disponibilidad_participantes'
)

# 2.5.3. no clonacion de personas
model.addConstrs(
    (quicksum(
        x[persona, espacio, modulo, reunion]
        for espacio in espacios
        for reunion in reuniones
    ) <= 1
        for persona in personas
        for modulo in modulos
    ),
    name='no_clonacion'
)

# 2.5.4. aforos
model.addConstrs(
    (quicksum(
        x[persona, espacio, modulo, reunion]
        for persona in personas
        for reunion in reuniones
    ) <= aforo_j[e_index]
        for e_index, espacio in enumerate(espacios)
        for modulo in modulos
    ),
    name='aforos'
)

# 2.5.5. disponibilidad espacios fisicos
model.addConstrs(
    (quicksum(
        de[espacio, modulo, reunion]
        for reunion in reuniones
    ) <= 1
        for espacio in espacios
        for modulo in modulos
    ),
    name='disp_espacio_fisico(1)'
)

model.addConstrs(
    (quicksum(
        x[persona, espacio, modulo, reunion]
        for persona in personas
    ) <= M_GRANDE * de[espacio, modulo, reunion]
        for espacio in espacios
        for modulo in modulos
        for reunion in reuniones
    ),
    name='disp_espacio_fisico(2)'
)

model.addConstrs(
    (quicksum(
        de[espacio, modulo, reunion]
        for espacio in espacios
        for modulo in modulos
    ) <= pr[reunion]
        for reunion in reuniones
    ),
    name='disp_espacio_fisico(3)'
)

# 2.5.6. participantes clave
model.addConstrs(
    (quicksum(
        x[persona, espacio, modulo, reunion]
        for espacio in espacios
        for modulo in modulos
    ) <= clave_i_l[persona, reunion]
        for persona in personas
        for reunion in reuniones
    ),
    name='participantes_clave'
)

# 2.5.7. reuniones exclusivas
model.addConstrs(
    (quicksum(
        x[persona, espacio, modulo, reunion]
        for persona in personas
        for espacio in espacios
        for modulo in modulos
        # for reunion in reuniones
    ) <= max_l[r_index]
        for r_index, reunion in enumerate(reuniones)),
    name='reuniones_exclusivas'
)

# FUNCION OBJETIVO
obj = (
    quicksum(
        x[persona, espacio, modulo, reunion] * utilidades_i[persona]
        for persona in personas
        for espacio in espacios
        for modulo in modulos
        for reunion in reuniones
    )) + (quicksum(
        pr[reunion] * utilidades_l[reunion]
        for reunion in reuniones
    )
)
model.setObjective(obj, GRB.MAXIMIZE)
model.optimize()

# Mostrar los valores de las soluciones
model.printAttr("x")
print("\n-------------\n")
# Imprime las holguras de las restricciones (0 significa que la restricción es activa.
# for constr in model.getConstrs():
#     print(constr, constr.getAttr("slack"))

print(model)
