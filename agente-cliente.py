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
	os.system( comando + ' 2> /dev/null > /dev/null &' )

def activar_configuracion():
	# ------------------------------
	# Variables del servicio desde
	# un archivo de configuracion
	# ------------------------------
	configuracion = "agente-cliente.cfg"
	global direccion
	global puerto
	global clave
	try:
		cfg = ConfigParser.ConfigParser()
		cfg.read([configuracion])
		direccion = cfg.get('cliente','ipcliente')
		puerto = int(cfg.get('cliente','puerto'))
		clave = cfg.get('cliente','clave')
	except:
		poner_mensaje( 'ERROR' , "No se pudo leer el archivo de configuracion " + configuracion )
		poner_mensaje( 'AVISO' , "Se tomaran los valores por omision: 127.0.0.1 6470 root" )
		direccion = '127.0.0.1'
		puerto = 6470
		clave = 'root'


# ------------------------------
# iniciacion del agente cliente
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
				poner_mensaje( 'AVISO' , "El agente servidor se identifico correctamente" )
				canal.send( 'Mucho gusto! Que desea?' )
				peticion = canal.recv(1000)
				if ( "hola" == peticion ):
					poner_mensaje( 'AVISO' , "El agente servidor solicito terminar el agente" )
					canal.send( 'Agente servidor terminando... Nos vemos!' )
					seguir = False
				else:
					poner_mensaje( 'AVISO' , "El agente servidor solicito la ejecucion de: " + peticion ) 
					ejecutar_comando( peticion )
					canal.send( 'Comando: <' + peticion + '> ejecutado!' )
			else:
				poner_mensaje( 'ERROR' , "El agente servidor no se identifico correctamente" )
				canal.send( 'No se quien es usted...' )
				poner_mensaje( 'ERROR' , "Puede ser un intento de ataque o una mala configuracion en el servidor" )
				canal.send( '... Adios !' )
			canal.close( )
	except:
			poner_mensaje( 'ERROR' , "No se pudo iniciar el agente cliente" )			