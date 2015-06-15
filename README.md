ciberues
========
Sistema de contro de sesiones para CiberUES en El Salvador


Uso
========
En los equipos clientes se debe ejecutar como servicio el programa:
./agente-cliente.py &

En el equipo servidor se utiliza el programa cliente seguido de algun comando:
./agente-servidor 127.0.0.1 ls

Para que ambos puedan comunicarse correctamente deberá configurarse el archivo agente-cliente.cfg en los equipos clientes y el archivo agente-servidor.cfg en el equipo servidor, en ambos archivos se indica el puerto en el que se abrirá la comunicación, la clave con la que interactaurán y la lista de IP de equipos que serán clientes o servidores

Aviso
========
Este programa carece de encriptación en la comunicación, es actualmente una simple herramienta para poder tener control sobre el equipo remoto a travez de simples instrucciones a ejecutar en la shell.
