import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

#--------------------------------------------------------------------------------------------------

class Menu:
	def __init__(self):
		super().__init__()
	def menu(self):
		menubar = Gtk.MenuBar()
		menu1 = Gtk.Menu()
		menu1.set_property("width-request", 200)
		file = Gtk.MenuItem.new_with_label('File')

		file.set_submenu(menu1)
		open = Gtk.MenuItem.new_with_label('Open')
		open.connect( "activate", self.file_viwe, self.preseed_file)
		save = Gtk.MenuItem.new_with_label('Save')
		save.connect( "activate",self.save_to_file, self.preseed_file)
		exit = Gtk.MenuItem.new_with_label('Exit')
		exit.connect( "activate", self.on_destroy)
		sep1 = Gtk.SeparatorMenuItem()
		sep2 = Gtk.SeparatorMenuItem()
		sep3 = Gtk.SeparatorMenuItem()
		menu1.append(open)
		menu1.append(sep1)
		menu1.append(save)
		menu1.append(sep2)
		menu1.append(exit)

		menu2 = Gtk.Menu()
		menu2.set_property("width-request", 200)
		preferences = Gtk.MenuItem.new_with_label('Preferences')
		preferences.set_submenu(menu2)

		chk1 = Gtk.CheckMenuItem.new_with_label('Right panel')
		if self.cfg.get('panel') == True:
			chk1.set_active(True)

		sep = Gtk.SeparatorMenuItem()

		chk2 = Gtk.CheckMenuItem.new_with_label('Dark theme')

		if self.cfg.get('dark') == True:
			chk2.set_active(True)

		chk1.connect( "toggled", self.on_check_button_toggled_menu)
		chk2.connect( "toggled", self.on_check_button_toggled_menu)
		menu2.append(chk1)
		menu2.append(sep)
		menu2.append(chk2)
		menubar.append(file)
		menubar.append(preferences)
		self.menubar = menubar
