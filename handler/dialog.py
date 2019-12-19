import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

class Dialog:
	def __init__(self):
		super().__init__()

	def file_chooser(self, caller):
		label_text = caller.get_label()
		dialog = Gtk.FileChooserDialog(label_text, self,
			Gtk.FileChooserAction.OPEN,
			(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
			Gtk.STOCK_OPEN, Gtk.ResponseType.OK))
		dialog.set_default_size(800, 400)
		dialog.set_modal(True)
		filter = Gtk.FileFilter()
		filter.set_name("Disc Image")
		filter.add_pattern("*.iso")
		dialog.add_filter(filter)
		dialog.connect("response", self.on_file_chooser_dialog)
		response = dialog.run()

	def file_viwe(self, caller, file):
		label_text = caller.get_label()
		title = self.get_title()
		dialog = Gtk.Dialog(None, self, Gtk.DialogFlags.MODAL, (Gtk.STOCK_SAVE, Gtk.ResponseType.APPLY, Gtk.STOCK_CLOSE, Gtk.ResponseType.CLOSE))
		dialog.set_title(title+': file '+file)
		width = (self.get_size()[0] - 50)
		height = (self.get_size()[1] - 50)
		dialog.set_default_size(width, height)
		dialog.set_border_width(5)
		dialog.set_modal(False)
		scrolled_window = Gtk.ScrolledWindow()
		scrolled_window.set_policy(Gtk.PolicyType.ALWAYS, Gtk.PolicyType.AUTOMATIC)
		scrolled_window.set_border_width(0)
		self.file_buffer = Gtk.TextBuffer()
		textview = Gtk.TextView(buffer = self.file_buffer)
		textview.set_border_width(0)
		scrolled_window.add(textview)
		textview.set_cursor_visible(True)
		textview.set_editable(True)
		textview.set_wrap_mode(Gtk.WrapMode.WORD)
		self.file = file
		f = open(file, "r")
		start, end = self.file_buffer.get_bounds()
		self.file_buffer.insert(start,f.read())
		f.close() 

		box = dialog.get_content_area()
		box.pack_end(scrolled_window, True, True, 5)
		dialog.connect("response", self.on_file_viwe_dialog)
		dialog.show_all()

	def info_dialog(self, info_title, info_message):
		dialog = Gtk.MessageDialog(self, Gtk.MessageType.INFO, 0, Gtk.ButtonsType.OK, info_title)
		dialog.format_secondary_markup(info_message)
		dialog.set_default_size(400, 100)
		dialog.connect("response", self.on_destroy_dialog)
		dialog.run()

	def error_dialog(self, error_title, error_message):
		dialog = Gtk.MessageDialog(self, 0, Gtk.MessageType.ERROR,
			Gtk.ButtonsType.CANCEL, error_title)
		dialog.format_secondary_text(error_message)
		dialog.set_default_size(400, 100)
		dialog.connect("response", self.on_destroy_dialog)
		dialog.run()

	def question_dialog(self, question_title, question_message, data=None):
		dialog = Gtk.MessageDialog(self, 0, Gtk.MessageType.QUESTION,
			Gtk.ButtonsType.YES_NO, question_title)
		dialog.format_secondary_text(question_message)
		dialog.set_default_size(400, 100)
		dialog.connect("response", self.on_question_dialog, data)
		dialog.run()







