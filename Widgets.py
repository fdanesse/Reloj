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
from gi.repository import Rsvg

BASE_PATH = os.path.abspath(os.path.dirname(__file__))

class Imagen_Reloj(Gtk.DrawingArea):
    
    __gtype_name__ = 'Imagen_Reloj'
    
    __gsignals__ = {
        "update":(GObject.SIGNAL_RUN_LAST,
            GObject.TYPE_NONE, (GObject.TYPE_PYOBJECT,
            GObject.TYPE_PYOBJECT))}
            
    def __init__(self):
        
        Gtk.DrawingArea.__init__(self)

        self.time = datetime.now()
        self.tipo = "Reloj Sencillo"
        self._center_x = 0
        self._center_y = 0
        self.radio = 0
        self._width = 0
        self._height = 0
        self._line_width = 2

        self.connect("draw", self.__draw)
        self.show_all()
        
        GObject.timeout_add(1000, self.__update)
        
    def __draw(self, widget, cr):

        rect = self.get_allocation()
        
        self._center_x = int(rect.width / 2.0)
        self._center_y = int(rect.height / 2.0)
        
        self.radio = max(min(
            int(rect.width / 2.0), \
            int(rect.height / 2.0)) - 20, 0)
            
        self._width = rect.width
        self._height = rect.height
        self._line_width = int(self.radio / 150)
        
        if self.tipo == "Reloj Sencillo":
            self.__dibujar_fondo(cr)
            #self._draw_numbers(cr)
            self.__dibujar_agujas(cr)
            
        elif self.tipo == "Reloj Digital":
            self._draw_time_scale(cr)
            #self._draw_time(cr)
            
        return False

    def _draw_time_scale(self, cr):
        
        hours_length = 2 * self.radio / 24 * self.time.hour
        minutes_length = 2 * self.radio / 60 * self.time.minute
        seconds_length = 2 * self.radio / 60 * self.time.second
        
        cr.set_source_rgba(255, 255, 255, 1)
        
        cr.rectangle(
            round(self._center_x - 1.1 * self.radio),
            round(self._center_y - 0.85 * self.radio),
            round(2.2 * self.radio),
            round(0.65 * self.radio))
            
        cr.fill()

        h = round(0.15 * self.radio)
        x = round(self._center_x - self.radio)

        # Hours scale
        cr.set_source_rgba(0, 0, 255, 1)
        y = round(self._center_y - 0.75 * self.radio)
        cr.rectangle(x, y, hours_length, h)
        cr.fill()

        # Minutes scale
        cr.set_source_rgba(0, 255, 0, 1)
        y = round(self._center_y - 0.60 * self.radio)
        cr.rectangle(x, y, minutes_length, h)
        cr.fill()

        # Seconds scale
        cr.set_source_rgba(255, 0, 0, 1)
        y = round(self._center_y - 0.45 * self.radio)
        cr.rectangle(x, y, seconds_length, h)
        cr.fill()
    
    def __dibujar_fondo(self, cr):
        
        cr.set_line_width(4 * self._line_width)
        cr.set_line_cap(cairo.LINE_CAP_ROUND)

        ### Fondo
        cr.set_source_rgba(255, 255, 255, 1)
        cr.arc(self._width / 2, self._height / 2,
            self.radio, 0, 2 * math.pi)
        cr.fill_preserve()
        
        cr.set_source_rgba(0, 0, 0, 1)
        cr.stroke()

        ### Lineas
        for i in xrange(60):
            if i % 15 == 0:
                inset = 0.11 * self.radio
                cr.set_line_width(7 * self._line_width)
                
            elif i % 5 == 0:
                inset = 0.1 * self.radio
                cr.set_line_width(5 * self._line_width)
                
            else:
                inset = 0.05 * self.radio
                cr.set_line_width(4 * self._line_width)

            cos = math.cos(i * math.pi / 30.0)
            sin = math.sin(i * math.pi / 30.0)
            
            cr.move_to(int(self._center_x + (self.radio - inset) * cos),
                int(self._center_y + (self.radio - inset) * sin))

            cr.line_to(int(self._center_x + (self.radio - 3) * cos),
                int(self._center_y + (self.radio - 3) * sin))
            
            cr.stroke()
    
    def __dibujar_agujas(self, cr):
        
        hours = self.time.hour
        minutes = self.time.minute
        seconds = self.time.second
        
        cr.set_line_cap(cairo.LINE_CAP_ROUND)
        
        cr.set_source_rgba(0, 0, 255, 1)
        cr.set_line_width(9 * self._line_width)
        cr.arc(self._center_x, self._center_y,
            5 * self._line_width, 0, 2 * math.pi)
            
        cr.fill_preserve()
        
        cr.move_to(self._center_x, self._center_y)
        
        cr.line_to(int(self._center_x + self.radio * 0.5 *
            math.sin(math.pi / 6 * hours + math.pi / 360 * minutes)),
            int(self._center_y + self.radio * 0.5 *
            - math.cos(math.pi / 6 * hours + math.pi / 360 * minutes)))
            
        cr.stroke()

        cr.set_source_rgba(0, 255, 0, 1)
        cr.set_line_width(6 * self._line_width)
        
        cr.arc(self._center_x, self._center_y,
            4 * self._line_width, 0, 2 * math.pi)
            
        cr.fill_preserve()
        
        cr.move_to(self._center_x, self._center_y)
        cr.line_to(int(self._center_x + self.radio * 0.7 *
                math.sin(math.pi / 30 * minutes)),
                int(self._center_y + self.radio * 0.7 *
                - math.cos(math.pi / 30 * minutes)))
                
        cr.stroke()
        
        cr.set_source_rgba(255, 0, 0, 1)
        cr.set_line_width(2 * self._line_width)
        
        cr.arc(self._center_x, self._center_y,
            3 * self._line_width, 0, 2 * math.pi)
            
        cr.fill_preserve()
        
        cr.move_to(self._center_x, self._center_y)
        
        cr.line_to(int(self._center_x + self.radio * 0.8 *
                math.sin(math.pi / 30 * seconds)),
                int(self._center_y + self.radio * 0.8 *
                - math.cos(math.pi / 30 * seconds)))
                
        cr.stroke()
        
    '''
    def _draw_numbers(self, cr):
        
        #cr = self.get_property('window').cairo_create()
        cr.set_source_rgba(0, 0, 255, 1)
        pango_layout = PangoCairo.create_layout(
            PangoCairo.create_context(cr))
        
        for i in xrange(12):
            hour_number = _('<markup><span lang="en" \
font_desc="Sans Bold 40">%d</span></markup>') % (i + 1)
            cr.save()
            pango_layout.set_markup(hour_number)
            dx, dy = pango_layout.get_pixel_size()
            cr.translate(- dx / 2.0 + self._center_x + 0.75 *
                self.radio * math.cos((i - 2) * math.pi / 6.0),
                - dy / 2.0 + self._center_y + 0.75 * self.radio *
                math.sin((i - 2) * math.pi / 6.0))
                
            PangoCairo.update_layout(cr, pango_layout)
            PangoCairo.show_layout(cr, pango_layout)
            cr.restore()'''

    def __update(self):
        
        self.time = datetime.now()
        time = "%s:%s:%s" % (self.time.hour, self.time.minute, self.time.second)
        date = "%s/%s/%s" % (self.time.day, self.time.month, self.time.year)
        self.emit("update", date, time)
        self.queue_draw()
        
        return True
    
