import sys
import rrdtool
from trend.notify import send_alert_attached
import time

rrdpath = 'RRD/'
imgpath = 'img/'

def crearGrafica(hostname, datasource, U_READY, U_SET, U_GO, titulo, y_label, color_hex):
    ultima_lectura = int(rrdtool.last(rrdpath+f"trend-{hostname}.rrd")) #Fecha del ultimo punto que se guardo menos cierto tiempo
    tiempo_final = ultima_lectura
    tiempo_inicial = tiempo_final - 1800

    ret = rrdtool.graphv(f"{imgpath}deteccion-{datasource}.png",
                         "--start",str(tiempo_inicial),
                         "--end",str(tiempo_final),
                         f"--vertical-label={y_label}",
                        '--lower-limit', '0',
                        '--upper-limit', '100',
                        f"--title={titulo}\n Detección de umbrales",
                        f"DEF:{datasource}={rrdpath}trend-{hostname}.rrd:{datasource}:AVERAGE",
                         f"VDEF:cargaMAX={datasource},MAXIMUM",
                         f"VDEF:cargaMIN={datasource},MINIMUM",
                         f"VDEF:cargaSTDEV={datasource},STDEV",
                         f"VDEF:cargaLAST={datasource},LAST",
                     #   "CDEF:cargaEscalada=cargaCPU,8,*",
                         f"CDEF:umbral{U_READY}={datasource},{U_READY},LT,0,{datasource},IF",
                         f"CDEF:umbral{U_SET}={datasource},{U_SET},LT,0,{datasource},IF",
                         f"CDEF:umbral{U_GO}={datasource},{U_GO},LT,0,{datasource},IF",
                         f"AREA:{datasource}{color_hex}:{titulo}",
                         f"AREA:umbral{U_READY}#54FF2E:{titulo} mayor que {U_READY}",
                         f"AREA:umbral{U_SET}#EED839:{titulo} mayor que {U_SET}",
                         f"AREA:umbral{U_GO}#FF2E2E:{titulo} mayor que {U_GO}",
                         f"HRULE:{U_READY}#48D000:Umbral {U_READY}%",
                         f"HRULE:{U_SET}#EED207:Umbral {U_SET}%",
                         f"HRULE:{U_GO}#FF0000:Umbral {U_GO}%",
                         "PRINT:cargaLAST:%6.2lf",
                         "GPRINT:cargaMIN:%6.2lf %SMIN",
                         "GPRINT:cargaSTDEV:%6.2lf %SSTDEV",
                         "GPRINT:cargaLAST:%6.2lf %SLAST" )
    #print(ret)

    ultimo_valor = float(ret['print[0]'])
    if ultimo_valor>U_READY and ultimo_valor<U_SET:
        send_alert_attached(f"Sobrepasa el umbral READY línea base de {titulo}",hostname,datasource)
        print(f"Sobrepasa el umbral READY línea base {titulo}")
    if ultimo_valor>U_SET and ultimo_valor<U_GO:
        send_alert_attached(f"Sobrepasa el umbral SET línea base de {titulo}", hostname, datasource)
        print(f"Sobrepasa el umbral SET línea base {titulo}")
    if ultimo_valor>U_GO:
        send_alert_attached(f"Sobrepasa el umbral GO línea base de {titulo}", hostname, datasource)
        print(f"Sobrepasa el umbral GO línea base {titulo}")