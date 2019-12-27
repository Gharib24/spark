#!/usr/bin/python3
# -*- coding: utf-8 -*-
import gi, sys
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

#sys.path.append('./')
sys.path.append('./handler')
sys.path.append('./stack')
#sys.path.append('./data/')

from logging_initializer import Logging
from main_handler import Handler
from users import Users
from basicoptions import BasicOptions
from network import Network
from partition import Partition
from apt_sources import AptSources
from package import PackageSelection
from bootloader import BootLoader
from script import Script
from rebuild import Rebuild
from review import Review
from menu import Menu
from dialog import Dialog
from value import Value
from sys_supported import Config
import spark_lists
#--------------------------------------------------------------------------------------------------

class SparkWindow(Gtk.ApplicationWindow, 
	Handler,
	Users, BasicOptions, Network, Partition, AptSources, PackageSelection, BootLoader, Script, 
	Review, Rebuild, 
	Menu, Dialog, Value):

	def __init__(self, app, **kwargs):
		Gtk.ApplicationWindow.__init__(self, title="Spark", application=app, **kwargs)
		super().__init__()
		self.id = {}
		self.files_dir()
		self.log = Logging(name= self.get_title(), leval = 'DEBUG' ,logger_type = 'both', log_file=self.log_file, state=False)
		self.cfg = Config(self.config_file)

	def spark(self):
		self.__main_view()
		self.connect("delete-event", self.on_delete_event)

		if self.cfg.get('dark') == True:
			settings = Gtk.Settings.get_default()
			settings.set_property('gtk-application-prefer-dark-theme', True)

		self.show_all()

		if self.cfg.get('panel') == True:
			self.frame_3.show()
		else:

			self.frame_3.hide()

		if self.value_length(self.preseed_file) > 0:
			self.question_dialog('load values',' load values from last session', data='load')

	def __main_view(self):
		self.set_default_size(1000, 500)
#		self.set_resizable(False)
		self.set_border_width(0)
#		self.set_icon_from_file("./data/spark.svg")
		main_vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
		self.add(main_vbox)
		self.hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
		self.menu()
		self.left_view = self.left_view()
		self.center_view = self.center_view()
		self.right_view = self.right_view()

		main_vbox.pack_start(self.menubar , False, False, 0)
		main_vbox.pack_start(self.hbox, True, True, 5)
		self.hbox.pack_start(self.left_view, False, True, 5)
		self.hbox.pack_start(self.center_view, True, True, 5)
		self.hbox.pack_end(self.right_view, True, True, 5)

		self.statusbar = Gtk.Statusbar(margin_bottom=0, margin_top=0)
		self.statusbar_context_1 = self.statusbar.get_context_id("statusbar")
		main_vbox.pack_end(self.statusbar, False, False, 0)
		widget = Gtk.Statusbar()

	def left_view(self):
		self.category = spark_lists.category
		frame = Gtk.Frame(label=None)
		frame.set_label_align(xalign=0.01, yalign=0.5)
		frame.props.border_width = 0
		liststore = Gtk.ListStore(str)
		for i in range(len(self.category)):
			liststore.append([self.category[i]])
		category_view = Gtk.TreeView(model = liststore)
		category_view.set_enable_tree_lines(1)
		category_view.set_grid_lines(True)
		category_view.set_grid_lines(1)
		category_view.set_hexpand (False)
		category_view.set_vexpand (True)
		category_view.set_headers_visible(False)
		renderer = Gtk.CellRendererText()
		renderer.set_fixed_size (width=260, height=50)
		renderer.set_property('font', 'Cantarell Regular 16')
		column = Gtk.TreeViewColumn("category", renderer, text=0)
		category_view.append_column(column)
		self.selection = category_view.get_selection()
		self.selection.connect("changed", self.on_treeview_selection_changed)
		
		frame.add(category_view)
		return frame

	def center_view(self):
		self.stack_1 = Gtk.Stack()
		self.stack_1.set_vexpand(False)
		self.stack_1.set_hexpand(False)
		self.frame_2 = Gtk.Frame(label=None)
		self.frame_2.set_label_align(xalign=0.01, yalign=0.5)
		self.frame_2.props.border_width = 0
		self.frame_2.set_hexpand(True)
		self.frame_2.add(self.stack_1)
		self.users()
		self.localization()
		self.network()
		self.partition()
		self.aptsources()
		self.package()
		self.bootloader()
		self.script()
		self.rebuild()
		return self.frame_2

	def right_view(self):
		self.frame_3 = Gtk.Frame(label='Review')
		self.frame_3.set_label_align(xalign=0.01, yalign=0.5)
		self.frame_3.props.border_width = 0
		vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
		self.frame_3.add(vbox)
		self.stack_2  = Gtk.Stack()
		self.stack_2.set_vexpand(True)
		self.stack_2.set_hexpand(True)
		vbox.add(self.stack_2)
		self.review()
		separator = Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL)
		vbox.add(separator)
		box = Gtk.Box(spacing=20)
		box.set_border_width(10)
		vbox.add(box)
		radiobutton1 = Gtk.RadioButton(label='View style 1')
		radiobutton2 = Gtk.RadioButton(label='View style 2', group=radiobutton1)
		radiobutton1.connect("toggled", self.on_radio_button_toggled_view)
		radiobutton2.connect("toggled", self.on_radio_button_toggled_view)
		box.pack_start(radiobutton1, True, False, 0)
		box.pack_start(radiobutton2, True, False, 0)
		return self.frame_3

#	def __str__(self):
#		return __name__

class Application(Gtk.Application):
	def __init__(self):
		super().__init__(application_id='org.spark.spark', flags=0)
		
	def do_activate(self):
		self.win = self.props.active_window
		if not self.win:
			self.win = SparkWindow(self)
		
		self.win.spark()

	def do_startup(self):
		Gtk.Application.do_startup(self)

def main(version=None):
	app = Application()
	return app.run(sys.argv)

if __name__ == "__main__":
	main()
#--------------------------------------------------------------------------------------------------

