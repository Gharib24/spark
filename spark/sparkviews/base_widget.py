#!/usr/bin/env python
import os

import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GObject

from spark.sparkothers.widget_value import WidgetValue


class BaseWidget(WidgetValue):
	def __init__(self):
		super().__init__()
		self.completion_name = ('fullname', 'username', 'hostname',
								'domain','ipaddress', 'netmask', 'gateway',
								'nameservers', 'groups')

	def get_liststore_model(self, question):
		name = self.naming(question)
		liststore_name = f"liststore_{name}"

		if self.widgets_object_dict.get(liststore_name) == None:
			thislist = self.get_list_for_liststore_model(name)
			if name == 'debian_installer_locale':
				liststore = Gtk.ListStore(str)
				for i, locale in enumerate(thislist, 0):
					liststore.append(locale)

			elif name == 'localechooser_supported_locales':
				liststore = Gtk.ListStore(bool, str)
				for i, locale in  enumerate(thislist, 0):
					liststore.append([False, locale[0]])

			elif name == 'keyboard_configuration_xkb_keymap':
				liststore = Gtk.ListStore(str, str)
				for item in thislist:
					liststore.append(item)
			elif name == 'time_zone':
				liststore = Gtk.ListStore(str)
				for item in thislist:
					liststore.append([item])

			elif name == 'partman_auto_expert_recipe':
				liststore = Gtk.ListStore(str, str, str, str, str, str, str,)

			elif name == 'apt_setup_local0_repository':
				liststore = Gtk.ListStore(str, str, str, str, bool)
#
			elif name == 'tasksel_first':
				liststore = Gtk.ListStore(bool, str)
				for i, tasksel_name in  enumerate(thislist, 0):
					liststore.append([False, tasksel_name[0]])

			elif name in self.completion_name:
				liststore = Gtk.ListStore(str)
				for completion_text in thislist:
					liststore.append([completion_text])
#			else:
#				liststore = Gtk.ListStore(str, str)

			try:
				liststore.question = question
				self.widget_name_space(liststore, name)
				self.question_to_own_widget_object_dict[question] = liststore
				return liststore
			except NameError:
				self.log.error(self.whoami(), NameError ,liststore_name)
			finally:
				liststore.set_name(name)
				if 'thislist' in locals():
					del thislist
				del liststore
		else:
			try:
				liststore = self.widgets_object_dict.get(liststore_name)
				return liststore
			except KeyError:
				self.log.error(self.whoami(), KeyError ,liststore_name)

#-------------------------------------------------------------------------------

	def base_entry(self, question):
		name = self.naming(question)

		entry = Gtk.Entry(placeholder_text=None, name=name)
		if name.split('_')[-1] in self.completion_name:
			model = self.get_liststore_model(name.split('_')[-1])
			entrycompletion = Gtk.EntryCompletion()
			entrycompletion.set_model(model)
			entrycompletion.set_text_column(0)
#			entrycompletion.set_popup_completion(True)
#			entrycompletion.set_inline_completion(False)
			entry.set_completion(entrycompletion)

		entry.set_hexpand(True)
		entry.set_activates_default(True)
		if 'password' in question:
			entry.set_visibility(False)
			entry.set_invisible_char("*")
		entry.signal_name = 'changed'
		entry.question = question
		self.widget_name_space(entry, question)
		return entry
#-------------------------------------------------------------------------------

	def base_checkbutton(self, question, label_text):
		name = self.naming(question)
		checkbutton = Gtk.CheckButton(label=label_text , xalign=0, yalign=0.5, name=name)
		checkbutton.signal_name = 'toggled'
		checkbutton.question = question
		self.widget_name_space(checkbutton, question)
		return checkbutton

#-------------------------------------------------------------------------------

	def base_comboboxtext(self, question, widget_type):
		name = self.naming(question)
		if widget_type == 'comboboxtext_with_entry':
			with_entry = True
		else:
			with_entry = False
#		comboboxtext = Gtk.ComboBoxText.new_with_entry()
		comboboxtext = Gtk.ComboBoxText(has_entry=with_entry)
		comboboxtext.set_name(name)
		comboboxtext.set_hexpand(True)
		comboboxtext.set_vexpand(False)
		comboboxtext.set_entry_text_column(0)

		for value in self.get_value_for_comboboxtext(name):
			comboboxtext.append(value[0], value[1])
		comboboxtext.signal_name = 'changed'
		comboboxtext.question = question
		self.widget_name_space(comboboxtext, question)
		return comboboxtext

#-------------------------------------------------------------------------------

	def base_combobox(self, question):
		name = self.naming(question)
		liststore = self.get_liststore_model(question)
		if liststore.get_n_columns() == 1:
			text = 0
		else:
			text = 1

		combobox = Gtk.ComboBox(name=name, model=liststore, has_entry=True)
		combobox.set_model(liststore)
		combobox.set_hexpand (True)
		combobox.set_vexpand (False)
		combobox.set_wrap_width(1)
		combobox.set_entry_text_column(text)
		combobox.set_popup_fixed_width(True)
		combobox.signal_name = 'changed'
		combobox.question = question
		self.widget_name_space(combobox, question)

		entry_completion = Gtk.EntryCompletion()
#		entry_completion.set_popup_completion(True)
#		entry_completion.set_inline_completion(True)
		entry_completion.set_model(combobox.get_model())
		entry_completion.set_text_column(text)
		entry_completion.question = question
		entry_completion.signal_name = 'match-selected'
		self.widget_name_space(entry_completion, question)

		combobox.get_child().set_completion(entry_completion)

