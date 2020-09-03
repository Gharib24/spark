#!/usr/bin/env python
import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

from spark.sparkothers.objects_directory import ObjectsDirectory


class BaseContainer(ObjectsDirectory):
	def __init__(self):
		super().__init__()

	def base_vbox(self, namespace):
		vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
		vbox.props.border_width = 10
		self.container_name_space(vbox, namespace)
		return vbox

	def base_grid(self, namespace):
		grid = Gtk.Grid(expand=False)
		grid.set_hexpand(True)
		grid.set_vexpand(False)
		grid.set_row_spacing(15)
		grid.set_column_spacing(15)
		self.container_name_space(grid, namespace)
		return grid

	def base_frame(self, namespace, label_text=None):
		frame = Gtk.Frame(label=label_text)
		frame.set_label_align(xalign=0.01, yalign=0.5)
		frame.set_hexpand(True)
		frame.set_vexpand(True)
		frame.set_margin_top(10)
		self.container_name_space(frame, namespace)
		return frame

	def base_scrolledwindow(self, namespace):
		scrolledwindow = Gtk.ScrolledWindow()
		scrolledwindow.set_policy(
				Gtk.PolicyType.AUTOMATIC,
				Gtk.PolicyType.AUTOMATIC)
		scrolledwindow.set_shadow_type(True)
		scrolledwindow.set_vexpand(True)
		self.container_name_space(scrolledwindow, namespace)
		return scrolledwindow

	def base_actionbar(self, namespace):
		actionbar = Gtk.ActionBar()
		actionbar.set_hexpand(0)
		self.container_name_space(actionbar, namespace)
		return actionbar

	def base_buttonbox(self, namespace):
		buttonbox = Gtk.ButtonBox()
		buttonbox.set_orientation(Gtk.Orientation.HORIZONTAL)
		buttonbox.set_spacing(2)
		self.container_name_space(buttonbox, namespace)
		return buttonbox

