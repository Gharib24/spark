import gi
gi.require_version('Gtk', '3.0')
gi.require_version('Pango', '1.0')
from gi.repository import Gtk, Gdk, Pango

from datastore import datastore

text_buffer = Gtk.TextBuffer()
bold_tag = text_buffer.create_tag( "bold", size_points=16, weight=Pango.Weight.BOLD)
normal_tag = text_buffer.create_tag("normal",size_points=14, weight=Pango.Weight.NORMAL)
underline_tag = text_buffer.create_tag( "underline", size_points=16,  underline=Pango.Underline.DOUBLE)
white_fg_tag = text_buffer.create_tag( "white", foreground="#ffffff")
black_fg_yellow_bg_tag = text_buffer.create_tag( "colored0", foreground="#000000", background="#ffff00")
yellow_fg_black_bg_tag = text_buffer.create_tag( "colored3", foreground="#ffff00", background="#000000")
orange_fg_tag = text_buffer.create_tag( "colored1", foreground="#e65c00")
green_fg_tag = text_buffer.create_tag( "colored2", foreground="#339933")
blue_fg_tag = text_buffer.create_tag( "colored4", foreground="#3465a4")
x_fg_tag = text_buffer.create_tag( "colored5", foreground='cyan')

editable_tag = text_buffer.create_tag( "editable", editable=0) 
liststore = Gtk.ListStore(str, str, str, str)

#--------------------------------------------------------------------------------------------------
class View:
	def __init__(self):
		self.store = datastore
		self.text_buffer = text_buffer

	def __view_a(self, state):
		if state == True:
			if len(liststore) != 0:
				for i in range(len(liststore)):
					iter = liststore.get_iter(0)
					liststore.remove(iter)
			for i in range(len(datastore)):
				if len(datastore[i]) == 4:
					liststore.append([datastore[i][0], datastore[i][1], datastore[i][2],datastore[i][3]])

	def __view_b(self, state):
		if state == True:
			start, end = self.text_buffer.get_bounds()
			self.text_buffer.delete(start, end)
			self.text_buffer.insert_with_tags(start, "* * * SPARK * * *\n", white_fg_tag,bold_tag, yellow_fg_black_bg_tag)
			self.text_buffer.insert_with_tags(start, "<Owner>\t<Question name>\t<Question type>\t<Value>", black_fg_yellow_bg_tag, bold_tag, underline_tag)

			for i in range(len(datastore)):
				if len(datastore[i]) == 4:
#					print(datastore[i][0], datastore[i][1])
					start, end = self.text_buffer.get_bounds()
					self.text_buffer.insert_with_tags(end, "\n{} ".format(datastore[i][0]), orange_fg_tag, blue_fg_tag)
					self.text_buffer.insert_with_tags(end, " {}".format(datastore[i][1]), orange_fg_tag, editable_tag)
					self.text_buffer.insert_with_tags(end, " {}".format(datastore[i][2]), green_fg_tag, editable_tag)
					self.text_buffer.insert_with_tags(end, " {}".format(datastore[i][3]), x_fg_tag, green_fg_tag)

			start, end = self.text_buffer.get_bounds()
			self.text_buffer.apply_tag(normal_tag, start, end)

	def view(self, state=True):
		self.__view_a(state)
		self.__view_b(state)
v = View()

#--------------------------------------------------------------------------------------------------

class Review(object):
	def __init__(self):
		pass

	def __review_a(self):
		self.log.debug("{} : {}".format(__name__, __file__))

		vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
		vbox.set_border_width(5)

		stack_name = "1"
		self.stack_2.add_named(vbox, stack_name)
		
		button = Gtk.Button(label="Reload")
		button.connect("clicked", self.on_button_clicked_view)

		scrolled_window = Gtk.ScrolledWindow()
		scrolled_window.set_policy(Gtk.PolicyType.ALWAYS, Gtk.PolicyType.ALWAYS)
		scrolled_window.set_border_width(0)
		vbox.pack_start(scrolled_window, True, True, 10)
		vbox.pack_start(button, 0, 0, 0)

		self.liststore = liststore
		view = Gtk.TreeView(model=self.liststore)
		view.set_headers_visible(True)
		view.set_hexpand (False)
		view.set_vexpand (True)
		view.set_grid_lines(True)
		view.set_grid_lines(1)

		scrolled_window.add(view)

		resizable = [True, True, True, True]
		width = [10, 200, 80, 300]
		background = ['pink', 'cyan','yellow', 'green']
		for i, titles in enumerate(['Owner', 'Question name', 'Question type', 'Value'], 0):
			renderer = Gtk.CellRendererText()
			renderer.set_fixed_size(width=width[i], height=30)
			renderer.set_property('cell-background', background[i])
			column = Gtk.TreeViewColumn(titles, renderer, text=i)
			column.set_min_width(width[i])
			column.set_reorderable(False)
			column.set_resizable(True)
			column.set_resizable(resizable[i])
			view.append_column(column)
	def __review_b(self):
		vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
		vbox.set_border_width(5)

		stack_name = "2"
		self.stack_2.add_named(vbox, stack_name)
		
		button = Gtk.Button(label="Reload")
		button.connect("clicked", self.on_button_clicked_view)

		scrolled_window = Gtk.ScrolledWindow()
		scrolled_window.set_policy(Gtk.PolicyType.ALWAYS, Gtk.PolicyType.ALWAYS)
		scrolled_window.set_border_width(0)
		vbox.pack_start(scrolled_window, True, True, 0)
		vbox.pack_start(button, 0, 0, 0)

		self.text_buffer = text_buffer
		# XXX a textview (displays the buffer)
		textview = Gtk.TextView(buffer = self.text_buffer)
		textview.set_border_width(5)
		scrolled_window.add(textview)
		textview.set_cursor_visible(0)
		textview.set_editable(0)
		textview.override_background_color(Gtk.StateFlags.NORMAL, Gdk.RGBA(0,0.1,0.2))
		#textview.set_wrap_mode(Gtk.WrapMode.WORD)
		#start, end = self.text_buffer.get_bounds()
		#self.text_buffer.insert(end,"# XXX test")
		#self.text_buffer.insert_with_tags(start, "*** Spark ***", self.white_fg_tag, self.bold_tag)

	def review(self):
		self.__review_a()
		self.__review_b()

	def on_button_clicked_view(self, button):
		v.view(True)


