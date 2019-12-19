import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk

from datastore import command_questions as questions

class Script:
	def __init__(self):
		super().__init__()

	def __pre(self):
		vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
		vbox.set_border_width(0)

		stack_name = str(self.category.index("Pre-Installation Script"))
		self.stack_1.add_named(vbox, stack_name)

		scrolled_window = Gtk.ScrolledWindow()
		scrolled_window.set_policy(Gtk.PolicyType.ALWAYS, Gtk.PolicyType.AUTOMATIC)
		scrolled_window.set_border_width(5)
		vbox.pack_start(scrolled_window, True, True, 0)

		self.text_buffer_a = Gtk.TextBuffer()
		# XXX a textview (displays the buffer)
		textview = Gtk.TextView(buffer = self.text_buffer_a)
		textview.set_border_width(1)
		scrolled_window.add(textview)
		textview.set_cursor_visible(True)
		textview.set_editable(True)
		textview.set_wrap_mode(Gtk.WrapMode.WORD)
		start, end = self.text_buffer_a.get_bounds()
		self.text_buffer_a.insert(end,"#!/bin/sh\n")
		self.text_buffer_a.connect( "changed", self.on_text_changed, questions[0])
		self.id[questions[0]] = self.text_buffer_a

		actionbar = Gtk.ActionBar()
		actionbar.set_hexpand(True)
		vbox.add(actionbar)

		self.button_pre_save = Gtk.Button(label='Save')
		self.button_pre_add = Gtk.Button(label='Add')
		self.button_pre_save.set_property("width-request", 100)
		self.button_pre_add.set_property("width-request", 100)
		actionbar.pack_end(self.button_pre_save)
		actionbar.pack_end(self.button_pre_add)
		self.button_pre_save.connect("clicked", self.on_button_clicked, questions[0])
		self.button_pre_add.connect("clicked", self.on_button_clicked, questions[0])


	def __post(self):
		vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
		vbox.set_border_width(0)

		stack_name = str(self.category.index("Post-Installation Script"))
		self.stack_1.add_named(vbox, stack_name)

		scrolled_window = Gtk.ScrolledWindow()
		scrolled_window.set_policy(Gtk.PolicyType.ALWAYS, Gtk.PolicyType.AUTOMATIC)
		scrolled_window.set_border_width(5)
		vbox.pack_start(scrolled_window, True, True, 0)

		self.text_buffer_b = Gtk.TextBuffer()
		textview = Gtk.TextView(buffer = self.text_buffer_b)

		textview.set_border_width(1)
		scrolled_window.add(textview)
		textview.set_cursor_visible(True)
		textview.set_editable(True)
		textview.set_wrap_mode(Gtk.WrapMode.WORD)
		start, end = self.text_buffer_b.get_bounds()
		self.text_buffer_b.insert(end,"#!/bin/sh\n")
		self.text_buffer_b.connect( "changed", self.on_text_changed, questions[1])
		self.id[questions[1]] = self.text_buffer_b

		actionbar = Gtk.ActionBar()
		actionbar.set_hexpand(True)
		vbox.add(actionbar)

		self.button_post_save = Gtk.Button(label='Save')
		self.button_post_add = Gtk.Button(label='Add')
		self.button_post_save.set_property("width-request", 100)
		self.button_post_add.set_property("width-request", 100)
		actionbar.pack_end(self.button_post_save)
		actionbar.pack_end(self.button_post_add)
		self.button_post_save.connect("clicked", self.on_button_clicked, questions[1])
		self.button_post_add.connect("clicked", self.on_button_clicked, questions[1])


	def script(self):
		self.__pre()
		self.__post()

#	def on_text_changed(self, buffer,  *args):
#		question = args[0]
#		chars = buffer.get_char_count() 
#		lines = buffer.get_line_count() 
#		start, end = buffer.get_bounds()
#		value = buffer.get_text(start, end, include_hidden_chars = False)
#		pass
