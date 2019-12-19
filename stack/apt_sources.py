import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

from additional_repos import AdditionalRepos
from datastore import aptsources_questions as questions

#--------------------------------------------------------------------------------------------------

class AptSources(AdditionalRepos):
	def __init__(self):
		super().__init__()

	def aptsources(self):
		table = Gtk.Table(rows=10, columns=3, homogeneous=False)
		table.set_col_spacings(15)
		table.set_row_spacings(15)
		table.props.border_width = 10
		table.attach( Gtk.Label(''), 1, 3, 0, 1, xoptions=Gtk.AttachOptions.EXPAND ,yoptions=Gtk.AttachOptions.FILL)
		vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
		vbox.add(table)
		stack_name = str(self.category.index("Apt Sources Configuration"))
		self.stack_1.add_named(vbox, stack_name)
		# XXX left side of table
		label_text = ['Official Debian mirror', 'Mirror directory', 'Security Host', 'Volatile host','Services:' ,'contrib Repository','non-free Repository','Use A Network Mirror', 
			'Disable scan for another CD',
			'Disable CDROM entries after install']
		top_attach = 0 ; bottom_attach =1
		for i, text in enumerate(label_text, 0):
			if i <= 4:
				label = Gtk.Label(text, xalign=0, yalign=0.6)
				table.attach(label, 0, 1, top_attach, bottom_attach, xoptions=Gtk.AttachOptions.FILL ,yoptions=Gtk.AttachOptions.FILL, xpadding=0, ypadding=0)
			elif i in [5, 6, 7]:
				pass
			elif i > 8 :
				top_attach += 1; bottom_attach += 1
				separator = Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL)
				table.attach(separator, 0, 3, top_attach, bottom_attach, xoptions=Gtk.AttachOptions.FILL ,yoptions=Gtk.AttachOptions.FILL, xpadding=0, ypadding=0)
			top_attach += 1; bottom_attach += 1
		# XXX right side of table
		top_attach = 0 ; bottom_attach =1
		for i, question in enumerate(questions, 0):
			if i == 1: 
				combobox_text = Gtk.ComboBoxText.new_with_entry()
				combobox_text.append("http.us.debian.org", "http.us.debian.org")
				combobox_text.append("deb.debian.org", "deb.debian.org")
				combobox_text.append("ftp.debian.org", "ftp.debian.org")
				combobox_text.set_entry_text_column(0)
				combobox_text.connect("changed", self.on_comboboxtext_with_entry_changed, question)
				table.attach(combobox_text, 1, 3, top_attach, bottom_attach, xoptions=Gtk.AttachOptions.FILL ,yoptions=Gtk.AttachOptions.FILL, xpadding=0, ypadding=0)
				self.id[question] = combobox_text

			# XXX  entries
			elif i in [2, 4, 5]:
				entry = Gtk.Entry(placeholder_text=None)
				table.attach(entry, 1, 3, top_attach, bottom_attach, xoptions=Gtk.AttachOptions.FILL ,yoptions=Gtk.AttachOptions.FILL, xpadding=0, ypadding=0)
				entry.set_activates_default(True)
				entry.connect('changed', self.on_entry_changed, question)
				if i in [5]:
					entry.set_sensitive(False)
				self.id[question] = entry

			elif i == 6:
				buttonbox = Gtk.ButtonBox()
				buttonbox.set_orientation(Gtk.Orientation.HORIZONTAL)
				buttonbox.set_spacing(0)
				buttonbox.props.border_width = 0
				table.attach(buttonbox, 1, 2, top_attach, bottom_attach, xoptions=Gtk.AttachOptions.FILL ,yoptions=Gtk.AttachOptions.FILL, xpadding=0, ypadding=0)
				for j, name in enumerate(['security', 'updates' ,'volatile'], 0):
					checkbutton = Gtk.CheckButton(label=name , xalign=0, yalign=0)
					checkbutton.connect("toggled", self.on_check_button_toggled, question)
					buttonbox.add(checkbutton)
					self.id[name] = checkbutton
					if j == 0:
						self.id[question] = checkbutton

			elif i in [7, 8 , 9, 10, 11]:
				checkbutton = Gtk.CheckButton(label=label_text[i-2], xalign=0, yalign=0.5)
				checkbutton.connect("toggled", self.on_check_button_toggled, question)
				table.attach(checkbutton, 0, 3, top_attach, bottom_attach, xoptions=Gtk.AttachOptions.FILL ,yoptions=Gtk.AttachOptions.FILL, xpadding=0, ypadding=0)
				self.id[question] = checkbutton
			if i not in [0, 3]:
				top_attach += 1; bottom_attach += 1

		self.frame = Gtk.Frame(label='Additional repositories')
		self.frame.props.border_width = 10
		self.repos()
		vbox.add(self.frame)
		self.frame.add(self.vbox)

