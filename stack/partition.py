import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

from partition_recipe import PartitionRecipe
from datastore import partition_questions as questions

#--------------------------------------------------------------------------------------------------

class Partition(PartitionRecipe):

	def __init__(self):
		super().__init__()

	def partition(self):
		table = Gtk.Table(rows=12, columns=3, homogeneous=False)
		table.set_col_spacings(15)
		table.set_row_spacings(15)
		table.props.border_width = 10
		table.attach( Gtk.Label(''), 1, 3, 0, 1, xoptions=Gtk.AttachOptions.EXPAND ,yoptions=Gtk.AttachOptions.FILL)
		vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
		vbox.add(table)

		stack_name = str(self.category.index("Partition Information"))
		self.stack_1.add_named(vbox, stack_name)

		self.partitionrecipe_frame = Gtk.Frame(label=None)
		self.partitionrecipe_frame.props.border_width = 10
		self.partitionrecipe_frame.set_sensitive(False)
		vbox.add(self.partitionrecipe_frame)

		label_text = ['Disk', 'Partition table', 'Mount style','Automatically partitioned recipe',  'Manual partitioned recipe']
		# XXX left side of table
		top_attach = 0; bottom_attach = 1
		for i, text in  enumerate(label_text, 0):
			if i <= 2:
				label = Gtk.Label(text, xalign=0, yalign=0.6)
				table.attach(label, 0, 1, top_attach, bottom_attach, xoptions=Gtk.AttachOptions.FILL ,yoptions=Gtk.AttachOptions.FILL, xpadding=0, ypadding=0)

			if i  == 3:
				separator = Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL)
				table.attach(separator, 0, 3, top_attach, bottom_attach, xoptions=Gtk.AttachOptions.FILL ,yoptions=Gtk.AttachOptions.FILL, xpadding=0, ypadding=0)
				top_attach += 1; bottom_attach += 1

			top_attach += 1; bottom_attach +=1

		# XXX left side of table
		top_attach = 0; bottom_attach = 1
		for i, question in  enumerate(questions, 0):
			if i == 0:
				comboboxtext_1 = Gtk.ComboBoxText.new_with_entry()
				comboboxtext_1.append('/dev/sda', '/dev/sda')
				comboboxtext_1.append('/dev/sdb', '/dev/sdb')
				comboboxtext_1.append('/dev/sdc', '/dev/sdc')
				comboboxtext_1.set_entry_text_column(0)
				comboboxtext_1.connect("changed", self.on_comboboxtext_with_entry_changed, question)
				table.attach(comboboxtext_1, 1, 3, top_attach, bottom_attach, xoptions=Gtk.AttachOptions.FILL ,yoptions=Gtk.AttachOptions.FILL, xpadding=0, ypadding=0)
				self.id[question] = comboboxtext_1

			elif i == 1:
				comboboxtext_2 = Gtk.ComboBoxText()
				comboboxtext_2.append('gpt', 'GUID Partition Table')
				comboboxtext_2.append('msdos', 'Master Boot Record')
#				comboboxtext.set_active_id("gpt")
				comboboxtext_2.connect("changed",self.on_comboboxtext_changed, question)
				table.attach(comboboxtext_2, 1, 3, top_attach, bottom_attach, xoptions=Gtk.AttachOptions.FILL ,yoptions=Gtk.AttachOptions.FILL, xpadding=0, ypadding=0)
				self.id[question] = comboboxtext_2
				comboboxtext_2

			elif i == 2:
				comboboxtext_3 = Gtk.ComboBoxText()
				comboboxtext_3.append('uuid', 'UUID')
				comboboxtext_3.append('label', 'Label')
				comboboxtext_3.append('name', 'Name')
#				comboboxtext.set_active_id("uuid")
				comboboxtext_3.connect("changed",self.on_comboboxtext_changed, question)
				table.attach(comboboxtext_3, 1, 3, top_attach, bottom_attach, xoptions=Gtk.AttachOptions.FILL ,yoptions=Gtk.AttachOptions.FILL, xpadding=0, ypadding=0)
				self.id[question] = comboboxtext_3

			elif i == 3:
				top_attach += 1; bottom_attach +=1
				radiobutton1 = Gtk.RadioButton(label=label_text[3])
				table.attach(radiobutton1, 0, 1, top_attach, bottom_attach, xoptions=Gtk.AttachOptions.FILL ,yoptions=Gtk.AttachOptions.FILL, xpadding=0, ypadding=0)
				radiobutton1.connect("toggled", self.on_radio_button_toggled, question)
				self.id[question] = radiobutton1
				top_attach += 1; bottom_attach +=1

				self.choose_recipe_comboboxtext = Gtk.ComboBoxText()
				self.choose_recipe_comboboxtext.append('atomic', 'All files in one partition')
				self.choose_recipe_comboboxtext.append('home', 'Separate /home partition')
				self.choose_recipe_comboboxtext.append('multi', 'Separate /home, /usr, /var, and /tmp partitions')
#				comboboxtext.set_active_id("atomic")
				self.choose_recipe_comboboxtext.connect("changed",self.on_comboboxtext_changed, question)
				table.attach(self.choose_recipe_comboboxtext,1, 3, top_attach, bottom_attach, xoptions=Gtk.AttachOptions.FILL ,yoptions=Gtk.AttachOptions.FILL, xpadding=0, ypadding=0)
				self.id[question] = self.choose_recipe_comboboxtext

			elif i == 4:
				comboboxtext_4 = Gtk.ComboBoxText.new_with_entry()
				comboboxtext_4.append('ext4', "ext4")
				comboboxtext_4.append('ext3', "ext3")
				table.attach(comboboxtext_4,1, 3, top_attach, bottom_attach, xoptions=Gtk.AttachOptions.FILL ,yoptions=Gtk.AttachOptions.FILL, xpadding=0, ypadding=0)
				comboboxtext_4.connect("changed", self.on_comboboxtext_with_entry_changed, question)
				self.id[question] = comboboxtext_4

			elif i == 5:
				top_attach += 1; bottom_attach +=1
				radiobutton2 = Gtk.RadioButton(label=label_text[4], group=radiobutton1)
				table.attach(radiobutton2,0, 3, top_attach, bottom_attach, xoptions=Gtk.AttachOptions.FILL ,yoptions=Gtk.AttachOptions.FILL, xpadding=0, ypadding=0)
				radiobutton2.connect("toggled", self.on_radio_button_toggled, question)
				self.id[question] = radiobutton2

			else:
				continue

			top_attach += 1; bottom_attach +=1

		self.choose_recipe()



