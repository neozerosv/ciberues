#!/usr/bin/env python
############################################
#  Servidor de CiberUES                    #
############################################


# ------------------------------
# importacion
# ------------------------------

import socket, os, sys, time, ConfigParser
from thread import *


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
	configuracion = "./agente-servidor.cfg"
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


#Function for handling connections. This will be used to create threads
def clientthread(canal,detalles):
	#Sending message to connected client
	#canal.send('Welcome to the server. Type something and hit enter\n') #send only takes string
     	#infinite loop so that function do not terminate and thread do not end.
	seguir=True
        ipremota = str( detalles )
        print "IPREMOTA:"+ipremota
        ipremota = ipremota[ ipremota.find("(") + 2 : ipremota.find(",") - 1 ]
        poner_mensaje( 'AVISO' , 'Se ha recibido una conexion ' + ipremota )

	canal.send( 'Hola ' + ipremota + ' !' )
	peticion = canal.recv(1024)
	peticion= peticion.rstrip()
	print "peticion:"+peticion+": clave:"+clave+":"
	
	if(clave == peticion):
	        poner_mensaje( 'AVISO' , "El agente servidor se identifico correctamente" )
		while seguir:
	                canal.send( 'Mucho gusto! Que desea?' )
	                peticion = canal.recv(1024)
			peticion= peticion.rstrip()
	                if ( "hola" == peticion ):
	                        poner_mensaje( 'AVISO' , "Saludo al "+ipremota )
	                        canal.send( 'Saludamos al cliente!' )
	                        #seguir = False
	                elif ( "estado" == peticion ):
	                        poner_mensaje( 'AVISO' , "El agente "+ipremota+" solicito corroborar el estado, y le dije que estaba vivo..." )
	                        canal.send( 'Estoy vivo ' + direccion + ' !' )
			elif ( "salir" == peticion ):
				poner_mensaje( 'AVISO' , "El agente "+ipremota+" solicito salir" )
				canal.send( '... Adios !' )
				seguir=False
			elif ( "ejecutar" == peticion ):
                                poner_mensaje( 'AVISO' , "El agente "+ipremota+" solicito ejecutar" )
                                canal.send( 'ifconfig' )
	                else:
	                        poner_mensaje( 'AVISO' , "El agente "+ipremota+" solicito la ejecucion de: " + peticion )
	                        ejecutar_comando( peticion )
	                        canal.send( 'Comando: <' + peticion + '> ejecutado!' )
	else:
	        poner_mensaje( 'ERROR' , "El agente servidor no se identifico correctamente" )
	        canal.send( 'No se quien es usted...ADIOS' )
	        poner_mensaje( 'ERROR' , "Puede ser un intento de ataque o una mala configuracion en el servidor" )
        #canal.send( '... Adios !' )
	#came out of loop
	canal.close()
# ------------------------------
# iniciacion del agente servidor
# ------------------------------
if __name__ == "__main__":
	activar_configuracion()
	agente = socket.socket( socket.AF_INET, socket.SOCK_STREAM )
	print "D:"+str(direccion)+" P:"+str(puerto)
	try:
		agente.bind( ( direccion, puerto ) )
		agente.listen( 1 )
		seguir = True
	except socket.error , msg:
		poner_mensaje( 'ERROR' , "No se pudo iniciar el agente cliente codigo:"+str(msg[0])+" mensaje:"+ msg[1] )
		seguir = False
	# ------------------------------
	# Bucle infinito para atender clientes
	# ------------------------------
	while seguir:
		canal, detalles = agente.accept( )
		start_new_thread(clientthread,(canal,detalles))

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
