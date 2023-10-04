import json

__author__ = 'REBECA GONZÁLEZ BALADO'

# lista de vehiculos
listavehiculos = []


class Vehiculo:
    def __init__(self, valores):
        self.matricula = valores[0]
        self.numbastidor = valores[1]
        self.marca = valores[2]
        self.modelo = valores[3]
        self.color = valores[4]
        self.annomatriculacion = valores[5]
        self.tipo = valores[6]
        self.alias = valores[7]

    def __str__(self):
        return f'Vehiculo {self.alias}[Matrícula: {self.matricula}, Núm. bastidor: {self.numbastidor}, ' \
               f'Marca: {self.marca}, Modelo: {self.modelo}, Color: {self.color}, ' \
               f'Año de matriculación: {self.annomatriculacion}, Tipo: {self.tipo}] '


# importa los vehiculos del json a una lista
def importarvehiculos():
    print('\nImportando vehículos...')

    try:
        # cargamos la lista de vehiculos del json
        vehiculos = open('vehiculos.json')
        datos = json.load(vehiculos)

        for d in datos['vehiculos']:
            listavalores = [d['matricula'], d['numbastidor'], d['marca'], d['modelo'], d['color'],
                            d['annomatriculacion'], d['tipo'], d['alias']]
            vehiculo = Vehiculo(listavalores)
            listavehiculos.append(vehiculo)

        vehiculos.close()

    # si el json no existe o esta vacio, ignoramos la importacion
    except (FileNotFoundError, json.decoder.JSONDecodeError):
        print('No hay contactos a importar.')
    else:
        print('Contactos importados satisfactoriamente.')


# graba la lista en el fichero json
def escribirjson():
    # ordenamos albafeticamente la lista
    listavehiculos.sort(key=lambda cont: cont.matricula)

    # mapeamos los objetos de la lista
    listadict = []
    for vehiculo in listavehiculos:
        listadict.append(vehiculo.__dict__)

    vehiculos = {
        'vehiculos': listadict
    }

    # volcamos la lista de vehiculos a json
    with open('vehiculos.json', 'w') as salida:
        json.dump(vehiculos, salida, indent=3)


# muestra la lista de vehiculos existentes
def listarvehiculos():
    print('\nLista vehículos')

    # si esta vacia, no recorremos la lista
    if len(listavehiculos) == 0:
        print('La lista de vehículos se encuentra vacía.')

    # si existen vehiculos, imprimimos la lista
    else:
        for vehiculo in listavehiculos:
            print(vehiculo)


# agrega un nuevo vehiculo a partir de sus datos y lo guarda en un json
def agregarvehiculo():
    print('\nAgregar vehículo')

    listapeticiones = ['la matrícula', 'el número de bastidor', 'la marca', 'el modelo', 'el color',
                       'el año de matriculación', 'el tipo', 'el alias']
    listavalores = []

    for peticion in listapeticiones:
        while True:
            valor = str(input('Introduzca ' + peticion + ': '))

            # comprobamos que la string no esta vacia
            if len(valor) > 0:
                listavalores.append(valor)
                break
            else:
                print('Introduzca un valor válido.\n')

    # añadimos el nuevo vehiculo
    vehiculo = Vehiculo(listavalores)
    listavehiculos.append(vehiculo)

    # guardamos los cambios en el fichero json
    escribirjson()


# busca vehiculos a partir de su matricula o alias y/o los elimina
def buscareliminarvehiculo(eliminar):
    while True:
        if eliminar:
            print('\nEliminar vehículo')
        else:
            print('\nBuscar vehículo')

        print('M - Matrícula')
        print('A - Alias')
        print('X - Volver')
        opcion = str(input('\nElija un parámetro con el que buscar: '))

        # selector menu
        if opcion.casefold() == 'm':
            matricula = str(input('\nIntroduzca la matrícula a buscar: '))
            buscareliminarfun(eliminar, 1, matricula)
            break

        elif opcion.casefold() == 'a':
            alias = str(input('\nIntroduzca el alias a buscar: '))
            buscareliminarfun(eliminar, 2, alias)
            break

        elif opcion.casefold() == 'x':
            break
        else:
            print('Elige una opción válida.')


def buscareliminarfun(eliminar, tipo, valor):
    # buscamos todos los valores que coincidan
    listavehiculoseliminar = []

    for vehiculo in listavehiculos:
        if (tipo == 1 and vehiculo.matricula == valor) or (tipo == 2 and vehiculo.alias == valor):
            listavehiculoseliminar.append(vehiculo)
            print(f'{len(listavehiculoseliminar)}: {vehiculo}')

    if len(listavehiculoseliminar) == 0:
        print('No se encontró ningún vehículo con el parámetro introducido.')

    # si esta en modo eliminar, elegimos un vehiculo a eliminar
    elif eliminar:
        while True:
            try:
                vehiculoeliminar = int(input('\nElija un vehículo a eliminar (introduzca su número): '))
                if vehiculoeliminar < 1:
                    raise ValueError()

                # eliminamos el vehiculo introducido de la lista de vehiculos
                for vehiculo in listavehiculos:
                    if vehiculo == listavehiculoseliminar[vehiculoeliminar - 1]:
                        listavehiculos.remove(vehiculo)

                # guardamos los cambios en el fichero json
                escribirjson()

                break

            except (ValueError, IndexError):
                print('Introduzca un valor válido.')


# impresion menu
def menu():
    while True:
        print('\nGestión de vehículos')
        print('L - Listar vehículos')
        print('A - Agregar vehículo')
        print('B - Buscar vehículo')
        print('E - Eliminar vehículo')
        print('X - Salir')
        opcion = str(input('\nElija una opción: '))

        # selector menu
        if opcion.casefold() == 'l':
            listarvehiculos()
        elif opcion.casefold() == 'a':
            agregarvehiculo()
        elif opcion.casefold() == 'b':
            buscareliminarvehiculo(False)
        elif opcion.casefold() == 'e':
            buscareliminarvehiculo(True)
        elif opcion.casefold() == 'x':
            break
        else:
            print('Elige una opción válida.')


def main():
    importarvehiculos()
    menu()


if __name__ == '__main__':
    main()
