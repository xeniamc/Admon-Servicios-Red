import sys
import rrdtool
import time

def crearGrafica(rrd_name, datasource, titulo, y_label, color_hex):

	tiempo_actual = int(time.time())

	tiempo_inicial = tiempo_actual - 1200

	ret = rrdtool.graphv( f'RRD/graficas/{datasource}.png',
		             "--start",str(tiempo_inicial),
		             "--end","N",
		             f'--vertical-label={y_label}',
		             f'--title={titulo}',
		             f'DEF:{datasource}=RRD/{rrd_name}.rrd:{datasource}:AVERAGE',
		             f'AREA:{datasource}{color_hex}:',
		              )
	print(ret)