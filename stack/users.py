import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

from datastore import account_questions as questions
#--------------------------------------------------------------------------------------------------

class Users:
	def __init__(self):
		super().__init__()

	def users(self):
		table = Gtk.Table(rows=12, columns=3, homogeneous=False)
		table.set_col_spacings(15)
		table.set_row_spacings(15)
		table.props.border_width = 10
		table.attach( Gtk.Label(''), 1, 3, 0, 1, xoptions=Gtk.AttachOptions.EXPAND ,yoptions=Gtk.AttachOptions.FILL)

		stack_name = str(self.category.index("User Settings"))
		self.stack_1.add_named(table, stack_name)

		# XXX left side of table
		label_text = ['Full name', 'Username', 'User password', 'User default groups','Disable root login', 'Root password']
		top_attach = 0; bottom_attach =1
		for i, name in enumerate(label_text, 0):
			if i  == 4:
				separator = Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL)
				table.attach(separator, 0, 3, top_attach, bottom_attach, xoptions=Gtk.AttachOptions.FILL ,yoptions=Gtk.AttachOptions.FILL, xpadding=0, ypadding=0)
				top_attach += 1; bottom_attach += 1

			label = Gtk.Label(name, xalign=0, yalign=0.6)
			table.attach(label, 0, 1, top_attach, bottom_attach, xoptions=Gtk.AttachOptions.FILL ,yoptions=Gtk.AttachOptions.FILL, xpadding=0, ypadding=0)
			top_attach += 1; bottom_attach += 1

		# XXX right side of table
		top_attach = 0; bottom_attach =1
		for i, question in enumerate(questions, 0):
			if question == 'passwd/root-login': # i 4
				checkbutton = Gtk.CheckButton(label=None, xalign=0, yalign=0.5)
				checkbutton.connect("toggled", self.on_check_button_toggled, question)
				table.attach(checkbutton, 1, 3, top_attach, bottom_attach, xoptions=Gtk.AttachOptions.FILL ,yoptions=Gtk.AttachOptions.FILL, xpadding=0, ypadding=0)
				self.id[question] = checkbutton
			else :
				entry = Gtk.Entry(placeholder_text=None)
				table.attach(entry, 1, 3, top_attach, bottom_attach, xoptions=Gtk.AttachOptions.FILL ,yoptions=Gtk.AttachOptions.FILL, xpadding=0, ypadding=0)
				entry.set_activates_default(True)
				self.id[question] = entry
				entry.connect('changed', self.on_entry_changed, question)
#				if question == 'passwd/root-password-crypted': 
#					entry.set_sensitive(False)
				if "password" in question: 
					entry.set_visibility(False)
					entry.set_invisible_char("*")

				if i == 3:
					top_attach += 1; bottom_attach += 1

			top_attach += 1; bottom_attach += 1






