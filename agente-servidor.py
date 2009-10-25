#!/usr/bin/env python
# ------------------------------
# importacion
# ------------------------------
import socket, os, time, ConfigParser


def poner_mensaje( tipo , mensaje ):
	# -----------------------------
	# Colocar mensajes con formato
	# y marca de tiempo
	# -----------------------------
	print time.strftime('%Y-%m-%d-%X') + " " + tipo + ": " + mensaje

def ejecutar_comando( comando ):
	# -----------------------------
	# Ejecutar el comando en el
	# sistema operativo
	# -----------------------------
	os.system( comando + ' > /dev/null &' )

def activar_configuracion():
	# ------------------------------
	# Variables del servicio desde
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
# iniciacion del agente servidor
# ------------------------------
if __name__ == "__main__":
	activar_configuracion()
	agente = socket.socket( socket.AF_INET, socket.SOCK_STREAM )
	try:
		agente.bind( ( direccion, puerto ) )
		agente.listen( 1 )
		seguir = True
		# ------------------------------
		# Bucle infinito para atender clientes
		# ------------------------------
		while seguir:
			canal, detalles = agente.accept( )
			poner_mensaje( 'AVISO' , 'Se ha recibido una conexion ' + str( detalles ) )
			canal.send( 'Hola ' + str( detalles ) + ' !' )
			peticion = canal.recv(1000)
			if ( clave == peticion):
				poner_mensaje( 'AVISO' , "El cliente se identifico correctamente" )
				canal.send( 'Mucho gusto! Que desea?' )
				peticion = canal.recv(1000)
				if ( "hola" == peticion ):
					poner_mensaje( 'AVISO' , "El cliente solicito terminar el agente" )
					seguir = False
				else:
					poner_mensaje( 'AVISO' , "El cliente solicito la ejecucion de: " + peticion ) 
					ejecutar_comando( peticion )
			else:
				poner_mensaje( 'ERROR' , "El cliente no se identifico correctamente" )
				canal.send( 'Adios !' )
			canal.close( )
	except:
			poner_mensaje( 'ERROR' , "No se pudo iniciar el agente" )
