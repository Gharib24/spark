import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
#--------------------------------------------------------------------------------------------------
class Handler:
	def __init__(self):
		super().__init__()

	def on_file_chooser_dialog(self, widget, response):
		global iso_file 
		if response == Gtk.ResponseType.OK:

			iso_file =  widget.get_filename()
			iso_label = self.get_iso_label(iso_file)
			self.log.debug(iso_label)

#			if "Ubuntu" in iso_label:
			if "Debian" in iso_label:
				for i in range(len(self.file_liststore)):
					text = self.file_liststore[i][0]
					if text == iso_file:
						in_liststore = True
						path = Gtk.TreePath(i)
						treeiter = self.file_liststore.get_iter(path)
						root_iter = self.file_liststore.get_iter_first()
						break
					else:
						in_liststore = False

				if in_liststore  == True:
					self.file_liststore.move_before(treeiter, root_iter)
					self.combobox.set_active(0)

				elif in_liststore  == False:
					iter = self.file_liststore.prepend([iso_file])
					self.combobox.set_active(0)
					if len(self.file_liststore) > 5:
						path = Gtk.TreePath(4)
						treeiter = self.file_liststore.get_iter(path)
						self.file_liststore.remove(treeiter) # remove 1 befor Empty
				files_lst = []
				for i in range(len(self.file_liststore)):
					files_lst.append(self.file_liststore[i][0])
				v = ' '.join(files_lst)
				self.cfg.write('file', v)
				self.on_destroy_dialog(widget, response)
			else:
				self.on_destroy_dialog(widget, response)
				self.label.set_text("Unsupported! {0}".format(iso_label))
				self.button.set_sensitive(False)
				self.error_dialog("Unsupported!", iso_label)

		elif response == Gtk.ResponseType.CANCEL:
			self.on_destroy_dialog(widget, response)


	def on_file_viwe_dialog(self, widget, response):
		if response == Gtk.ResponseType.APPLY:
			self.on_text_changed(self.file_buffer, file=self.preseed_file)
			self.on_destroy_dialog(widget, response)

		elif response == Gtk.ResponseType.CLOSE:
			self.on_destroy_dialog(widget, response)


	def on_question_dialog(self, widget, response, data=None):
		if response == Gtk.ResponseType.YES:
			if data == 'load':
				self.on_destroy_dialog(widget, response)
				self.return_value()

			elif data == 'unsaved':
				self.on_destroy_dialog(widget, response)
				self.save_to_file(widget, self.preseed_file)

		elif response == Gtk.ResponseType.NO:
			self.on_destroy_dialog(widget, response)

	def on_destroy_dialog(self, widget, response):
		widget.destroy()



