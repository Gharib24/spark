import os
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk, GLib
import threading
from sys_cmd import SysCmd

#--------------------------------------------------------------------------------------------------
class Handler(SysCmd):
	def __init__(self):
		super().__init__()

	def __call__(self): 
		pass

	def on_combo_changed_rebuild(self, combobox):
		tree_iter = combobox.get_active()
		if tree_iter is not None:
			model = combobox.get_model()
			value = model[tree_iter][0]
			if value == "Empty":
				self.label.set_text("")
				self.button.set_sensitive(False)
				self.file_chooser(self.select_iso_file_button)
			else:
				self.log.info("{}  {}".format('iso file:' ,value))
				self.label.set_text("<a href='file:///{0}'>file:{0}</a>".format(value))
				self.label.set_use_markup(True)
				self.button.set_sensitive(True)
				iso_label = self.get_iso_label(value)
				output_file_name = '{}-auto-install.iso'.format(iso_label.lower().split()[0])
				self.file_name_entry.set_text(output_file_name)

	def on_button_clicked_rebuild(self, button, data=None):
		name = button.get_label()
		if name == 'Create ISO file':
			tree_iter = self.combobox.get_active()
			model = self.combobox.get_model()
			iso_file = (model[tree_iter][0])
			filename = self.file_name_entry.get_text()

			if iso_file != 'Empty':
				if not os.path.exists(iso_file):
					self.error_dialog('Error file not found!', iso_file)
				else:
#					self.new_image(iso_file, filename)
					def lengthy_process():
						self.log.debug("{1} : {0}".format('starting', threading.current_thread().getName()))
						def start():
							self.label.set_text('Making iso file')
							watch_cursor = Gdk.Cursor(Gdk.CursorType.WATCH)
							self.button.set_sensitive(False)
							self.get_window().set_cursor(watch_cursor)
							self.spinner.start()

						GLib.idle_add(start)
						try:
		#					TODO kill thread  befor destroy
							self.new_image(iso_file, filename)
		#					import time
		#					time.sleep(5)
						except:
							def error():
								self.spinner.stop()
								self.get_window().set_cursor(None)
								self.button.set_sensitive(True)
								self.label.set_text('Error')
								self.error_dialog("Error!", 'failed successfully')
							GLib.idle_add(error)
							self.log.error("{0}".format('Error'))
							raise SystemExit()

						def done():
							self.spinner.stop()
							self.get_window().set_cursor(None)
							self.button.set_sensitive(True)

							self.label.set_text("<a href='file:///{0}'>Done: {0}{1}</a>".format(self.work_path, filename))
							self.label.set_use_markup(True)
							self.info_dialog("Done", "<a href='file:///{0}'>file: {0}{1}</a>".format(self.work_path, filename))

						GLib.idle_add(done)
						self.log.debug("{1} : {0}".format('terminated', threading.current_thread().getName()))
		#			lengthy_process()
					thread = threading.Thread(name='thread 1', target=lengthy_process).start()
#--------------------------------------------------------------------------------------------------

