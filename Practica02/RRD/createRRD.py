#!/usr/bin/env python
import rrdtool

def crearRRD(hostname):

    ret = rrdtool.create(f'RRD/agente.rrd',
                         "--start",'N',
                         "--step",'60',
                         "DS:ifInUcastPkts:COUNTER:120:U:U",
                         "DS:ipInReceives:COUNTER:120:U:U",
                         "DS:icmpOutEchos:COUNTER:120:U:U",
                         "DS:tcpInSegs:COUNTER:120:U:U",
                         "DS:udpInDatagrams:COUNTER:120:U:U",
                         "RRA:AVERAGE:0.5:6:5",
                         "RRA:AVERAGE:0.5:1:600")

    if ret:
        print (rrdtool.error())