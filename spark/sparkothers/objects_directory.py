#!/usr/bin/env python
import sys

import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GObject


class ObjectsDirectory:
	def __init__(self):
		super().__init__()
		self.question_to_own_widget_object_dict = {}
		self.widgets_object_dict  = {}
		self.labels_object_dict = {}

	def whoami(self):
		return sys._getframe(1).f_code.co_name

	def naming(self, *name):
		name = ' '.join(name)
		translation_table = dict.fromkeys(map(ord, '$@%&*!+\|-/ '), "_")
		name = name.translate(translation_table)
		name = name.lstrip('_').rstrip('_').lower()
		name = name.replace('gtk', '')
		while '__' in name:
			name = name.replace('__', '_')
		return name

	def container_name_space(self, container, name):
		type_name = GObject.type_name(container)
		newname = self.naming(type_name, name)
#		self.log.info(newname)
		if hasattr(self, newname):
			delattr(self, newname)
		setattr(self, newname,  container)
		return newname

	def widget_name_space(self, widget, *args):
		name = ' '.join(map(str, args))
		type_name = GObject.type_name(widget)
		newname = self.naming(type_name, name)
#		self.log.info(newname)
		if type_name == "GtkLabel":
				self.labels_object_dict[newname] = widget
		else:
			self.widgets_object_dict[newname] = widget
		return newname

