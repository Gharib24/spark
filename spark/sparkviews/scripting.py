#!/usr/bin/env python

example1 = """
### example
### set hostname equal to product_name
#DEVICE_PRODUCT_NAME=`(cat /sys/devices/virtual/dmi/id/product_name | tr -d '()+-.' | tr -s '  ' | tr ' ' '-' | tr 'A-Z' 'a-z')`
#PRESEED=/tmp/preseed_for_${DEVICE_PRODUCT_NAME}.cfg
#echo "d-i netcfg/get_hostname string" ${DEVICE_PRODUCT_NAME} > $PRESEED
#debconf-set-selections $PRESEED
"""
example2 = """
### example
### change grub timeout to 1 second
#sed -i 's/GRUB_TIMEOUT=5/GRUB_TIMEOUT=1/g' /target/etc/default/grub
#in-target update-grub
"""
example={"preseed_run": example1, "preseed_late_command": example2}



import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk


class Scripting:
	def __init__(self):
		super().__init__()

	def scripting(self, question, label_text):
		name = self.naming(question)

		vbox = self.base_vbox(question)
		textview = self.base_textview(question)
		self.question_to_own_widget_object_dict[question] = textview
		scrolled_window =  self.base_scrolledwindow(question)
		vbox.pack_start(scrolled_window, True, True, 0)
		actionbar = self.base_actionbar(question)
		vbox.add(actionbar)

		textbuffer = self.widgets_object_dict.get(f"textbuffer_{name}")
		start, end = textbuffer.get_bounds()
		textbuffer.insert(end, "#!/bin/sh\n")
		textbuffer.insert(end, example.get(name))
		scrolled_window.add(textview)


		button_label_text = self.get_label_text_for_button(name)
		for counter, label_text in enumerate(button_label_text):
			button = Gtk.Button(label=label_text, name=name)
			button.question = question
			button.signal_name = 'clicked'
			button.set_property("width-request", 100)
			actionbar.pack_end(button)
			self.widget_name_space(button, counter, question)
			del button
		return vbox
