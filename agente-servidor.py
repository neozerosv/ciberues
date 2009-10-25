#!/usr/bin/env python

# ------------------------------
# importacion
# ------------------------------
import socket, sys, time, ConfigParser

def activar_configuracion():
	# ------------------------------
	# Variables del cliente desde
	# un archivo de configuracion
	# ------------------------------
	configuracion = "agente-servidor.cfg"
	global direccion
	global puerto
	global clave
	try:
		cfg = ConfigParser.ConfigParser()
		cfg.read([configuracion])
		direccion = cfg.get('servidor','ipservidor')
		puerto = int(cfg.get('servidor','puerto'))
		clave = cfg.get('servidor','clave')
	except:
		poner_mensaje( 'ERROR' , "No se pudo leer el archivo de configuracion " + configuracion )
		poner_mensaje( 'AVISO' , "Se tomaran los valores por omision: 127.0.0.1 6470 root" )
		direccion = '127.0.0.1'
		puerto = 6470
		clave = 'root'



# ------------------------------
# parametros a utilizar
# ------------------------------
if( len(sys.argv) == 5 ):
	continuar = True
	direccion =  sys.argv[1]
	clave = sys.argv[2]
	comando =  sys.argv[3]
	try:
		puerto =  int(sys.argv[4])
	except:
		print "No acepto " + sys.argv[4] + " !"
		print "Probando puerto 6470"
		puerto = 6470
	agente = socket.socket( socket.AF_INET, socket.SOCK_STREAM )
	try:
		agente.connect( ( direccion, puerto ) )
	except:
		print "No se pudo establecer la conexion en la direccion: "+ direccion +" con el puerto: " + str(puerto)
		continuar = False
	if ( continuar == True ):
		data, server = agente.recvfrom( 100 )
		print data
		agente.send( clave )
		data, server = agente.recvfrom( 100 )
		print data
		agente.send( comando )
		agente.close()
else:
	print "--------------------------------------------------------------"
	print " Tiene que mandar cuatro parametros"
	print "     agente-servidor.py <direccion> <clave> <comando> <puerto>"
	print "--------------------------------------------------------------"

if __name__ == "__main__":
	activar_configuracion()