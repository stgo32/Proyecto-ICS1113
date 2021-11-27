from pprint import pprint


def parse_line(line, name) -> list:
    """
    Parse a line of the output of gurobi and returns
    the data that contains that line and the result of the
    line
    input: name of the field
    output: data->list
    """
    while line[-1] == " ":
        line = line[:-1]
    line = line[:-1]
    info = line.split("            ")
    result = info[1]
    data = info[0].strip(name)[1:-1].split(",")
    return data


espacios = set()
personas = set()
reuniones = set()


def build_reunion(reunion, reuniones):
    if reunion not in reuniones:
        reuniones[reunion] = {
            "personas": [],
            "sala": '',
            "modulo": '',
            "presencialidad": '0',
        }

"""
{
    reunion1: personas: [p1,p2,p3],
    sala: sala1,
    modulo: mod1,
    presencialidad: pres,
}
"""
reuniones = {
}
with open("out.txt", "r") as file:
    lines = file.readlines()

    for line in lines:
        if "asistencia" in line:
            data = parse_line(line, "asistencia")
            persona, sala, modulo, reunion = data

            build_reunion(reunion, reuniones)
            reuniones[reunion]["personas"].append(persona)
            reuniones[reunion]["sala"] = sala
            reuniones[reunion]["modulo"] = modulo
        elif "disponibilidad_espacio" in line:
            data = parse_line(line, "disponibilidad_espacio")
            sala, modulo, reunion = data
            build_reunion(reunion, reuniones)
            reuniones[reunion]["sala"] = sala
        elif "presencialidad" in line:
            data = parse_line(line, "presencialidad")
            reunion = data[0]
            build_reunion(reunion, reuniones)
            reuniones[reunion]["presencialidad"] = True


pprint(reuniones)
