import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

from datastore import bootloader_questions as questions
from datastore import finishup_questions as _questions

#--------------------------------------------------------------------------------------------------

class BootLoader:
	def __init__(self):
		super().__init__()

	def bootloader(self):
		table = Gtk.Table(rows=5, columns=3, homogeneous=False)
		table.set_col_spacings(15)
		table.set_row_spacings(15)
		table.props.border_width = 10
		table.attach(Gtk.Label(''), 1, 3, 0, 1, xoptions=Gtk.AttachOptions.EXPAND ,yoptions=Gtk.AttachOptions.FILL)

		table1 = Gtk.Table(rows=5, columns=3, homogeneous=False)
		table1.set_col_spacings(15)
		table1.set_row_spacings(15)
		table1.props.border_width = 10
		table1.attach(Gtk.Label(''), 1, 3, 0, 1, xoptions=Gtk.AttachOptions.EXPAND ,yoptions=Gtk.AttachOptions.FILL)

		vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)

		stack_name = str(self.category.index("Boot Loader Options"))
		self.stack_1.add_named(vbox, stack_name)

		vbox.pack_start(table, False, False, 10)
		vbox.pack_start(table1, False, False, 10)

		# XXX left side of table
		label_text = ['Install GRUB on device', 
			'Install GRUB to the MBR', 
			'Detected other OS on the machine',
			'EFI removable', 
			'kernel boot parameters']

		top_attach = 0; bottom_attach = 1
		for i, name in enumerate(label_text, 0):
			if i in [4]:
				separator = Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL)
				table.attach(separator, 0, 3, top_attach, bottom_attach, xoptions=Gtk.AttachOptions.FILL ,yoptions=Gtk.AttachOptions.FILL, xpadding=0, ypadding=0)
				top_attach += 1; bottom_attach += 1
			if i in [0, 4]:
				label = Gtk.Label(name, xalign=0, yalign=0.6)
				table.attach(label, 0, 1, top_attach, bottom_attach, xoptions=Gtk.AttachOptions.FILL ,yoptions=Gtk.AttachOptions.FILL, xpadding=0, ypadding=0)
			top_attach += 1; bottom_attach += 1

		# XXX right side of table
		top_attach = 0; bottom_attach =1
		for i, question in enumerate(questions, 0):
			if i in [4]:
				top_attach += 1; bottom_attach += 1
			if i == 0:
				combobox_text = Gtk.ComboBoxText.new_with_entry()
				self.combobox_text_disk = combobox_text
				combobox_text.append('/dev/sda', '/dev/sda')
				combobox_text.append('/dev/sdb', '/dev/sdb')
				combobox_text.append('/dev/sdc', '/dev/sdc')
				combobox_text.append('default', 'default')
				combobox_text.set_entry_text_column(0)
				combobox_text.connect("changed", self.on_comboboxtext_with_entry_changed, question)
				table.attach(combobox_text, 1, 3, top_attach, bottom_attach, xoptions=Gtk.AttachOptions.FILL ,yoptions=Gtk.AttachOptions.FILL, xpadding=0, ypadding=0)
				self.id[question] = combobox_text

			if i in [1, 2, 3]:
				checkbutton = Gtk.CheckButton(label=label_text[i], xalign=1, yalign=0.5)
				checkbutton.connect("toggled", self.on_check_button_toggled, question)
				table.attach(checkbutton, 0, 1, top_attach, bottom_attach, xoptions=Gtk.AttachOptions.FILL ,yoptions=Gtk.AttachOptions.FILL, xpadding=0, ypadding=0)
				self.id[question] = checkbutton

			if i == 4:
				entry = Gtk.Entry(placeholder_text=None)
				table.attach(entry, 1, 3, top_attach, bottom_attach, xoptions=Gtk.AttachOptions.FILL ,yoptions=Gtk.AttachOptions.FILL, xpadding=0, ypadding=0)
				entry.set_activates_default(True)
				entry.connect('changed', self.on_entry_changed, question)
				self.id[question] = entry

			top_attach += 1; bottom_attach += 1

		separator = Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL)
		table.attach(separator, 0, 3, top_attach, bottom_attach, xoptions=Gtk.AttachOptions.FILL ,yoptions=Gtk.AttachOptions.FILL, xpadding=0, ypadding=0)

		label_text = ['Ejecting the CD during the reboot', 'Avoid that last message about the install being complete', 'Power off the machine']

		top_attach = 0; bottom_attach =1

		label = Gtk.Label('Finishing up the installation:', xalign=1, yalign=0.6)
		table1.attach(label , 0, 1, top_attach, bottom_attach, xoptions=Gtk.AttachOptions.FILL ,yoptions=Gtk.AttachOptions.FILL, xpadding=0, ypadding=0)

		top_attach += 1; bottom_attach += 1

		for i, question in enumerate(_questions, 0):
			if i in [0, 1, 2]:
				checkbutton = Gtk.CheckButton(label=label_text[i], xalign=0, yalign=0)
				checkbutton.connect("toggled", self.on_check_button_toggled, question)
				table1.attach(checkbutton, 1, 2, top_attach, bottom_attach, xoptions=Gtk.AttachOptions.FILL ,yoptions=Gtk.AttachOptions.FILL, xpadding=0, ypadding=0)
				self.id[question] = checkbutton


			top_attach += 1; bottom_attach += 1




