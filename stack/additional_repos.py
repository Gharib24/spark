import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

#--------------------------------------------------------------------------------------------------

class AdditionalRepos:
	def __init__(self):
		super().__init__()

	def repos(self):
		self.vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
		self.vbox.set_border_width(0)

		scrolledwindow = Gtk.ScrolledWindow()
		scrolledwindow.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.ALWAYS)
		self.vbox.add(scrolledwindow)

		self.repos_store = Gtk.ListStore(str, str, str, str, bool)

		view = Gtk.TreeView(model=self.repos_store)
		scrolledwindow.add(view)
		view.set_hexpand (True)
		view.set_vexpand (True)
		view.set_grid_lines(True)
		view.set_grid_lines(1)
		self.view_selection_r = view.get_selection()
		self.view_selection_r.connect("changed", self.on_view_selection_changed_repos)
		renderer = Gtk.CellRendererText()
		renderer.set_fixed_size(width=20, height=30)
		column = Gtk.TreeViewColumn('Repos num', renderer, text=0)
		column.set_min_width(20)
		column.set_reorderable(False)
		column.set_expand(False)
		view.append_column(column)

		for col, titles in enumerate(['Repositories ', 'Public key URL', 'Comment'], 1):
			renderer_editabletext = Gtk.CellRendererText()
			renderer_editabletext.set_fixed_size(100, height=30)
			renderer_editabletext.set_property("editable", True)
			renderer_editabletext.connect("edited", self.text_edited_repos, col) 
			column_editabletext = Gtk.TreeViewColumn(titles, renderer_editabletext, text=col)
			column_editabletext.set_min_width(100)
			column_editabletext.set_reorderable(True)
			column_editabletext.set_expand(True)
			column_editabletext.set_resizable(True)
			view.append_column(column_editabletext)

		renderer_toggle = Gtk.CellRendererToggle(xalign=0.05 , yalign=0)
		renderer_toggle.connect("toggled", self.on_cell_toggled_repos)
		column_toggle = Gtk.TreeViewColumn("Enable deb-src", renderer_toggle, active=4)
		column_toggle.set_min_width(5)
		column_toggle.set_reorderable(False)
		view.append_column(column_toggle)

		actionbar = Gtk.ActionBar()
		actionbar.set_hexpand(True)
		self.vbox.add(actionbar)

		self.add_r = Gtk.Button(label="Add")
		self.add_r.set_property("width-request", 100)
		actionbar.pack_start(self.add_r)
		self.add_r.connect("clicked", self.on_button_clicked_repos)

		local_repos = [[['Empty'], [None, None, None, False]]]

		third_party__repos = [
					[['VirtualBox repository'], ['deb [ arch=amd64 ] http://download.virtualbox.org/virtualbox/debian buster contrib',
									'https://www.virtualbox.org/download/oracle_vbox_2016.asc',
									'VirtualBox',False]],
					[['Google repository'], ['deb [ arch=amd64 ] http://dl.google.com/linux/chrome/deb/ stable main',
									'http://dl.google.com/linux/linux_signing_key.pub',
									'Google Chrome Browser',False]]
					]

		self.local_repos = local_repos + third_party__repos

		self.comboboxtext_add_r  = Gtk.ComboBoxText()
		for i, text in enumerate(self.local_repos, 0):
			self.comboboxtext_add_r.append_text(''.join(text[0]))
		self.comboboxtext_add_r.set_active(0)
		self.comboboxtext_add_r.set_property("width-request", 100)
		actionbar.pack_start(self.comboboxtext_add_r)
		self.comboboxtext_add_r.connect("changed", self.on_comboboxtext_changed_repos)

		self.remove_r = Gtk.Button(label="Remove")
		self.remove_r.set_property("width-request", 100)
		self.remove_r.set_sensitive(False)
		actionbar.pack_end(self.remove_r)
		self.remove_r.connect("clicked", self.on_button_clicked_repos)

		self.remove_all_r = Gtk.Button(label="Remove All")
		self.remove_all_r.set_property("width-request", 100)
		actionbar.pack_end(self.remove_all_r)
		self.remove_all_r.connect("clicked", self.on_button_clicked_repos)
		self.remove_all_r.connect("clicked", self.on_button_clicked_repos)

