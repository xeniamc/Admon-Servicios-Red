import time
import rrdtool
from trend.SNMP import *
rrdpath = 'RRD/'

def trendUpdate(host, community, port):

    carga_CPU = 0
    carga_RAM = 0
    inoctects = 0
    outoctects = 0

    while 1:
        carga_CPU = consultaSNMP(host, community, port,'1.3.6.1.2.1.25.3.3.1.2.7')
        total_gb_RAM = int(consultaSNMP(host, community, port,'1.3.6.1.2.1.25.2.2.0')) / 1000000
        GB_RAM = walkSum(host, community, port,'1.3.6.1.2.1.25.5.1.1.2') / 1000000
        carga_RAM = int (GB_RAM * 100 / total_gb_RAM)
        inoctects = consultaSNMP(host, community, port,'1.3.6.1.2.1.2.2.1.10.42')
        outoctects = consultaSNMP(host, community, port, '1.3.6.1.2.1.2.2.1.16.42')

        valor = "N:" + str(carga_CPU) + ':' + str(carga_RAM) + ':' + str(inoctects) + ':' + str(outoctects)
        rrdtool.update(f'{rrdpath}trend-{host}.rrd', valor)
        rrdtool.dump(f'{rrdpath}trend-{host}.rrd',f'{rrdpath}trend-{host}.xml')
        time.sleep(5)
    if ret:
        print(rrdtool.error())
        time.sleep(300)