#		cellrenderertext = Gtk.CellRendererText()
#		cellrenderertext.set_fixed_size(width=300, height=20)
#		combobox.pack_start(cellrenderertext, True)
#		combobox.add_attribute(cellrenderertext, "text", text)
		return combobox

#-------------------------------------------------------------------------------

	def base_treeview(self, question):
		name = self.naming(question)

		model = self.get_liststore_model(question)
		column_type = str(model.get_column_type(1)).split()[1]

		treeview = Gtk.TreeView(model=model ,name=name,)
		treeview.question = question
		treeview.set_headers_visible(True)
		treeview.set_hexpand (True)
		treeview.set_vexpand (True)
		treeview.set_grid_lines(3) #GTK_treeview_GRID_LINES_BOTH
		treeview.set_enable_search(False)
		self.widget_name_space(treeview, question)

		treeview_selection = treeview.get_selection()
		treeview_selection.signal_name = 'changed'
		treeview_selection.question=question
		self.widget_name_space(treeview_selection, question)
		del treeview_selection

		title = self.get_title_for_treeview(name)
		for column_number in range(0, model.get_n_columns()):
			column_type = str(model.get_column_type(column_number)).split()[1]
#			print(title[column_number])
			if column_type == 'gboolean':
				cellrenderertoggle = Gtk.CellRendererToggle(xalign=0.0, yalign=0.0)
				column = Gtk.TreeViewColumn(title[column_number], cellrenderertoggle, active=column_number)
				cellrenderertoggle.question = question
				cellrenderertoggle.signal_name = 'toggled'
				cellrenderertoggle.column_number = column_number
				cellrenderertoggle.list = []
				self.widget_name_space(cellrenderertoggle, column_number, question)
				treeview.append_column(column)

			if column_type == 'gchararray':
				cellrenderertext = Gtk.CellRendererText()
				cellrenderertext.signal_name = 'edited'
				cellrenderertext.question = question
				cellrenderertext.column_number = column_number
#		#		cellrenderertext.set_fixed_size(250, height=30)
				cellrenderertext.set_alignment(xalign=0.0, yalign=0.0)
				column = Gtk.TreeViewColumn(title[column_number], cellrenderertext, text=column_number)
				self.widget_name_space(cellrenderertext, column_number, question)
				treeview.append_column(column)
		return treeview

#-------------------------------------------------------------------------------

	def base_textview(self, question):
		name = self.naming(question)
		textbuffer = Gtk.TextBuffer()
		textbuffer.signal_name = "changed"
		textbuffer.question = question
		textbuffer.set_text('')
		textview = Gtk.TextView(buffer=textbuffer)
		textview.set_wrap_mode(Gtk.WrapMode.WORD)
		textview.set_cursor_visible(True)
		textview.set_editable(True)
		self.widget_name_space(textbuffer, question)
		return textview

#-------------------------------------------------------------------------------

	def base_button(self, question, label_text):
		name = self.naming(question)
		button = Gtk.Button(label=label_text, name=name)
		button.question = question
		button.signal_name = 'clicked'
		button.set_vexpand (False)
#		button.set_property("width-request", 100)
		self.widget_name_space(button, question)
		return button

#-------------------------------------------------------------------------------

	def base_label(self, question, label_text):
		name = self.naming(question)
		label = Gtk.Label(label_text, xalign=0, yalign=0.4, name=name)
		self.widget_name_space(label, question)
		return label

#-------------------------------------------------------------------------------

#	def base_label(self, question, label_text):
#		name = self.naming(question)
#		label = Gtk.Label(label_text, xalign=0, yalign=0.4, name=name)
#		self.widget_name_space(label, question)
#		return label

#-------------------------------------------------------------------------------

	def base_separator(self):
		separator = Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL)
		separator.set_hexpand(True)
		return separator

#-------------------------------------------------------------------------------

	def base_spinner(self, question):
		name = self.naming(question)
		spinner = Gtk.Spinner()
#		spinner = Gtk.Spinner(height_request=50, width_request=50, name=name)
#		spinner.set_hexpand(True)
#		spinner.set_vexpand(True)
		spinner.question = question
		self.widget_name_space(spinner, question)
		return spinner

#-------------------------------------------------------------------------------

	def base_progressbar(self, question, label_text):
		progressbar = Gtk.ProgressBar(margin_bottom=5, margin_top=0, margin_left=5, margin_right=5)
		progressbar.set_show_text(True)
		self.widget_name_space(progressbar, question)
		return progressbar

#-------------------------------------------------------------------------------

	def base_filechooserbutton(self, question, label_text):
		name = self.naming(question)
		filechooserbutton_type = question.split('-')[-1:]

		filechooserbutton = Gtk.FileChooserButton(name=name)
		filechooserbutton.set_title(label_text)
		filechooserbutton.signal_name = "file-set"
		filechooserbutton.question = question
		filechooserbutton.set_current_folder(os.path.expanduser('~/Documents'))
		if "foldar" in filechooserbutton_type:
			filechooserbutton.set_action(Gtk.FileChooserAction.SELECT_FOLDER)
			filechooserbutton.set_create_folders(True)
		elif "file" in filechooserbutton_type:
			filechooserbutton.set_action(Gtk.FileChooserAction.OPEN)
			filter = Gtk.FileFilter()
			filter.set_name("Disc Image")
			filter.add_pattern("*.iso")
			filechooserbutton.add_filter(filter)
		self.widget_name_space(filechooserbutton, question)
		return filechooserbutton

#-------------------------------------------------------------------------------

