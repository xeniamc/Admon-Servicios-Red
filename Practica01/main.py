# This is a sample Python script.

# Press Mayús+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

'''
    PRACTICA 01: ADQUISICIÓN DE INFORMACIÓN USANDO SNMP
    UA: Administración de Servicios en Red | Grupo: 4CM13
    Martinez Cervantes Xenia Guadalupe
'''
import os
from pysnmp.hlapi import *
from reportlab.pdfgen import canvas
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter

agents = {}
file = open("agentes.txt", "w+")

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

def getAgents():
    file = open("agentes.txt", "r")
    index = 0
    agents.clear()
    if file.readline() == '':
        return -1
    else:
        file.seek(0)
        for linea in file:
            list = linea.split(',')
            agents[index] = list
            index += 1
        file.close()

def addAgent():
    file = open("agentes.txt", "a")

    index = len(agents)

    print(f'Ingresa la información del nuevo agente no. {index}:')
    ip_hostname = input('IP/Hostname:')
    community = input('Comunidad:')
    port = int(input('Puerto:'))
    version =  input('Version SNMP (v1,v2,v3): ')
    '''
    ip_hostname = '192.168.1.127'
    port = 161
    community = 'comunidadASR'
    version = 'v1'
    '''
    agents[index] = [ip_hostname, community, port, version]
    file.write(ip_hostname + ',' + community + ',' + str(port) + ',' + version +'\n')
    file.close()


def deleteAgent():

    if getAgents() == -1:
        print('AUN NO SE TIENEN AGENTES REGISTRADOS. PRIMERO INTENTE AGREGAR UN AGENTE')
    else:
        print('\tAGENTES EN LA LISTA:')
        for clave in agents:
            print(f'Agente {clave}:  {agents[clave]}')

        while (del_agent := int(input('No. del agente que desea eliminar:'))) not in agents:
            print(f'El agente {del_agent} no existe. Intentelo otra vez.')

        confirm = input(f'Seguro que desea eliminar el agente {del_agent}: {agents[del_agent][0]}? S/N\t')
        print(confirm)

        if confirm == 's' or confirm == 'S':
            file = open("agentes.txt","w+")
            print(f'Se ha eliminado el agente {del_agent}: {agents.pop(del_agent)}')
            for valor in agents.values():
                file.write(str(valor)+'\n')
            file.close()
        else:
            print(f'Se cancelo la eliminacion del agente {del_agent}: {agents[del_agent][0]}')


def getReport():
    print('Reporte')


    if getAgents() == -1:
        print('AUN NO SE TIENEN AGENTES REGISTRADOS. PRIMERO INTENTE AGREGAR UN AGENTE')
    else:
        print('\tAGENTES EN LA LISTA:')
        for clave in agents:
            print(f'Agente {clave}:' + str(agents[clave]))

        while (agent_report := int(input('No. del agente del que desea generar el reporte:'))) not in agents:
            print(f'El agente {agent_report} no existe. Intentelo otra vez.')

        createPDFReport(agents[agent_report])



