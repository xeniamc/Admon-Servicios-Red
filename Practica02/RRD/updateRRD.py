import time
import rrdtool
from RRD.SNMP import consultaSNMP

def updateRRD(host, community, port):

    ifInUcastPkts = 0
    ipInReceives = 0
    icmpOutEchos = 0
    tcpInSegs = 0
    udpInDatagrams = 0

    while 1:
        ifInUcastPkts = consultaSNMP(host, community, port,'1.3.6.1.2.1.2.2.1.11.32')
        ipInReceives = consultaSNMP(host, community, port,'1.3.6.1.2.1.4.3.0')
        icmpOutEchos = consultaSNMP(host, community, port,'1.3.6.1.2.1.5.21.0')
        tcpInSegs = consultaSNMP(host, community, port,'1.3.6.1.2.1.6.10.0')
        udpInDatagrams = consultaSNMP(host, community, port,'1.3.6.1.2.1.7.1.0')
        #print(ifInUcastPkts)

        valor = "N:" + str(ifInUcastPkts) + ':' + str(ipInReceives) + ':' + str(icmpOutEchos) + ':' + str(tcpInSegs) + ':' + str(udpInDatagrams)
        #print (valor)
        rrdtool.update(f'RRD/{host}.rrd', valor)
        rrdtool.dump(f'RRD/{host}.rrd',f'RRD/{host}.xml')

        time.sleep(1)

    if ret:
        print (rrdtool.error())
        time.sleep(300)


