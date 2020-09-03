#!/usr/bin/python3
# -*- coding: utf-8 -*-
import sys

import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GdkPixbuf, Gio

from spark.sparkviews.header_bar import HeaderBar
from spark.sparkviews.dialog import Dialog
from spark.sparkviews.stack_pager import StackPager

from spark.sparkhandlers.main_handler import Handler as MainHandler

from spark.sparkothers.return_widget_field_value import WidgetsFieldValue
from spark.sparkothers.config import Config
from spark.sparkothers.console_log import ConsoleLog
from spark.sparkothers import static_data
from spark.sparkothers import settings
from spark.sparkothers.debian_installer_preseed_questions import preseed_questions_identifier

class SparkWindow(Gtk.ApplicationWindow, HeaderBar, MainHandler, StackPager, Dialog, WidgetsFieldValue, Config):

	def __init__(self, app, **kwargs):
		Gtk.ApplicationWindow.__init__(self, title=settings.APP_NAME, application=app, **kwargs)
		self.static_data = static_data
		Config.__init__(self)
		StackPager.__init__(self)
		WidgetsFieldValue.__init__(self)
		super().__init__()

		if "debug" in sys.argv:
			self.debug = True
		else:
			self.debug = False
		if "extra" in sys.argv:
			self.extra = True
		else:
			self.extra = False

		self.TESTPAGE = 0
		for i in sys.argv:
			if i.isdigit():
				j = int(i)
				if j <= 9:
					self.TESTPAGE = i
					break
		self.on_load = True
		self.log = ConsoleLog(self.debug)
		self.log.log_name = settings.APP_NAME
		self.log.info('debug ON')
		self.settings = settings

	def spark_show_all(self):
		self.main_view()
		self.show_all()
#		self.stack_1.set_visible_child_name(str(self.TESTPAGE))
		self.treeselection.select_path(self.TESTPAGE)
		if self.get_value_from_preseed_file():
			self.base_message_dialog('question', 'load_values')
		self.on_load = False

	def main_view(self):
		self.set_border_width(0)
		self.set_name('toplevale_window')
		self.set_position(Gtk.WindowPosition(1))
		self.set_default_size(1132, 700)
#		self.set_resizable(False)
#		self.set_wmclass(settings.APP_NAME, settings.APP_NAME)

		#icon = GdkPixbuf.Pixbuf.new_from_file_at_size(self.settings.APP_ICON, 32, 32)
		icon = Gtk.IconTheme.get_default().load_icon('non-starred', 32, 0)
		self.set_icon(icon)
#		self.set_icon_from_file(settings.APP_ICON)
		self.connect("delete-event", self.on_delete_event)
		self.set_titlebar(self.header_bar())
		main_vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)

		self.add(main_vbox)
		self.hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)

		main_vbox.pack_start(self.hbox, True, True, 0)
		self.hbox.pack_start(self.left_view(), False, True, 5)
		self.hbox.pack_start(self.right_view(), True, True, 5)
		main_vbox.pack_end(self.bottom_view(), False, False, 0)

	def bottom_view(self):
		hbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)

		self.statusbar = Gtk.Statusbar(margin_bottom=0, margin_top=0)
		self.statusbar_context_1 = self.statusbar.get_context_id("statusbar")
		self.statusbar.set_property('width-request', 270)
		hbox.pack_start(self.statusbar, False, False, 0)

		self.levelbar = Gtk.LevelBar(margin_bottom=5, margin_top=0, margin_left=5, margin_right=5)
		self.levelbar.set_min_value(0)
		self.levelbar.set_property('height-request', 22)
		hbox.pack_end(self.levelbar, True, True, 0)
		return hbox

	def left_view(self):
		frame = Gtk.Frame(label=None, margin_top=10)
		frame.set_label_align(xalign=0.01, yalign=0.5)
		frame.props.border_width = 0

		if self.extra:
			self.static_data.category.append(("Network Console"))
#		if self.debug:
#			self.static_data.category.append(("Create an ISO image"))

		liststore = Gtk.ListStore(GdkPixbuf.Pixbuf, str)
		for text in self.static_data.category:
			icon_name = self.static_data.category_icons.get(text)
			pixbuf = Gtk.IconTheme.get_default().load_icon(icon_name, 32, 0)
			liststore.append([pixbuf, text])

		category_tree_view = Gtk.TreeView(model=liststore)
		category_tree_view.set_enable_tree_lines(1)
		category_tree_view.set_grid_lines(True)
		category_tree_view.set_grid_lines(1)
		category_tree_view.set_hexpand (False)
		category_tree_view.set_vexpand (True)
		category_tree_view.set_headers_visible(False)

		cellrendererpixbuf = Gtk.CellRendererPixbuf()
		treeviewcolumn = Gtk.TreeViewColumn("Logo")
		category_tree_view.append_column(treeviewcolumn)
		treeviewcolumn.pack_start(cellrendererpixbuf, False)
		treeviewcolumn.add_attribute(cellrendererpixbuf, "pixbuf", 0)

		cellrenderertext = Gtk.CellRendererText()
		cellrenderertext.set_fixed_size (width=265, height=50)
		cellrenderertext.set_property('font', 'Cantarell Regular 16')
		treeviewcolumn = Gtk.TreeViewColumn("category", cellrenderertext, text=1)
		category_tree_view.append_column(treeviewcolumn)

		self.treeselection = category_tree_view.get_selection()
		self.treeselection.connect("changed", self.on_treeselection_changed_main)

		frame.add(category_tree_view)
		self.frame = frame
		return frame

	def right_view(self):
		self.stack_1 = Gtk.Stack()
		self.stack_1.set_vexpand(False)
		self.stack_1.set_hexpand(False)
		self.frame_2 = Gtk.Frame(label="")
		self.frame_2.set_label_align(xalign=0.01, yalign=0.5)
		self.frame_2.props.border_width = 0
		self.frame_2.set_hexpand(True)
		self.frame_2.add(self.stack_1)
		self.stack_containers()

		self.widgets_parking(self.static_data.stack_components)

		return self.frame_2

	def __str__(self):
		return(f"{settings.APP_NAME} {settings.APP_VERSION}")


class Application(Gtk.Application):
	def __init__(self):
		super().__init__(application_id='org.spark.spark', flags=0)

	def do_activate(self,  **kwargs):
		if not self.win:
			self.win = SparkWindow(self)
		self.win.spark_show_all()
		self.win.present()

	def do_startup(self):
		Gtk.Application.do_startup(self)
		self.win = self.props.active_window


def main(version=None):
	app = Application()
	return app.run(sys.argv[0:1])

if __name__ == "__main__":
	main()