class Toolbar(Gtk.Toolbar):
    
    __gtype_name__ = 'ToolbarClock'
    
    __gsignals__ = {
    "accion":(GObject.SIGNAL_RUN_FIRST,
        GObject.TYPE_NONE, (GObject.TYPE_STRING,
        GObject.TYPE_BOOLEAN)),
    "speak":(GObject.SIGNAL_RUN_FIRST,
        GObject.TYPE_NONE, (GObject.TYPE_BOOLEAN,))}
        
    def __init__(self):
        
        Gtk.Toolbar.__init__(self)
        
        self.grupo1 = []
        
        ### Grupo 1
        archivo = os.path.join(BASE_PATH,
            "Iconos", "simple-clock.svg")
        button = self.__get_toggle_boton(archivo, 'Reloj Sencillo')
        button.connect("toggled", self.__emit_accion)
        self.insert(button, -1)
        self.grupo1.append(button)
        
        archivo = os.path.join(BASE_PATH,
            "Iconos", "digital-clock.svg")
        button = self.__get_toggle_boton(archivo, 'Reloj Digital')
        button.connect("toggled", self.__emit_accion)
        self.insert(button, -1)
        self.grupo1.append(button)
        
        separator = Gtk.SeparatorToolItem()
        separator.set_draw(True)
        separator.set_expand(False)
        self.insert(separator, -1)
        
        archivo = os.path.join(BASE_PATH,
            "Iconos", "speak-time.svg")
        button = self.__get_toggle_boton(archivo, 'Reloj Parlante')
        button.connect("toggled", self.__emit_espeak)
        button.set_tooltip_text('Reloj Parlante')
        self.insert(button, -1)
        
        self.show_all()
        
        self.grupo1[0].set_active(True)
        
    def __get_toggle_boton(self, archivo, tooltip_text):
        
        from gi.repository import GdkPixbuf
        
        boton = Gtk.ToggleToolButton()
        imagen = Gtk.Image()
        pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_size(archivo, 32, 32)
        
        imagen.set_from_pixbuf(pixbuf)
        boton.set_icon_widget(imagen)
        
        if tooltip_text:
            boton.set_tooltip_text(tooltip_text)
            boton.TOOLTIP = tooltip_text
        
        imagen.show()
        boton.show()
        
        return boton
    
    def __emit_accion(self, widget):
        
        button = widget
        if widget.get_active():
            for button in self.grupo1:
                if button != widget:
                    button.set_active(False)
                    break
                
        else:
            for button in self.grupo1:
                if button != widget:
                    button.set_active(True)
                    break
                
        self.emit("accion", button.TOOLTIP, button.get_active())
        
    def __emit_espeak(self, widget):
        
        self.emit("speak", widget.get_active())
    