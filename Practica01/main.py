
# Press Mayús+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

'''
    PRACTICA 01: ADQUISICIÓN DE INFORMACIÓN USANDO SNMP
    UA: Administración de Servicios en Red | Grupo: 4CM13
    Martinez Cervantes Xenia Guadalupe
'''
from pysnmp.hlapi import *
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from datetime import datetime

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
    '''
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

    agents[index] = [ip_hostname, community, port, version]
    file.write(ip_hostname + ',' + community + ',' + str(port) + ',' + version +',\n')
    file.close()


def deleteAgent():

    if getAgents() == -1:
        print('AUN NO SE TIENEN AGENTES REGISTRADOS. PRIMERO INTENTE AGREGAR UN AGENTE')
    else:
        print('\tAGENTES EN LA LISTA:')
        for clave in agents:
            print(f'AGENTE {clave}:  {agents[clave][0]}, {agents[clave][1]}, {agents[clave][2]}, {agents[clave][3]}')

        while (del_agent := int(input('No. del agente que desea eliminar:'))) not in agents:
            print(f'El agente {del_agent} no existe. Intentelo otra vez.')

        confirm = input(f'Seguro que desea eliminar el agente {del_agent}: {agents[del_agent][0]}? S/N\t')
        print(confirm)

        if confirm == 's' or confirm == 'S':
            file = open("agentes.txt","w+")
            print(f'Se ha eliminado el agente {del_agent}: {agents.pop(del_agent)}')
            for valor in agents.values():
                file.write(valor[0]+','+valor[1]+','+valor[2]+','+valor[3]+',\n')
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
            print(f'AGENTE {clave}:  {agents[clave][0]}, {agents[clave][1]}, {agents[clave][2]}, {agents[clave][3]}')

        while (agent_report := int(input('No. del agente del que desea generar el reporte:'))) not in agents:
            print(f'El agente {agent_report} no existe. Intentelo otra vez.')

        createPDFReport(agents[agent_report])



def createPDFReport(agent):
    w, h = letter
    date = datetime.now()
    hr_min = str(date.time()).split(':')
    time = hr_min[0]+hr_min[1]
    pdfReport = canvas.Canvas('reportes/reporte_' + agent[0] + '_' + time +'.pdf', pagesize=letter)

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
    info = consultaSNMP(agent[0], agent[1], agent[2], '1.3.6.1.2.1.1.1.0')

    sistema = []
    info_list = info.split()
    for info in info_list:
        if info == 'Linux' or info == 'Windows' or info.endswith('Ubuntu'):
            sistema.append(info)

    pdfReport.setFont('Helvetica', 10)
    pdfReport.drawString(w - 450, h - 150,f'{sistema[0]} {sistema[1]}')

    if sistema[0] == 'Linux' :
        pdfReport.drawImage("sistema-logos/ubuntu-logo.png", w-150, h - 230, width=100,height=100)
    if sistema[0] == 'Windows' :
        pdfReport.drawImage("sistema-logos/win-logo.jpeg", w - 150, h - 230, width=100, height=100)

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


    xlist = [50,500,562]
    ylist = []
    ylist_newpage = []
    y = 522
    padding = 10

    pdfReport.grid(xlist,[542,522])
    pdfReport.setFont('Helvetica-Bold', 12)
    pdfReport.drawCentredString(178, 542 - padding - 5, 'Interfaz')
    pdfReport.drawCentredString(531, 542 - padding - 5, 'Estado')
    pdfReport.setFont('Helvetica', 10)

    for i in range(1, 7, 1):
        ylist.append(y)
        y = y - 20
    for i in range(1,6,1):
        if i <= int(no_inter):
            inter_descr = consultaSNMP(agent[0], agent[1], agent[2], f'1.3.6.1.2.1.2.2.1.2.{i}')
            pdfReport.drawString(xlist[0]+padding, ylist[i] + 15 - padding, inter_descr)

            state = consultaSNMP(agent[0], agent[1], agent[2], f'1.3.6.1.2.1.2.2.1.7.{i}')
            if state == '1':
                state = 'Up'
            elif state == '2':
                state = 'Up'
            else:
                state = 'Testing'
            pdfReport.drawString(xlist[1] + padding, ylist[i] + 15 - padding, state)

    pdfReport.grid(xlist,ylist)

    pdfReport.setFont('Helvetica-Bold', 8)
    pdfReport.drawRightString(530,ylist.pop()-20,f'Fecha y hora del reporte:{date.strftime("%d %B, %Y %H:%M:%S")}')

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
        resultado = str(varBinds[0][1])
        return resultado

def close():
    print('Saliendo')


if __name__ == '__main__':
    print('\n\t\tSISTEMA DE ADMINISTRACIÓN DE RED')
    print('PRACTICA NO. 1: ADQUISICIÓN DE INFORMACIÓN USANDO SNMP')
    print('Martinez Cervantes Xenia Guadalupe \t 4CM13\t 2020630284\n')
    menu_principal()
