#!/usr/bin/env python
############################################
#  Cliente de CiberUES                     #
############################################


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
	configuracion = "./agente-cliente.cfg"
	global direccion
	global puerto
	global clave
	try:
		cfg = ConfigParser.ConfigParser()
		cfg.read([configuracion])
		puerto = int(cfg.get('cliente','puerto'))
		clave = cfg.get('cliente','clave')
		clientes = cfg.get('cliente','servidor')
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
		#Crear 
		try:
			agente = socket.socket( socket.AF_INET, socket.SOCK_STREAM )
		except socket.error, msg:
			poner_mensaje ( 'ERROR' ,'Fallo crear socket. codigo: ' + str(msg[0]) + ' , mensaje: ' + msg[1])
			continuar = False
		#Conectarse
		try:
			agente.connect( ( direccion, puerto ) )
		except:
			poner_mensaje ( 'ERROR' , "No se pudo establecer la conexion en la direccion: "+ direccion +" con el puerto: " + str(puerto) )
			continuar = False
		#Hacer todo lo demas
		poner_mensaje ( 'AVISO' ,"Conectado al"+direccion+" ")
		if ( continuar == True ):
			#Obtiene mensaje, envia clave
			data, server = agente.recvfrom( 100 )
			poner_mensaje ( 'MENSAJE' , data )
			agente.send( clave )
			#Obtiene Mensaje, envia comando
			data, server = agente.recvfrom( 100 )
			poner_mensaje ( 'MENSAJE' , data )
			agente.send( comando )
			#Obtiene mensaje
			data, server = agente.recvfrom( 100 )
			poner_mensaje ( 'MENSAJE' , data )
			#Obtiene mensaje, se salr
			data, server = agente.recvfrom( 100 )
			poner_mensaje ( 'MENSAJE' , data) 
			agente.send( "salir" )

			agente.close()
	else:
		print "--------------------------------------------------------------"
		print " Tiene que mandar cuatro parametros"
		print "     agente-servidor.py <direccion> <comando>"
		print "--------------------------------------------------------------"

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
