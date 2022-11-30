import rrdtool

def crearRRD(hostname):
    ret = rrdtool.create(f"RRD/trend-{hostname}.rrd",
                         "--start",'N',
                         "--step",'60',
                         "DS:cargaCPU:GAUGE:60:0:100", #limites para tomar la muestra como valida
                         "DS:cargaRAM:GAUGE:60:0:100",
                         "DS:inoctects:COUNTER:120:U:U",
                         "DS:outoctects:COUNTER:120:U:U",
                         "RRA:AVERAGE:0.5:1:24")
    if ret:
        print (rrdtool.error())
