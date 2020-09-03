#!/usr/bin/env python
import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gio


class HeaderBar:
	def __init__(self):
		pass
	def header_bar(self):
		headerbar = Gtk.HeaderBar()
		headerbar.set_show_close_button(True)
		headerbar.props.title = self.settings.APP_NAME
		headerbar.set_border_width(0)

		menubutton = Gtk.MenuButton()
		icon = Gio.ThemedIcon(name="open-menu-symbolic")
		image = Gtk.Image.new_from_gicon(icon, Gtk.IconSize.MENU)
		menubutton.add(image)
		headerbar.pack_end(menubutton)

		menu = Gtk.Menu()
		menubutton.set_popup(menu)
		menu.set_property("width-request", 170)

		label_text = ('Open preseed file','Create an ISO file', 'Preferences', 'Help', 'About', 'Quit')
		for counter, text in enumerate(label_text):
			menuitem = Gtk.MenuItem.new_with_label(label=text)
			menuitem.name = self.naming(text)
			menu.append(menuitem)
			if counter < (len(label_text)-1):
				separator = Gtk.SeparatorMenuItem()
				menu.append(separator)
			menuitem.connect( "activate", self.on_menuitem_activate)
		menu.show_all()

		button = Gtk.Button("Save")
		button.set_name('save')
		button.connect('clicked', self.on_button_clicked_main)
		headerbar.pack_end(button)

		box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
		Gtk.StyleContext.add_class(box.get_style_context(), "linked")

		button = Gtk.Button()
		button.add(Gtk.Arrow(arrow_type=Gtk.ArrowType.LEFT, shadow_type=Gtk.ShadowType.NONE))
		button.set_name('previous')
		box.add(button)
		button.connect('clicked', self.on_button_go_clicked_main)

		button = Gtk.Button()
		button.add(Gtk.Arrow(arrow_type=Gtk.ArrowType.RIGHT, shadow_type=Gtk.ShadowType.NONE))
		button.set_name('next')
		box.add(button)
		button.connect('clicked', self.on_button_go_clicked_main)

		headerbar.pack_start(box)

		if self.debug:
			icons_name = ("document-save-symbolic", "media-optical-symbolic", "view-refresh-symbolic", "document-open-symbolic")
			button_name = ('save','create', 'reload', 'open')
			for counter, (icon, name) in enumerate(zip(icons_name, button_name)):
				icon = Gio.ThemedIcon(name=icon)
				image = Gtk.Image.new_from_gicon(icon, Gtk.IconSize.BUTTON)
				button = Gtk.Button()
				button.add(image)
				button.set_name(name)
				headerbar.pack_end(button)
				button.connect('clicked', self.on_button_clicked_main)

		return headerbar






