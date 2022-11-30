from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from datetime import datetime
from trend.SNMP import *
from trend.trendGraphDetection import *

def createPDFReport(agent):

    w, h = letter
    date = datetime.now()
    hr_min = str(date.time()).split(':')
    time = hr_min[0]+hr_min[1]
    pdfReport = canvas.Canvas('reportes/reporte_' + agent[0] + '_' + time +'.pdf', pagesize=letter)

    pdfReport.setFont('Times-Bold', 18)
    pdfReport.drawCentredString(w / 2, h - 50, 'ADMINISTRACIÓN DE SISTEMAS EN RED')
    pdfReport.setFont('Times-BoldItalic', 16)
    pdfReport.drawCentredString(w / 2, h - 70, 'Practica No. 3: Monitorizar el rendimiento de un agente usando SNMP')
    pdfReport.setFont('Times-Roman', 12)
    pdfReport.drawCentredString(w / 2, h - 90, 'Alumna: Martínez Cervantes Xenia Guadalupe              Grupo: 4CM13')

    pdfReport.setStrokeColorRGB(0.58, 0.64, 0.64)
    pdfReport.line(50, h - 100, w - 50, h - 100)

    pdfReport.setFont('Helvetica', 10)
    info = consultaSNMP(agent[0], agent[1], agent[2], '1.3.6.1.2.1.1.5.0')
    pdfReport.drawString(w - 562, h - 130, f'Nombre del dispositivo: {info}')

    info = consultaSNMP(agent[0], agent[1], agent[2], '1.3.6.1.2.1.1.1.0')
    info_list = info.split()
    i = info_list.index("Windows")
    if i < 0:
        i = info.index("Ubuntu")
    system = info_list[i:]
    sys = ''
    for s in system:
        sys = f'{sys} {s}'
    pdfReport.drawString(w - 562, h - 145, f'Versión del software: {sys}')

    info = consultaSNMP(agent[0], agent[1], agent[2], '1.3.6.1.2.1.25.1.1.0')
    pdfReport.drawString(w - 562, h - 160, f'Tiempo de actividad del sistema: {info}')

    info = consultaSNMP(agent[0], agent[1], agent[2], '1.3.6.1.2.1.25.1.2.0')
    pdfReport.drawString(w - 562, h - 175, f'Fecha y hora del host: {date.strftime("%d %b %Y %H:%M:%S")}')

    pdfReport.drawString(w - 562, h - 190, f'Comunidad SNMP: {agent[1]}')

    crearGrafica(agent[0], 'cargaCPU', 25, 60, 80, 'Carga de CPU', 'Carga de CPU', '#00EDFF')
    crearGrafica(agent[0], 'cargaRAM', 50, 70, 80, 'Carga de RAM', 'Carga de RAM', '#00EDFF')
    crearGrafica(agent[0], 'inoctects', 1000, 3000, 4500, 'Trafico de entrada de red', 'Octetos de entrada', '#00EDFF')
    crearGrafica(agent[0], 'outoctects', 1000, 3000, 4500, 'Trafico de salida de red', 'Octetos de salida', '#00EDFF')

    pdfReport.drawImage("img/deteccion-cargaCPU.png", w - 562, h - 460)
    pdfReport.drawImage("img/deteccion-cargaRAM.png", w - 562, h - 710)
    pdfReport.showPage()
    pdfReport.drawImage("img/deteccion-inoctects.png", w - 562, h - 250)
    pdfReport.drawImage("img/deteccion-outoctects.png", w - 562, h - 500)
    #######################################################################################
    '''
    pdfReport.drawString(w - 562, h - 220, f'NO VA: {date.strftime("%d %b %Y %H:%M:%S")}')

    pdfReport.drawString(w - 562, h - 235, '#NAS-IP-Address')
    pdfReport.drawString(w - 562, h - 250, f'{agent[0]}')

    pdfReport.drawString(w - 562, h - 265, '#User-name')
    info = consultaSNMP(agent[0], agent[1], agent[2], '1.3.6.1.2.1.1.5.0')
    pdfReport.drawString(w - 562, h - 280, f'{info}')

    pdfReport.drawString(w - 562, h - 295, '#Acct-Input-Octets')
    inoctets = consultaSNMP(agent[0], agent[1], agent[2], '1.3.6.1.2.1.2.2.1.10.41')
    pdfReport.drawString(w - 562, h - 310, f'{inoctets}')

    pdfReport.drawString(w - 562, h - 325, '#Acct-Output-Octets')
    outoctets = consultaSNMP(agent[0], agent[1], agent[2], '1.3.6.1.2.1.2.2.1.16.41')
    pdfReport.drawString(w - 562, h - 340, f'{outoctets}')

    pdfReport.drawString(w - 562, h - 355, '#Acct-Session-Id')
    pdfReport.drawString(w - 562, h - 370, f'{session_id}')

    pdfReport.drawString(w - 562, h - 385, '#Acct-Session-Time')
    info = consultaSNMP(agent[0], agent[1], agent[2], '1.3.6.1.2.1.1.3.0')
    pdfReport.drawString(w - 562, h - 400, f'{info}')

    pdfReport.drawString(w - 562, h - 415, '#Acct-Input-Packets')
    inpkts = consultaSNMP(agent[0], agent[1], agent[2], '1.3.6.1.2.1.2.2.1.12.41')
    pdfReport.drawString(w - 562, h - 430, f'{inpkts}')

    pdfReport.drawString(w - 562, h - 445, '#Acct-Output-Packets')
    outpkts = consultaSNMP(agent[0], agent[1], agent[2], '1.3.6.1.2.1.2.2.1.17.41')
    pdfReport.drawString(w - 562, h - 460, f'{outpkts}')

    pdfReport.showPage()
    pdfReport.drawImage("img/deteccion-cargaCPU.png", w - 562, h - 230)
    pdfReport.drawImage("img/deteccion-cargaRAM.png", w - 562, h - 480)
    pdfReport.drawImage("img/deteccion-inoctects.png", w - 562, h - 730)
    pdfReport.showPage()
    pdfReport.drawImage("img/deteccion-outoctects.png", w - 562, h - 230)
    
    pdfReport.showPage()
    pdfReport.drawImage("RRD/graficas/tcpInSegs.png", w - 562, h - 230)
    pdfReport.drawImage("RRD/graficas/udpInDatagrams.png", w - 562, h - 480)
    '''
    pdfReport.save()
    print('El reporte se ha generado existosamente!')