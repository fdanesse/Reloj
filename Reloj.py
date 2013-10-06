#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import math
import cairo
import re
from datetime import datetime

from gi.repository import GObject
from gi.repository import Gtk
from gi.repository import Gdk
from gi.repository import Pango
from gi.repository import PangoCairo

from Widgets import Imagen_Reloj
from Widgets import Toolbar

from JAMediaSpeak import JAMediaSpeak

class Reloj(Gtk.Window):
    
    __gtype_name__ = 'Reloj'
    
    def __init__(self):

        Gtk.Window.__init__(self)

        self.set_size_request(640, 480)
        self.set_title('Reloj')
        
        self.speaker_active = False
        self.speaker = JAMediaSpeak()
        self.minutos = 0
        
        self.toolbar = Toolbar()
        self.reloj = Imagen_Reloj()
        self.hora = Gtk.Label("Time")
        self.fecha = Gtk.Label("Date")
        
        vbox = Gtk.VBox()
        vbox.pack_start(self.toolbar, False, False, 0)
        vbox.pack_start(self.reloj, True, True, 0)
        vbox.pack_start(self.hora, False, False, 0)
        vbox.pack_start(self.fecha, False, False, 0)

        self.add(vbox)
        self.show_all()
        
        self.reloj.connect("update", self.__update)
        self.toolbar.connect("accion", self.__set_accion)
        self.toolbar.connect("speak", self.__set_speak)
        self.connect("delete-event", self.__exit)
        
    def __set_speak(self, widget, valor):
        
        self.speaker_active = valor
    
    def __set_accion(self, widget, accion, valor):
        
        if valor:
            if accion == "Reloj Sencillo":
                self.reloj.tipo = accion
            
            elif accion == "Reloj Digital":
                self.reloj.tipo = accion
    
    def __update(self, widget, date, time):
        
        self.fecha.set_text(date)
        self.hora.set_text(time)
        
        minutos = int(time.split(":")[1])
        
        if self.speaker_active:
            if minutos != self.minutos:
                self.minutos = minutos
                horas = int(time.split(":")[0])
                self.speaker.speak("Son las %s Horas con %s Minutos" % (horas, minutos))
    
    def __exit(self, widget, event):
        
        import sys
        sys.exit(0)
        
if __name__ == "__main__":
    Reloj()
    Gtk.main()
    