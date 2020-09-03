import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk


class Handler:
	def __init__(self):
		super().__init__()

	def on_message_dialog_response(self, dialog, response):
		if response == Gtk.ResponseType.YES:
			name = dialog.get_name()
			if name =='load_values':
#				self.get_value_from_preseed_file()
				self.return_widgets_field_value()
			elif name =='save_entered':
				self.save_preseed_file()

		elif response in [Gtk.ResponseType.NO, Gtk.ResponseType.CANCEL, Gtk.ResponseType.OK]:
			name = dialog.get_name()
			if name =='save_entered':
				self.get_application().quit()
			self.on_destroy_dialog(dialog, response)
		self.on_destroy_dialog(dialog, response)

	def on_dialog_response(self, dialog, response):
		if response == Gtk.ResponseType.APPLY:
			textbuffer = self.widgets_object_dict.get("textbuffer_preseed_file_viwe_diaog")
			start, end = textbuffer.get_bounds()
			text = textbuffer.get_text(start, end, include_hidden_chars = False)
			f = open(self.settings.PRESEED_FILE, "w")
			f.write(text)
			f.close()
			self.base_message_dialog('info', 'save_preseed', self.settings.PRESEED_FILE)
		elif response == Gtk.ResponseType.CLOSE:
			self.on_destroy_dialog(dialog, response)
#		self.on_destroy_dialog(dialog, response)

	def on_destroy_dialog(self, dialog, response):
		dialog.destroy()

	def on_file_chooser_dialog(self, dialog, response):
		if response == Gtk.ResponseType.OK:
			iso_file = dialog.get_filename()
			self.set_iso_file(iso_file)
			self.on_destroy_dialog(dialog, response)

		elif response == Gtk.ResponseType.CANCEL:
			self.on_destroy_dialog(dialog, response)






