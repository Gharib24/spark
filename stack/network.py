import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

from datastore import network_questions as questions

#--------------------------------------------------------------------------------------------------

class Network:
	def __init__(self):
		super().__init__()

	def network(self):
		table = Gtk.Table(rows=12, columns=3, homogeneous=False)
		table.set_col_spacings(15)
		table.set_row_spacings(15)
		table.props.border_width = 10
		table.attach( Gtk.Label(''), 1, 3, 0, 1, xoptions=Gtk.AttachOptions.EXPAND ,yoptions=Gtk.AttachOptions.FILL)

		stack_name = str(self.category.index("Network Configuration"))
		self.stack_1.add_named(table, stack_name)

		# XXX right side of grid XXX
		label_text =['Hostname',
			 'Domain',
			'Interface',
			'Wireless Security Type',
			'Wireless SSID',
			'Wireless Key',
			'IP4 Method', 'IP Address', 'Netmask', 'Gateway', 'nameservers']

		top_attach = 0; bottom_attach =1
		for i, text in enumerate(label_text, 0):
			if i in [2 , 6]:
				separator = Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL)
				table.attach(separator, 0, 3, top_attach, bottom_attach, xoptions=Gtk.AttachOptions.FILL ,yoptions=Gtk.AttachOptions.FILL, xpadding=0, ypadding=0)
				top_attach += 1; bottom_attach += 1

			label = Gtk.Label(text, xalign=0, yalign=0.5)
			table.attach(label, 0, 1, top_attach, bottom_attach, xoptions=Gtk.AttachOptions.FILL ,yoptions=Gtk.AttachOptions.FILL, xpadding=0, ypadding=0)
			top_attach += 1; bottom_attach += 1

		top_attach = 0; bottom_attach =1
		for i, question in  enumerate(questions, 0):
			if i in [0, 1 , 4, 6, 10, 11, 12, 13]:
				entry = Gtk.Entry(placeholder_text=None)
				table.attach(entry, 1, 3, top_attach, bottom_attach, xoptions=Gtk.AttachOptions.FILL ,yoptions=Gtk.AttachOptions.FILL, xpadding=0, ypadding=0)
				self.id[question] = entry
				if i in [4, 6, 10, 11, 12, 13]:
					entry.set_sensitive(False)
				entry.connect('changed', self.on_entry_changed, question)

			elif  i in [2]:
				top_attach += 1; bottom_attach += 1

				comboboxtext_1 = Gtk.ComboBoxText.new_with_entry()
				comboboxtext_1.append('auto', 'auto')
				comboboxtext_1.append('eth0', 'eth0')
				comboboxtext_1.append('wlan0', 'wlan0')
				comboboxtext_1.set_entry_text_column(0)
				comboboxtext_1.connect("changed", self.on_comboboxtext_with_entry_changed, question)
				table.attach(comboboxtext_1, 1, 3, top_attach, bottom_attach, xoptions=Gtk.AttachOptions.FILL ,yoptions=Gtk.AttachOptions.FILL, xpadding=0, ypadding=0)
				self.id[question] = comboboxtext_1
			elif  i == 3:
				self.w_comboboxtext = Gtk.ComboBoxText()
				self.w_comboboxtext.set_sensitive(False)
				self.w_comboboxtext.append('wep/open', 'WEP/OPEN')
				self.w_comboboxtext.append('wpa', 'WPA')
				self.w_comboboxtext.connect("changed", self.on_comboboxtext_changed, question)
				table.attach(self.w_comboboxtext, 1, 3, top_attach, bottom_attach, xoptions=Gtk.AttachOptions.FILL ,yoptions=Gtk.AttachOptions.FILL, xpadding=0, ypadding=0)
				self.id[question] = self.w_comboboxtext
			elif i == 8:
				top_attach += 1; bottom_attach += 1
				comboboxtext_2 = Gtk.ComboBoxText()
				comboboxtext_2.append('false', 'DHCP')
				comboboxtext_2.append('true', 'Static IP')
				comboboxtext_2.connect("changed",self.on_comboboxtext_changed, question)
				table.attach(comboboxtext_2, 1, 3, top_attach, bottom_attach, xoptions=Gtk.AttachOptions.FILL ,yoptions=Gtk.AttachOptions.FILL, xpadding=0, ypadding=0)
				self.id[question] = comboboxtext_2
			if  i in [5, 7, 9]:
				continue
			else:
				top_attach += 1; bottom_attach += 1

