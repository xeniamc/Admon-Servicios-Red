
# Press Mayús+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

'''
    PRACTICA 02: SISTEMA DE ADMINISTRACIÓN DE CONTABILIDAD
    UA: Administración de Servicios en Red | Grupo: 4CM13
    Martinez Cervantes Xenia Guadalupe
'''
from agentes import *
from threading import *

def mostrar_menu(opciones):
    print('\t\tMENÚ')
    for clave in sorted(opciones):
        print(f' {clave}) {opciones[clave][0]}')


def leer_opcion(opciones):
    while (a := input('Seleccione una opción:')) not in opciones:
        print('Opción incorrecta, vuelva a intentarlo.')
    return a


def ejecutar_opcion(opcion, opciones):
    opciones[opcion][1]()


def generar_menu(opciones, opcion_salida):
    opcion = None
    while opcion != opcion_salida:
        mostrar_menu(opciones)
        opcion = leer_opcion(opciones)
        ejecutar_opcion(opcion, opciones)
        print()


def menu_principal():
    opciones = {
        '1': ('Agregar agente', addAgent),
        '2': ('Eliminar agente', deleteAgent),
        '3': ('Generar reporte', getReport),
        '4': ('Salir', close)
    }

    generar_menu(opciones, '4')


def close():
    print('Saliendo')


if __name__ == '__main__':
    print('\n\t\tSISTEMA DE ADMINISTRACIÓN DE RED')
    print('PRACTICA NO. 02: SISTEMA DE ADMINISTRACIÓN DE CONTABILIDAD')
    print('Martinez Cervantes Xenia Guadalupe \t 4CM13\t 2020630284\n')
    menu_principal()



