import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk


class Handler():
	def __init__(self):
		super().__init__()

	def __call__(self):
		pass

	def on_delete_event(self, window, event):
		name = window.get_name()
		if name == 'toplevale_window':
			if self.count_answered_question() > 0:
				self.base_message_dialog('question', 'save_entered')
				return True
			else:
				return False
		elif name == 'dialog_create_an_iso_image':
			if self.job:
				return True
			else:
				return False
		else:
			return False

	def on_destroy(self, *argv):
		if self.count_answered_question() > 0:
			self.base_message_dialog('question', 'save_entered')
		self.get_application().quit()

	def on_treeselection_changed_main(self, treeselection, data=None):
		(model, iter) = treeselection.get_selected()
		if iter is not None:
			rownumobj = model.get_path(iter)
			intrownum = int(rownumobj.to_string())
			selected_name = ("%s" % (model[iter][1]))
			selected_num = rownumobj.to_string()
#			self.log.info(selected_num, selected_name)
			if intrownum >= 0:
				stack_name = self.stack_1.get_child_by_name(selected_num)
				if stack_name is not None:
					self.frame_2.set_label(selected_name)
					current_page = int(self.stack_1.get_visible_child_name()) #TODO error here if none
					if current_page > intrownum:
						self.stack_1.set_transition_type(5)
					elif current_page < intrownum:
						self.stack_1.set_transition_type(4)
					self.stack_1.set_visible_child_name(selected_num)

	def on_menuitem_activate(self, menuitem):
		label_text = menuitem.get_label()
		if menuitem.name == 'open_preseed_file':
			self.preseed_file_viwe_diaog()
		elif menuitem.name == 'create_an_iso_file':
			self.iso_image_builder_diaog()
		elif menuitem.name == 'quit':
			self.on_destroy()
		elif menuitem.name == 'about':
			self.about_dialog()
		else:
			self.base_message_dialog('info', 'oops')

	def on_button_clicked_main(self, button):
		name = button.get_name()
		if name == 'save':
			self.save_preseed_file()
		elif name == 'reload':
			if self.get_value_from_preseed_file():
				self.base_message_dialog('question', 'load_values')
		elif name == 'create':
			self.iso_image_builder_diaog()
		elif name == 'open':
			self.preseed_file_viwe_diaog()
		else:
			self.base_message_dialog('info', 'oops')

	def on_button_go_clicked_main(self, button):
		name = button.get_name()
		(model, iter) = self.treeselection.get_selected()
		rownumobj = model.get_path(iter)
		intrownum = int(rownumobj.to_string())
		if name == 'next':
			if intrownum < len(model):
				self.treeselection.select_path(intrownum+1)
		elif name == 'previous':
			if intrownum > 0:
				self.treeselection.select_path(intrownum-1)





