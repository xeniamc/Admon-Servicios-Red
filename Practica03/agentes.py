from report import *
from trend.trendCreate import *
from trend.trendUpdate import *
from threading import *
import multiprocessing

agents = {}
file = open("agentes.txt", "w+")
t = Thread(name="trendUpdate", target=trendUpdate)

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
    ip_hostname = '192.168.1.176'
    port = 161
    community = 'XENIA'
    version = 'v1'
    '''
    agents[index] = [ip_hostname, community, port, version]
    file.write(ip_hostname + ',' + community + ',' + str(port) + ',' + version +',\n')

    file.close()

    #crearRRD(ip_hostname)
    #print('SE CREO LA RRD')

    t = Thread(name="trendUpdate", target=trendUpdate, args=(ip_hostname, community, port))
    t.start()
    print('EL SONDEO COMENZO')

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
            file = open("agentes.txt", "w+")
            print(f'Se ha eliminado el agente {del_agent}: {agents.pop(del_agent)}')
            for valor in agents.values():
                file.write(valor[0]+','+valor[1]+','+valor[2]+','+valor[3]+',\n')
            file.close()
        else:
            print(f'Se cancelo la eliminacion del agente {del_agent}: {agents[del_agent][0]}')


def getReport():

    if getAgents() == -1:
        print('AUN NO SE TIENEN AGENTES REGISTRADOS. PRIMERO INTENTE AGREGAR UN AGENTE')
    else:
        print('\tAGENTES EN LA LISTA:')
        for clave in agents:
            print(f'AGENTE {clave}:  {agents[clave][0]}, {agents[clave][1]}, {agents[clave][2]}, {agents[clave][3]}')

        while (agent_report := int(input('No. del agente del que desea generar el reporte:'))) not in agents:
            print(f'El agente {agent_report} no existe. Intentelo otra vez.')

        createPDFReport(agents[agent_report])
