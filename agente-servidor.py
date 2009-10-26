#!/usr/bin/env python

# ------------------------------
# importacion
# ------------------------------
import socket, sys, time, ConfigParser

def poner_mensaje( tipo , mensaje ):
	# -----------------------------
	# Colocar mensajes con formato
	# y marca de tiempo
	# -----------------------------
	print time.strftime('%Y-%m-%d-%X') + " " + tipo + ": " + mensaje

def activar_configuracion():
	# ------------------------------
	# Variables del servidor desde
	# un archivo de configuracion
	# ------------------------------
	configuracion = "agente-servidor.cfg"
	global direccion
	global puerto
	global clave
	try:
		cfg = ConfigParser.ConfigParser()
		cfg.read([configuracion])
		puerto = int(cfg.get('servidor','puerto'))
		clave = cfg.get('servidor','clave')
	except:
		poner_mensaje( 'ERROR' , "No se pudo leer el archivo de configuracion " + configuracion )
		poner_mensaje( 'AVISO' , "Se tomaran los valores por omision: 6470 root" )
		puerto = 6470
		clave = 'root'

if __name__ == "__main__":
	activar_configuracion()
	# ------------------------------
	# parametros a utilizar
	# ------------------------------
	if( len(sys.argv) == 3 ):
		continuar = True
		direccion =  sys.argv[1]
		comando =  sys.argv[2]
		agente = socket.socket( socket.AF_INET, socket.SOCK_STREAM )
		try:
			agente.connect( ( direccion, puerto ) )
		except:
			poner_mensaje ( 'ERROR' , "No se pudo establecer la conexion en la direccion: "+ direccion +" con el puerto: " + str(puerto) )
			continuar = False
		if ( continuar == True ):
			data, server = agente.recvfrom( 100 )
			poner_mensaje ( 'MENSAJE' , data )
			agente.send( clave )
			data, server = agente.recvfrom( 100 )
			poner_mensaje ( 'MENSAJE' , data )
			agente.send( comando )
			data, server = agente.recvfrom( 100 )
			poner_mensaje ( 'MENSAJE' , data )
			agente.close()
	else:
		print "--------------------------------------------------------------"
		print " Tiene que mandar cuatro parametros"
		print "     agente-servidor.py <direccion> <comando>"
		print "--------------------------------------------------------------"