def createPDFReport(agent):
    w, h = letter

    pdfReport = canvas.Canvas('reportes/reporte_' + agent[0] + '.pdf', pagesize=letter)

    pdfReport.setFont('Times-Bold', 18)
    pdfReport.drawCentredString(w / 2, h - 50, 'ADMINISTRACIÓN DE SISTEMAS EN RED')
    pdfReport.setFont('Times-BoldItalic', 16)
    pdfReport.drawCentredString(w / 2, h - 70, 'Practica No. 1: Aquisición de información usando SNMP')
    pdfReport.setFont('Times-Roman', 12)
    pdfReport.drawCentredString(w / 2, h - 90, 'Alumna: Martínez Cervantes Xenia Guadalupe              Grupo: 4CM13')

    pdfReport.setStrokeColorRGB(0.58, 0.64, 0.64)
    pdfReport.line(50, h - 100, w - 50, h - 100)

    pdfReport.setFont('Helvetica-Bold', 17)
    pdfReport.drawCentredString(w / 2, h - 130, f'Reporte del Agente "{agent[0]}"')

    pdfReport.setFont('Helvetica-Bold', 12)
    pdfReport.drawString(w - 562, h - 150, 'Sistema Operativo: ')
    sistema = consultaSNMP(agent[0], agent[1], agent[2], '1.3.6.1.2.1.1.1.0')
    pdfReport.setFont('Helvetica', 10)
    pdfReport.drawString(w - 450, h - 150, f'{sistema}')
    if sistema == 'Linux' :
        pdfReport.drawImage("sistema-logos/ubuntu-logo.png", w-150, h - 230, width=100,height=100)
    if sistema == 'Windows' :
        pdfReport.drawImage("sistema-logos/win-logo.png", w - 150, h - 230, width=100, height=100)

    pdfReport.setFont('Helvetica-Bold', 12)
    pdfReport.drawString(w - 562, h - 170, 'Nombre del dispositivo: ')
    info = consultaSNMP(agent[0], agent[1], agent[2], '1.3.6.1.2.1.1.5.0')
    pdfReport.setFont('Helvetica', 10)
    pdfReport.drawString(w - 420, h - 170, f'{info}')

    pdfReport.setFont('Helvetica-Bold', 12)
    pdfReport.drawString(w - 562, h - 190, 'Información de contacto: ')
    info = consultaSNMP(agent[0], agent[1], agent[2], '1.3.6.1.2.1.1.4.0')
    pdfReport.setFont('Helvetica', 10)
    pdfReport.drawString(w - 410, h - 190, f'{info}')

    pdfReport.setFont('Helvetica-Bold', 12)
    pdfReport.drawString(w - 562, h - 210, 'Ubicación: ')
    info = consultaSNMP(agent[0], agent[1], agent[2], '1.3.6.1.2.1.1.6.0')
    pdfReport.setFont('Helvetica', 10)
    pdfReport.drawString(w - 495, h - 210, f'{info}')

    pdfReport.setFont('Helvetica-Bold', 12)
    pdfReport.drawString(w - 562, h - 230, 'No. de Interfaces: ')
    info = consultaSNMP(agent[0], agent[1], agent[2], '1.3.6.1.2.1.2.1.0')
    pdfReport.setFont('Helvetica', 10)
    pdfReport.drawString(w - 450, h - 230, f'{info}')

    pdfReport.setFont('Helvetica-Bold', 12)
    pdfReport.drawString(w - 562, h - 230, 'No. de Interfaces: ')
    no_inter = consultaSNMP(agent[0], agent[1], agent[2], '1.3.6.1.2.1.2.1.0')
    pdfReport.setFont('Helvetica', 10)
    pdfReport.drawString(w - 450, h - 230, f'{no_inter}')


    xlist = [153,306,459]
    ylist = []
    ylist_newpage = []
    y = 522
    padding = 13

    pdfReport.grid(xlist,[542,522])
    pdfReport.drawCentredString(229, 542 - padding, 'Interfaz')
    pdfReport.drawCentredString(382, 542 - padding, 'Estado')

    for i in range(1, int(no_inter) + 2, 1):
        if i < 26:
            ylist.append(y)
            y = y - 20
        else:
            if i == 26:
                y = h - 50
            y = y - 20
            ylist_newpage.append(y)
        if i <= int(no_inter) :
            inter_descr = consultaSNMP(agent[0], agent[1], agent[2], f'1.3.6.1.2.1.2.2.1.2.{i}')
            pdfReport.drawString(xlist[0]+padding, y + 20 - padding, inter_descr)

            inter_state = consultaSNMP(agent[0], agent[1], agent[2], f'1.3.6.1.2.1.2.2.1.7.{i}')
            pdfReport.drawString(xlist[1] + padding, y + 20 - padding, inter_state)


    pdfReport.setStrokeColorRGB(0,0,0)
    pdfReport.grid(xlist,ylist)

    if ylist_newpage:
        pdfReport.showPage()
        pdfReport.grid(xlist,ylist_newpage)

    pdfReport.save()
    print('El reporte se ha generado existosamente!')


def consultaSNMP(host,community,port,oid):

    errorIndication, errorStatus, errorIndex, varBinds = next(
        getCmd(SnmpEngine(),
               CommunityData(community),
               UdpTransportTarget((host, port)),
               ContextData(),
               ObjectType(ObjectIdentity(oid))))

    if errorIndication:
        print(errorIndication)
    elif errorStatus:
        print('%s at %s' % (errorStatus.prettyPrint(),errorIndex and varBinds[int(errorIndex) - 1][0] or '?'))
    else:
        for varBind in varBinds:
            varB = (' = '.join([x.prettyPrint() for x in varBind]))
            resultado = varB.split()[2]
    return resultado

def close():
    print('Saliendo')


if __name__ == '__main__':
    print('\n\t\tSISTEMA DE ADMINISTRACIÓN DE RED')
    print('PRACTICA NO. 1: ADQUISICIÓN DE INFORMACIÓN USANDO SNMP')
    print('Martinez Cervantes Xenia Guadalupe \t 4CM13\t 2020630284\n')
    menu_principal()
