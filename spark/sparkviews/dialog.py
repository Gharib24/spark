import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GdkPixbuf

from spark.sparkhandlers.dialog_handler import Handler as DialogHandler


class Dialog(DialogHandler):
	def __init__(self):
		super().__init__()

	def get_dialog_content(self, name, data=None):
		file_href = (f"<a href='file://{data}'>file: {data}</a>",)
		saved = ('Saved Successfully',)
		load_values = ('Load fields values', 'Load fields values from last session')
		save_preseed = save_pre_script = save_post_script = saved + file_href
		def s_field(field):
			if field >= 2:
				return 'fields'
			else:
				return 'field'
		field = s_field(self.count_answered_question())
		save_entered = ('Save entered data?', f'{self.count_answered_question()} {field} unsaved')
		iso_file_done = ('Done',) + file_href
		error = ("Error!", 'failed successfully')
		error_xorriso = ("Error!", 'The required dependency xorriso is not installed.\ntry: apt-get install xorriso')
		unsupported = ("Error!", 'The file Unsupported!')
		oops = ("Oops!", 'This options not available yet.')

		try:
			data = locals()[name]
			return data
		except NameError:
			log.error(self.whoami(), NameError, name)
		except KeyError:
			log.error(self.whoami(), KeyError, name)
		finally:
			del locals()[name]

	def preseed_file_viwe_diaog(self):
		dialog = Gtk.Dialog(None, self, Gtk.DialogFlags.MODAL, (Gtk.STOCK_SAVE, Gtk.ResponseType.APPLY, Gtk.STOCK_CLOSE, Gtk.ResponseType.CLOSE))
		self.dialog = dialog
		dialog.set_title(f"{self.get_title()}: file {self.settings.PRESEED_FILE}")
		width = (self.get_size()[0] - 50)
		height = (self.get_size()[1] - 50)
		dialog.set_default_size(width, height)
		dialog.set_border_width(5)
		dialog.set_modal(False)
		scrolledwindow = self.base_scrolledwindow(self.whoami())
		textview = self.base_textview(self.whoami())
		scrolledwindow.add(textview)
		textbuffer = self.widgets_object_dict.get(f"textbuffer_{self.whoami()}")

		f = open(self.settings.PRESEED_FILE, "r")
		start, end = textbuffer.get_bounds()
		textbuffer.insert(start,f.read())
		f.close()

		box = dialog.get_content_area()
		box.pack_end(scrolledwindow, True, True, 5)
		dialog.connect("response", self.on_dialog_response)
		dialog.show_all()

	def base_message_dialog(self, messagetype, name, data=None):
		dialog_content = self.get_dialog_content(name, data)
		dialog_title = dialog_content[0]
		dialog_message = dialog_content[1]

		if messagetype == "question":
			message_type = Gtk.MessageType.QUESTION
			buttons_type = Gtk.ButtonsType.YES_NO
		elif messagetype == "info":
			message_type = Gtk.MessageType.INFO
			buttons_type = Gtk.ButtonsType.OK
		elif messagetype == "error":
			message_type = Gtk.MessageType.ERROR
			buttons_type = Gtk.ButtonsType.CANCEL

		if hasattr(self, 'dialog'):
			parent = self.dialog
		else:
			parent = self

		dialog = Gtk.MessageDialog(parent, 0, message_type, buttons_type, dialog_title)
#		dialog.format_secondary_text(dialog_message)
		if len(dialog_message.split('\n')) >= 2:
				dialog.set_title(dialog_title)
				message = dialog_message.split('\n')[0]
				dialog.set_markup(f"<span size='12000'><b>{message}</b></span>")
				dialog.format_secondary_text(dialog_message.split('\n')[1])
		else:
			dialog.format_secondary_markup(dialog_message)
		dialog.set_default_size(width=450, height=170)
		dialog.set_name(name)
		dialog.connect("response", self.on_message_dialog_response)
		dialog.run()

	def about_dialog(self):
#		logo = GdkPixbuf.Pixbuf.new_from_file_at_size(self.settings.APP_ICON, 64, 64)
		logo = Gtk.IconTheme.get_default().load_icon('non-starred', 64, 0)
		dialog = Gtk.AboutDialog(None, self, Gtk.DialogFlags.MODAL)
#		dialog.set_default_size(500, 309)
		dialog.set_modal(True)
		dialog.set_logo(logo)

		dialog.set_program_name(self.settings.APP_NAME)
		dialog.set_version(self.settings.APP_VERSION)
		dialog.set_authors(["AG"])
		dialog.set_artists(["None"])
		dialog.set_documenters(['None'])
		dialog.set_comments(self.settings.APP_DESCRIPTION) # 'support Debian 10.X.X buster CD/DVD image, live image UNSUPPORTED
		dialog.set_website("https://spark.com/")
		dialog.set_website_label(f"{self.settings.APP_NAME} Website")
		dialog.set_copyright('Copyright 2018-2020 The Spark team')
		dialog.set_license_type(Gtk.License(3))
		dialog.connect('response', self.on_destroy_dialog)
		dialog.show_all()

	def iso_image_builder_diaog(self):
		self.static_data.category.append(("Create an ISO image"))
		key = self.static_data.dialog_components.keys()
		name = tuple(key)[0]

		dialog = Gtk.Dialog(None, self, Gtk.DialogFlags.MODAL)
		self.dialog = dialog
		dialog.set_title(name)
		dialog.set_name(self.naming('dialog', name))
		dialog.set_default_size(width=750, height=300)
		dialog.set_resizable(False)
		dialog.set_border_width(5)
		dialog.set_modal(True)
		box = dialog.get_content_area()
		grid = self.base_grid(name)
		self.widgets_parking(self.static_data.dialog_components)
		box.add(grid)
		dialog.hide_on_delete()
		dialog.connect("delete-event", self.on_delete_event)

		button_file_choose = self.widgets_object_dict.get('filechooserbutton_rebuild_select_iso_file')
		button_foldar_choose = self.widgets_object_dict.get('filechooserbutton_rebuild_select_foldar')
		entry_file_name = self.widgets_object_dict.get('entry_rebuild_enter_file_name')

		spinner = self.widgets_object_dict.get('spinner_rebuild_spinner')
		progressbar = self.widgets_object_dict.get('progressbar_rebuild_progressbar')

		file_choose = self.get_config('FILE-CHOOSE')
		foldar_choose= self.get_config('FOLDAR-CHOOSE')
		file_name = self.get_config('FILE-NAME')

		if file_choose != None:
			button_file_choose.set_filename(file_choose)
		if foldar_choose != None:
			button_foldar_choose.set_filename(foldar_choose)
		if file_name != None:
			entry_file_name.set_text(file_name)

		dialog.show_all()
#		spinner.hide()
		progressbar.hide()


























