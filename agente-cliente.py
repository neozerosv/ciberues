#!/usr/bin/env python

# ------------------------------
# importacion
# ------------------------------
import socket, sys, time, ConfigParser

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
	print "     agente-cliente.py <direccion> <clave> <comando> <puerto>"
	print "--------------------------------------------------------------"
