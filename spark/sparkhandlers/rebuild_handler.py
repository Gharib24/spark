import os
import time
import threading
import subprocess

import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk, GLib

from spark.sparkhandlers.iso_image_builder import IsoImageBuilder


class Handler(IsoImageBuilder):
	def __init__(self):
		self.job = False
		super().__init__()

	def __call__(self):
		pass

	def on_entry_changed_rebuild(self, enter):
		name = enter.get_name()
		if name =='rebuild_enter_file_name':
			self.set_config('FILE-NAME', enter.get_text())

	def on_button_clicked_rebuild(self, button):
		button_name = button.get_name()
		foldar_choose = self.widgets_object_dict.get('filechooserbutton_rebuild_select_foldar')
		file_choose = self.widgets_object_dict.get('filechooserbutton_rebuild_select_iso_file')
		entry_file_name = self.widgets_object_dict.get('entry_rebuild_enter_file_name')
		spinner = self.widgets_object_dict.get('spinner_rebuild_spinner')
		progressbar = self.widgets_object_dict.get('progressbar_rebuild_progressbar')
		progressbar.set_fraction(0.0)
#		progressbar.set_show_text(False)
		label = self.labels_object_dict.get('label_rebuild_label')

		source_iso_file = file_choose.get_filename()
		output_iso_file_name = entry_file_name.get_text()
		save_foldar = foldar_choose.get_filename()

		xorriso_exists = subprocess.getstatusoutput('xorriso')[0]
		if xorriso_exists == 127:
				self.base_message_dialog('error', 'error_xorriso')

		if source_iso_file != None and output_iso_file_name != '' and xorriso_exists == 2:
			def lengthy_process():
				self.log.debug(f"{threading.current_thread().getName()} starting")
				def start():
					self.job = True
					label.set_text('Making iso file')
					watch_cursor = Gdk.Cursor(Gdk.CursorType.WATCH)
					button.set_sensitive(False)
					self.get_window().set_cursor(watch_cursor)
					spinner.start()
					progressbar.show()
				GLib.idle_add(start)
				try:
		#			TODO kill thread  befor destroy
					time.sleep(2)
					self.make_new_image(source_iso_file, f"{save_foldar}/{output_iso_file_name}")
					time.sleep(2)
				except Exception as exception:
					def error():
						spinner.stop()
						self.get_window().set_cursor(None)
						button.set_sensitive(True)
						label.set_text('Error!')
						self.base_message_dialog("error", 'error')
						self.job = False

					GLib.idle_add(error)
					self.log.error(exception)
					raise SystemExit()

				def done():
					spinner.stop()
					progressbar.hide()
					self.get_window().set_cursor(None)
					button.set_sensitive(True)
					if self.exitcode == 0:
						label.set_text(f"<a href='file:///{save_foldar}'>File: {save_foldar}/{output_iso_file_name}</a>")
						label.set_use_markup(True)
					else:
						label.set_text(f'Error exitcode: {self.exitcode}')
#					self.base_message_dialog('info', 'iso_file_done', f"{save_foldar}/{output_iso_file_name}")
					self.job = False
				GLib.idle_add(done)
				self.log.debug(f"{threading.current_thread().getName()} terminated")

			#lengthy_process()
			thread = threading.Thread(name='thread 1', target=lengthy_process).start()

	def check_if_supported(self, filechoos):
		DVD_1_amd64_id_label = tuple(f"Debian 10.{i}.0 amd64 1" for i in range(0, 10))
		CD_netinst_amd64_id_label = tuple(f"Debian 10.{i}.0 amd64 n" for i in range(0, 10))
		all_iso_id_label_supported = DVD_1_amd64_id_label+CD_netinst_amd64_id_label

		id_label = self.get_iso_label(filechoos)

		if id_label in all_iso_id_label_supported:
			return True
		else:
			return False

	def on_filechooserbutton_file_set_rebuild(self, filechooserbutton):
		filechoos = filechooserbutton.get_filename()
#		self.log.debug(filechoos)
		name = filechooserbutton.get_name()
		if name == "rebuild_select_iso_file":
			if self.check_if_supported(filechoos):
				entry_file_name = self.widgets_object_dict.get('entry_rebuild_enter_file_name')
				entry_file_name.set_text(f"automated-installs-{os.path.basename(filechoos)}")
				self.set_config('FILE-CHOOSE', filechoos)
			else:
				filechooserbutton.unselect_all()
				self.base_message_dialog("error", 'unsupported')
		elif name == "rebuild_select_foldar":
			self.set_config('FOLDAR-CHOOSE', filechoos)




















