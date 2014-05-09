

from gi.repository import Gtk, Gdk, GdkPixbuf
#from gi.repository import Gdk
#from gi.repository import GdkPixbuf
import pygtk
pygtk.require('2.0')
import sys
#import gtk

FONDO="/usr/share/backgrounds/ues/rojo-tapiz-ues.png"
pixbuf = GdkPixbuf.Pixbuf.new_from_file(FONDO)

css = """
#MyWindow {
   background-color: #F00;
   background-image:url("/usr/share/backgrounds/ues/rojo-tapiz-ues.png"); 
   background-size: 115%;
   background-repeat:no-repeat;
}
"""

#pixbuf = gtk.gdk.pixbuf_new_from_file(IMG)

class bloqueaSesion(Gtk.ApplicationWindow):
    def ingresar(self, widget, data=None):
        print "Ingresando a la sesion del usuario"

    # create a window
    def __init__(self, app):
        Gtk.Window.__init__(self, title="Bienvenido al CiberUES", application=app)
        self.set_default_size(1000, 1000)

#Propiedades para el bloqueo de la ventana:
        self.fullscreen()
#        self.set_focus() 
#        self.stick()
#        image = Gtk.Image()
#        image.set_from_file("/usr/share/backgrounds/ues/rojo-tapiz-ues.png")
#        self.add(image)
#Falta ver lo agregar botones y que no pueda ejecutar algun menu

	image = Gtk.Image()
	#  (from http://www.pygtk.org/docs/pygtk/gtk-stock-items.html)
#image.set_from_stock(Gtk.STOCK_)
	image.set_from_file(FONDO)



	#Creamos una tabla para organizar los botones, 3x3
	self.table = Gtk.Table(4, 3, True)
        self.add(self.table)


	self.space = Gtk.Label("                                ")
        self.space.show()


	
        self.label = Gtk.Label()
	self.label.set_markup('<span foreground="#FFFFFF"  size="x-large"><b>Favor esperar activacion</b></span>')
	self.label.show()
	

	
	self.button = Gtk.Button()
	self.button.set_label("Ingresar")
	#Asocia la funcion al boton
        self.button.connect("clicked", self.ingresar, None)	
	self.button.show()


	#funcion para organizar table.attach(child, left_attach, right_attach, top_attach, bottom_attach, xoptions=<flags EXPAND | FILL of type AttachOptions>, yoptions=<flags EXPAND | FILL of type AttachOptions>, xpadding=0, ypadding=0)
        self.table.attach(self.label, 1, 2, 1, 2)
        self.table.attach(self.button, 1, 2, 2, 3)





class muestraBloqueo(Gtk.Application):
    def __init__(self):
        Gtk.Application.__init__(self)

    def do_activate(self):
	style_provider = Gtk.CssProvider()
	style_provider.load_from_data(css)

	Gtk.StyleContext.add_provider_for_screen(
	    Gdk.Screen.get_default(), 
	    style_provider,     
	    Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
	)
        win = bloqueaSesion(self)
	win.set_name('MyWindow')
        win.show_all()

    def do_startup(self):
        Gtk.Application.do_startup(self)

app = muestraBloqueo()
exit_status = app.run(sys.argv)
sys.exit(exit_status)



#Referencias
#http://python-gtk-3-tutorial.readthedocs.org/en/latest
#http://pygtk.org/pygtk2tutorial-es/sec-TablePackingExample.html/
#https://developer.gnome.org/pango/stable/PangoMarkupFormat.html
#http://wolfvollprecht.de/blog/gtk-python-and-css-are-an-awesome-combo/
#kill -9 $(ps aux|grep "[p]ython pruebagui.py"|awk '{print $2}')

