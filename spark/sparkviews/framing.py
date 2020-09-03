#!/usr/bin/env python
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk


class Framing:
	def __init__(self):
		super().__init__()

	def framing(self, question, label_text):
		name = self.naming(question)

		frame = self.base_frame(question, label_text)
		vbox = self.base_vbox(question)
		scrolled_window =  self.base_scrolledwindow(question)
		vbox.pack_start(scrolled_window, True, True, 0)
		actionbar = self.base_actionbar(question)
		vbox.add(actionbar)
		frame.add(vbox)

		tree_view = self.base_treeview(question)
		tree_view.set_property("margin-top", 0)
		tree_view.set_name(self.naming(question))

		liststore = self.get_liststore_model(question)
		column_type = str(liststore.get_column_type(1)).split()[1]
		for column_number in range(0, liststore.get_n_columns()):
			if column_number > 0:
				column_type = str(liststore.get_column_type(column_number)).split()[1]
				if column_type == 'gchararray':
					column = tree_view.get_column(column_number)
					column.set_expand(True)
					cellrenderertext = column.get_cells()[0]
					cellrenderertext.set_property("editable", True)
				elif column_type == 'gboolean':
					column = tree_view.get_column(column_number)
					cellrenderertoggle = column.get_cells()[0]
		scrolled_window.add(tree_view)

		comboboxtext = self.base_comboboxtext(question, 'comboboxtext')
		comboboxtext.set_active(0)
		comboboxtext.set_property("width-request", 100)
#		comboboxtext.set_hexpand (False)
		actionbar.pack_start(comboboxtext)

		button_label_text = self.get_label_text_for_button(name)
		for counter, label_text in enumerate(button_label_text):
			button = Gtk.Button(label=label_text, name=name)
			button.question = question
			button.signal_name = 'clicked'
			button.set_property("width-request", 100)
			if counter < 1:
				actionbar.pack_start(button)
			else:
				actionbar.pack_end(button)
			self.widget_name_space(button, counter, question)
			del button
		return frame
