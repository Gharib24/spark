import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

from sys_supported import Locales_Zone_Info
from datastore import localization_questions as questions
#--------------------------------------------------------------------------------------------------

class BasicOptions(Locales_Zone_Info):
	def __init__(self):
		super().__init__()

	def localization(self):
		self.locales_zone_info()
		table = Gtk.Table(rows=12, columns=3, homogeneous=False)
		table.set_col_spacings(15)
		table.set_row_spacings(15)
		table.props.border_width = 10
		table.attach( Gtk.Label(''), 1, 3, 0, 1, xoptions=Gtk.AttachOptions.EXPAND ,yoptions=Gtk.AttachOptions.FILL)
		stack_name = str(self.category.index("Basic Options"))
		self.stack_1.add_named(table, stack_name)

		# XXX left side of table XXX
		label_text =['Locale',
				'Language code',
				'Country code',
				'Default keyboard language',
				'Keyboard multi language', 
				'Keyboard toggle',
				'Language Support',
				'Time zone', 
				'Hardware clock is set to UTC',
				'Use NTP to set the clock during the install']
		top_attach = 0 ; bottom_attach = 1
		for i, text in  enumerate(label_text, 0):
			if  i in [3,6,7]:
				if  i == 7:
					bottom_attach += 6 ;top_attach += 6
				separator = Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL)
				table.attach(separator, 0, 3, top_attach, bottom_attach, xoptions=Gtk.AttachOptions.FILL ,yoptions=Gtk.AttachOptions.FILL, xpadding=0, ypadding=0)
				top_attach += 1 ; bottom_attach += 1
			label = Gtk.Label(text, xalign=0, yalign=0.5)
#			label.set_alignment(0, 0.6)
			table.attach(label, 0, 1, top_attach, bottom_attach, xoptions=Gtk.AttachOptions.FILL ,yoptions=Gtk.AttachOptions.FILL, xpadding=0, ypadding=0)
			if i == 7:
				break
			top_attach += 1 ; bottom_attach += 1

		# XXX right side of table XXX
		self.locales_supported_liststore = Gtk.ListStore(bool, str, str )
		for i, name in  enumerate(self.locales_supported_list, 0):
			self.locales_supported_liststore.append([False, name[0], name[1]])

		layout_liststore = Gtk.ListStore(str, str)
		for item in self.layout_list:
			layout_liststore.append(item)

		time_zone_liststore = Gtk.ListStore(str)
		for item in self.zoneinfo_list:
			time_zone_liststore.append([item])

		top_attach = 0 ; bottom_attach = 1
		for i, question in enumerate(questions, 0):
			if i in [0]:
				locales_combobox = Gtk.ComboBox()
				locales_combobox.set_wrap_width(1)
				locales_combobox.set_model(self.locales_supported_liststore)
				cellrenderertext = Gtk.CellRendererText()
				cellrenderertext.set_alignment(xalign=0, yalign=0)
				cellrenderertext.set_fixed_size(width=300, height=20)
				locales_combobox.pack_end(cellrenderertext, True)
				locales_combobox.add_attribute(cellrenderertext, "text", 2)
				locales_combobox.connect("changed", self.on_combobox_changed, question)
				table.attach(locales_combobox, 1, 3, top_attach, bottom_attach, xoptions=Gtk.AttachOptions.FILL ,yoptions=Gtk.AttachOptions.FILL, xpadding=0, ypadding=0)
				self.id[question] = locales_combobox

			elif i in [1, 2, 3, 4, 5]:
				if i in [3]:
					top_attach += 1 ;bottom_attach += 1
					keymap_combobox = Gtk.ComboBox(model=layout_liststore, wrap_width=1)
					cellrenderertext = Gtk.CellRendererText()
					cellrenderertext.set_alignment(xalign=0, yalign=0)
					cellrenderertext.set_fixed_size(width=300, height=20)
					keymap_combobox.pack_end(cellrenderertext, True)
					keymap_combobox.add_attribute(cellrenderertext, "text", 1)
					keymap_combobox.connect("changed", self.on_combobox_changed, question)
					table.attach(keymap_combobox, 1, 3, top_attach, bottom_attach, xoptions=Gtk.AttachOptions.FILL ,yoptions=Gtk.AttachOptions.FILL, xpadding=0, ypadding=0)
					self.id[question] = keymap_combobox
				else:
					entry = Gtk.Entry(placeholder_text=None)
					table.attach(entry, 1, 3, top_attach, bottom_attach, xoptions=Gtk.AttachOptions.FILL ,yoptions=Gtk.AttachOptions.FILL, xpadding=0, ypadding=0)
					entry.connect('changed', self.on_entry_changed, question)
					entry.set_activates_default(True)
					self.id[question] = entry

			elif i in [6]:
				scrolledwindow = Gtk.ScrolledWindow()
				scrolledwindow.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
				frame = Gtk.Frame(label=None)
				frame.add(scrolledwindow)
				treeview = Gtk.TreeView(model=self.locales_supported_liststore)
				treeview.set_headers_visible(False)
				treeview.set_hexpand (False)
				treeview.set_vexpand (False)
				cellrenderertoggle = Gtk.CellRendererToggle(xalign=0, yalign=0.5)
				column_toggle = Gtk.TreeViewColumn("select", cellrenderertoggle, active=0)
				column_toggle.set_min_width(10)
				column_toggle.set_reorderable(False)
				treeview.append_column(column_toggle)
				cellrenderertext = Gtk.CellRendererText()
#				renderer_text.set_fixed_size(250, height=30)
				cellrenderertext.set_alignment(xalign=0.01 , yalign=0)
				column_text = Gtk.TreeViewColumn("Locales", cellrenderertext, text=2)
				treeview.append_column(column_text)
				scrolledwindow.add(treeview)
				top_attach += 1; bottom_attach += 7
				table.attach(frame, 1, 3, top_attach, bottom_attach, xoptions=Gtk.AttachOptions.FILL ,yoptions=Gtk.AttachOptions.FILL, xpadding=0, ypadding=0)
				cellrenderertoggle.connect("toggled", self.on_cell_toggled , question)
				top_attach += 7 ;bottom_attach += 1
				self.id[question] = cellrenderertoggle

			elif i in [7]:
				zoneinfo_combobox = Gtk.ComboBox()
				zoneinfo_combobox.set_wrap_width(1)
				zoneinfo_combobox.set_model(time_zone_liststore)
				cellrenderertext = Gtk.CellRendererText()
				cellrenderertext.set_fixed_size(width=300, height=20)
				zoneinfo_combobox.pack_start(cellrenderertext, True)
				zoneinfo_combobox.add_attribute(cellrenderertext, "text", 0)
				zoneinfo_combobox.connect("changed", self.on_combobox_changed, question)
				table.attach(zoneinfo_combobox, 1, 3, top_attach, bottom_attach, xoptions=Gtk.AttachOptions.FILL ,yoptions=Gtk.AttachOptions.FILL, xpadding=0, ypadding=0)
				self.id[question] = zoneinfo_combobox

			elif i in [8, 9]: 
				checkbutton = Gtk.CheckButton(label=label_text[i])
				checkbutton.connect("toggled", self.on_check_button_toggled, question)
				table.attach(checkbutton, 1, 2, top_attach, bottom_attach, xoptions=Gtk.AttachOptions.FILL ,yoptions=Gtk.AttachOptions.FILL, xpadding=0, ypadding=0)
				self.id[question] = checkbutton

			top_attach += 1 ;bottom_attach += 1













