from gurobipy import GRB, Model, quicksum
import gurobipy
from randomizer import randomize
from parameters import (M_GRANDE, CANTIDAD_PERSONAS, CANTIDAD_ESPACIOS_FISICOS,
                        CANTIDAD_MODULOS, CANTIDAD_REUNIONES, CAMBIAR_PERSONAS,
                        CAMBIAR_SALAS, CAMBIAR_MODULOS, CAMBIAR_REUNIONES)
from read_csv import read_simple_csv, read_dict_csv_int, read_dict_csv_float

def solve_model():
    #new = {"personas": CAMBIAR_PERSONAS, "salas": CAMBIAR_SALAS, "modulos": CAMBIAR_MODULOS, "reuniones": CAMBIAR_REUNIONES}
    #personas, espacios, modulos, reuniones, disponibilidad_i_k, disponibilidad_j_k, clave_i_l, min_l, \
    #        max_l, aforo_j, utilidades_i, utilidades_l, costos_l, presencialidad = randomize(CANTIDAD_PERSONAS, CANTIDAD_ESPACIOS_FISICOS, CANTIDAD_MODULOS, CANTIDAD_REUNIONES, new)

    personas = read_simple_csv('personas')
    espacios = read_simple_csv('espacios')
    modulos = read_simple_csv('modulos')
    reuniones = read_simple_csv('reuniones')
    disponibilidad_i_k = read_dict_csv_int('disponibilidad_i_k')
    disponibilidad_j_k = read_dict_csv_int('disponibilidad_j_k')
    clave_i_l = read_dict_csv_int('clave_i_l')
    min_l = read_simple_csv('min_l')
    max_l = read_simple_csv('max_l')
    aforo_j = read_simple_csv('aforo_j')
    utilidades_i = read_dict_csv_float('utilidades_i')
    utilidades_l = read_dict_csv_float('utilidades_l')
    costos_l = read_dict_csv_float('costos_l')
    presencialidad = read_dict_csv_float('presencialidad')

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
            # if espacio != 'Remoto'
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
            # if espacio != 'Remoto'
        ) <= pr[reunion]
            for reunion in reuniones
        ),
        name='disp_espacio_fisico(3)'
    )

    # model.addConstr(
    #     (quicksum(pr['Reunion1'] for i in range(3)) <= 0),
    #     name='disp_espacio_fisico(4)'
    # )

    # model.addConstrs(
    #     (pr[reunion] == presencialidad[espacio]
    #         for espacio in espacios
    #         for reunion in reuniones),
    #     name='si_remoto_no_presencial'
    # )

    # model.addConstrs(
    #     (de['Remoto', modulo, reunion] >= pr[reunion] + 1
    #         for modulo in modulos
    #         for reunion in reuniones),
    #     name='fuck'
    # )

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
        (quicksum(
            x[persona, espacio, modulo, reunion] * utilidades_i[persona]
            for persona in personas
            for espacio in espacios
            for modulo in modulos
            for reunion in reuniones
        )) + (quicksum(
            pr[reunion] * utilidades_l[reunion] + utilidades_l[reunion]/3 * (1 - pr[reunion])
            for reunion in reuniones
        ))
    )
    model.setObjective(obj, GRB.MAXIMIZE)
    model.optimize()

    # Mostrar los valores de las soluciones
    model.printAttr("x")
    print("\n-------------\n")
    # Imprime las holguras de las restricciones (0 significa que la restricción es activa.
    # for constr in model.getConstrs():
    #     print(constr, constr.getAttr("slack"))

    return(model)


if __name__ == "__main__":
    solved = 0
    #while not solved:
    #    try: 
    #        model = solve_model()
    #        solved = 1
    #        model.write("out.sol")
    #    except gurobipy.GurobiError:
    #        print("No se pudo resolver")
    #    except Exception as error:
    #        print(error)
    #        break
    model = solve_model()