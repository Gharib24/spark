import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

#--------------------------------------------------------------------------------------------------

class PartitionRecipe(object):
	def __init__(self,):
		super().__init__()

	def choose_recipe(self):
		vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
		self.partitionrecipe_frame.add(vbox)

		fstype = ["ext4", "ext3", "ext2", "linux-swap", "fat32", "free"]
		mount_point = ["/", "/home", "/boot", "/boot/efi", "/mnt/storage"]

#		self.data_store = Gtk.ListStore(str, str)
#		for row0, row1 in zip(fstype, mount_point):
#			self.data_store.append([row0, row1])

		fstype_store =  Gtk.ListStore(str)
		for i, fs in enumerate(fstype, 0):
			fstype_store.append([fs])

		mount_point_store =  Gtk.ListStore(str)
		for i, mp in enumerate(mount_point, 0):
			mount_point_store.append([mp])

		list = [fstype_store, mount_point_store]

		self.recipe_store = Gtk.ListStore(str, str, str, str, str, str, str,)

		scrolled_window = Gtk.ScrolledWindow()
		scrolled_window.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
		scrolled_window.set_border_width(0)
		vbox.pack_start(scrolled_window, True, True, 0)

		view_p = Gtk.TreeView(model=self.recipe_store)
		view_p.set_hexpand (True)
		view_p.set_vexpand (True)
		view_p.set_grid_lines(True)
		view_p.set_grid_lines(1)
		scrolled_window.add(view_p)

		self.view_p_selection = view_p.get_selection()
		self.view_p_selection.connect("changed", self.on_view_selection_changed_partition)

		renderer = Gtk.CellRendererText()
		renderer.set_fixed_size(width=100, height=30)
		column = Gtk.TreeViewColumn('Part number', renderer, text=0)
		column.set_min_width(100)
		column.set_reorderable(True)
		column.set_expand(True)
		view_p.append_column(column)

		for col, titles in enumerate([ 'Fstype', 'Mount point'], 1):
			renderer_combo = Gtk.CellRendererCombo()
			self.renderer_combo = renderer_combo
			renderer_combo.set_fixed_size(width=100, height=30)
			renderer_combo.set_property("editable", True)
			renderer_combo.set_property("text-column", 0)
			renderer_combo.set_property("has-entry", True)
			renderer_combo.set_property("model", list[col - 1] )
			renderer_combo.connect("edited", self.on_combo_changed_partition, col)
			column_combo = Gtk.TreeViewColumn(titles, renderer_combo, text=col)
			column_combo.set_min_width(100)
			column_combo.set_reorderable(True)
			column_combo.set_expand(True)
			view_p.append_column(column_combo)

		for col, titles in enumerate(['Min Size (MB)', 'Priority Size (MB)', 'Max Size (MB) ','Label'], col+1):
			renderer_editabletext = Gtk.CellRendererText()
			renderer_editabletext.set_fixed_size(width=100, height=30)
			renderer_editabletext.set_property("editable", True)
			renderer_editabletext.connect("edited", self.text_edited_partition, col)
			column_editabletext = Gtk.TreeViewColumn(titles, renderer_editabletext, text=col)
			column_editabletext.set_min_width(100)
			column_editabletext.set_reorderable(True)
			column_editabletext.set_expand(True)

			view_p.append_column(column_editabletext)

		actionbar = Gtk.ActionBar()
		actionbar.set_hexpand(True)
		vbox.add(actionbar)

		self.add_p = Gtk.Button(label="Add")
		self.add_p.set_property("width-request", 100)
		actionbar.pack_start(self.add_p)
		self.add_p.connect("clicked", self.on_button_clicked_partition)

		self.text_completed =[
				[['Empty'], [None,None,None,None,None,None]],
				[['BIOS Boot Partition'], ['free','N/A', '1','1','1', 'N/A']],
				[['EFI System Partition'], ['fat32','/boot/efi', '537','537','537', 'ESP']],
				[['Swap Partition'], ['linux-swap','N/A', '50%','100%','100%', 'N/A']],
				[['Boot Partition'], ['ext4','/boot', '250','500','1000', 'boot']],
				[['Root Partition'], ['ext4','/', '10000','20000','30000', 'root']],
				[['Home Partition'], ['ext4','/home', '4000','8000','16000', 'home']],
				]

		self.comboboxtext_add_p  = Gtk.ComboBoxText()
		for i, text in enumerate(self.text_completed, 0):
			self.comboboxtext_add_p.append_text(''.join(text[0]))
		self.comboboxtext_add_p.set_active(0)
		self.comboboxtext_add_p.set_property("width-request", 100)
		actionbar.pack_start(self.comboboxtext_add_p)
		self.comboboxtext_add_p.connect("changed", self.on_comboboxtext_changed_partition)

		self.remove_p = Gtk.Button(label="Remove")
		self.remove_p.set_property("width-request", 100)
		self.remove_p.set_sensitive(False)
		actionbar.pack_end(self.remove_p)
		self.remove_p.connect("clicked", self.on_button_clicked_partition)

		self.remove_all_p = Gtk.Button(label="Remove All")
		self.remove_all_p.set_property("width-request", 100)
		actionbar.pack_end(self.remove_all_p)
		self.remove_all_p.connect("clicked", self.on_button_clicked_partition)
		self.remove_all_p.connect("clicked", self.on_button_clicked_partition)

