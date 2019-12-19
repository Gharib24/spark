import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk, GObject

#--------------------------------------------------------------------------------------------------

class Rebuild:
	def __init__(self):
		super().__init__()

	def rebuild(self):
		table = Gtk.Table(rows=10, columns=3, homogeneous=False)
		table.set_col_spacings(15)
		table.set_row_spacings(15)
		table.props.border_width = 10
		vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
		vbox.add(table)

		stack_name = str(self.category.index("Create an ISO image"))
		self.stack_1.add_named(vbox, stack_name)

		label = Gtk.Label("Select file:", xalign=0, yalign=0.6)
		table.attach(label, 0, 1, 0, 1, xoptions=Gtk.AttachOptions.FILL ,yoptions=Gtk.AttachOptions.FILL, xpadding=0, ypadding=0)
		self.file_liststore = Gtk.ListStore(str)
		if self.cfg.get('file') != None:
			files = self.cfg.get('file').split()
			for i in files:
				self.file_liststore.append([i])
			SENSITIVE=True
		else:
			self.file_liststore.append(["Empty"])
			SENSITIVE=False
		self.combobox = Gtk.ComboBox()
		self.combobox.set_model(self.file_liststore)
		cellrenderertext = Gtk.CellRendererText()
		self.combobox.pack_end(cellrenderertext, True)
		self.combobox.add_attribute(cellrenderertext, "text", 0)
		self.combobox.set_active(0)
		table.attach(self.combobox , 1, 2, 0, 1, xoptions=Gtk.AttachOptions.FILL ,yoptions=Gtk.AttachOptions.FILL, xpadding=0, ypadding=0)
		self.combobox.connect("changed", self.on_combo_changed_rebuild)

		self.select_iso_file_button = Gtk.Button(label="Choose file")
		self.select_iso_file_button.connect("clicked", self.file_chooser)
		table.attach(self.select_iso_file_button, 2, 3, 0, 1, xoptions=Gtk.AttachOptions.FILL ,yoptions=Gtk.AttachOptions.FILL, xpadding=0, ypadding=0)

		label = Gtk.Label("File name:", xalign=0, yalign=0.6)
		table.attach(label, 0, 1, 1, 2, xoptions=Gtk.AttachOptions.FILL ,yoptions=Gtk.AttachOptions.FILL, xpadding=0, ypadding=0.1)

		self.file_name_entry = Gtk.Entry(text='auto-install.iso')
		table.attach(self.file_name_entry, 1, 2, 1, 2, xoptions=Gtk.AttachOptions.FILL ,yoptions=Gtk.AttachOptions.FILL, xpadding=0, ypadding=0)

		self.button = Gtk.Button(label="Create ISO file")
		self.button.set_sensitive(SENSITIVE)
		self.button.connect("clicked", self.on_button_clicked_rebuild, 2)
		table.attach(self.button, 2, 3, 1, 2, xoptions=Gtk.AttachOptions.FILL ,yoptions=Gtk.AttachOptions.FILL, xpadding=0, ypadding=0)

		separator = Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL)
		table.attach(separator, 0, 3, 2, 3, xoptions=Gtk.AttachOptions.FILL ,yoptions=Gtk.AttachOptions.FILL, xpadding=0, ypadding=0)

		self.label = Gtk.Label()
		table.attach(self.label, 1, 2, 4, 5, xoptions=Gtk.AttachOptions.EXPAND ,yoptions=Gtk.AttachOptions.FILL, xpadding=0, ypadding=0)

		self.spinner = Gtk.Spinner(height_request=50, width_request=50)
		table.attach(self.spinner, 1, 2, 6, 7, xoptions=Gtk.AttachOptions.EXPAND ,yoptions=Gtk.AttachOptions.FILL, xpadding=0, ypadding=0)

		separator = Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL)
		table.attach(separator, 1, 2, 7, 8, xoptions=Gtk.AttachOptions.FILL ,yoptions=Gtk.AttachOptions.FILL, xpadding=0, ypadding=0)



















































































