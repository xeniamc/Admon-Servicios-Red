from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from datetime import datetime
from RRD.SNMP import *
from RRD.graphRRD import *

def createPDFReport(agent, session_id):

    w, h = letter
    date = datetime.now()
    hr_min = str(date.time()).split(':')
    time = hr_min[0]+hr_min[1]
    pdfReport = canvas.Canvas('reportes/reporte_' + agent[0] + '_' + time +'.pdf', pagesize=letter)

    pdfReport.setFont('Times-Bold', 18)
    pdfReport.drawCentredString(w / 2, h - 50, 'ADMINISTRACIÓN DE SISTEMAS EN RED')
    pdfReport.setFont('Times-BoldItalic', 16)
    pdfReport.drawCentredString(w / 2, h - 70, 'Practica No. 2: Sistema de administración de Contabilidad')
    pdfReport.setFont('Times-Roman', 12)
    pdfReport.drawCentredString(w / 2, h - 90, 'Alumna: Martínez Cervantes Xenia Guadalupe              Grupo: 4CM13')

    pdfReport.setStrokeColorRGB(0.58, 0.64, 0.64)
    pdfReport.line(50, h - 100, w - 50, h - 100)

    pdfReport.setFont('Helvetica', 10)
    pdfReport.drawString(w - 562, h - 130, f'version: 1')

    info = consultaSNMP(agent[0], agent[1], agent[2], '1.3.6.1.2.1.1.5.0')
    pdfReport.drawString(w - 562, h - 145, f'device: {info}')

    pdfReport.drawString(w - 562, h - 160, f'description: Accounting {info}')

    pdfReport.drawString(w - 562, h - 175, f'date: {date.strftime("%d %b %Y %H:%M:%S")}')

    pdfReport.drawString(w - 562, h - 190, f'defaultProtocol: radius')

    pdfReport.drawString(w - 562, h - 220, f'rdate: {date.strftime("%d %b %Y %H:%M:%S")}')

    pdfReport.drawString(w - 562, h - 235, '#NAS-IP-Address')
    pdfReport.drawString(w - 562, h - 250, '{info}')

    pdfReport.drawString(w - 562, h - 265, '#NAS-Port')
    pdfReport.drawString(w - 562, h - 280, '{info}')

    pdfReport.drawString(w - 562, h - 295, '#NAS-Port-Type')
    pdfReport.drawString(w - 562, h - 310, '{info}')

    pdfReport.drawString(w - 562, h - 325, '#User-name')
    info = consultaSNMP(agent[0], agent[1], agent[2], '1.3.6.1.2.1.1.5.0')
    pdfReport.drawString(w - 562, h - 340, f'{info}')

    pdfReport.drawString(w - 562, h - 355, '#Acct-Status-Type')
    pdfReport.drawString(w - 562, h - 370, '{info}')

    pdfReport.drawString(w - 562, h - 385, '#Acct-Delay-Time')
    pdfReport.drawString(w - 562, h - 400, '{info}')

    pdfReport.drawString(w - 562, h - 415, '#Acct-Input-Octets')
    inoctets = consultaSNMP(agent[0], agent[1], agent[2], '1.3.6.1.2.1.2.2.1.10.1')
    pdfReport.drawString(w - 562, h - 430, f'{inoctets}')

    pdfReport.drawString(w - 562, h - 445, '#Acct-Output-Octets')
    outoctets = consultaSNMP(agent[0], agent[1], agent[2], '1.3.6.1.2.1.2.2.1.16.1')
    pdfReport.drawString(w - 562, h - 460, f'{outoctets}')

    pdfReport.drawString(w - 562, h - 475, '#Acct-Session-Id')
    pdfReport.drawString(w - 562, h - 490, f'{session_id}')

    pdfReport.drawString(w - 562, h - 505, '#Acct-Authentic')
    pdfReport.drawString(w - 562, h - 520, '{info}')

    pdfReport.drawString(w - 562, h - 535, '#Acct-Session-Time')
    pdfReport.drawString(w - 562, h - 550, '{info}')

    pdfReport.drawString(w - 562, h - 565, '#Acct-Input-Packets')
    inpkts = consultaSNMP(agent[0], agent[1], agent[2], '1.3.6.1.2.1.2.2.1.12.1')
    pdfReport.drawString(w - 562, h - 580, f'{inpkts}')

    pdfReport.drawString(w - 562, h - 595, '#Acct-Output-Packets')
    outpkts = consultaSNMP(agent[0], agent[1], agent[2], '1.3.6.1.2.1.2.2.1.17.1')
    pdfReport.drawString(w - 562, h - 610, f'{outpkts}')

    pdfReport.drawString(w - 562, h - 625, '#Acct-Terminate-Cause')
    pdfReport.drawString(w - 562, h - 640, '{info}')

    pdfReport.drawString(w - 562, h - 655, '#Acct-Multi-Session-Id')
    pdfReport.drawString(w - 562, h - 670, '{info}')

    pdfReport.drawString(w - 562, h - 685, '#Acct-Link-Count')
    pdfReport.drawString(w - 562, h - 700, '{info}')

    crearGrafica('agente','ifInUcastPkts', 'Paquetes unicast que ha recibido \nuna interfaz de red de un agente',
                 'Paquetes unicast', '#00EDFF')
    crearGrafica('agente','ipInReceives', 'Paquetes recibidos a protocolos IP,\n incluyendo los que tienen errores.', 'Paquetes',
                 '#FFDC00')
    crearGrafica('agente','icmpOutEchos', 'Mensajes ICMP echo que ha\n enviado el agente', 'Mesajes ICMP', '#FF5500')
    crearGrafica('agente','tcpInSegs', 'Segmentos recibidos, incluyendo los\n que se han recibido con errores', 'Segmentos',
                 '#A6FF00')
    crearGrafica('agente','udpInDatagrams', 'Datagramas entregados a usuarios UDP', 'Datagramas', '#FFA4F8')

    pdfReport.showPage()
    pdfReport.drawImage("RRD/graficas/ifInUcastPkts.png", w - 562, h - 230)
    pdfReport.drawImage("RRD/graficas/ipInReceives.png", w - 562, h - 480)
    pdfReport.drawImage("RRD/graficas/icmpOutEchos.png", w - 562, h - 730)
    pdfReport.showPage()
    pdfReport.drawImage("RRD/graficas/tcpInSegs.png", w - 562, h - 230)
    pdfReport.drawImage("RRD/graficas/udpInDatagrams.png", w - 562, h - 480)

    pdfReport.save()
    print('El reporte se ha generado existosamente!')