import gi, sys 
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

from sub_handler import Handler as SHandler
from sys_supported import Path
from datastore import SaveToFile
from gi.repository import Gio
#--------------------------------------------------------------------------------------------------
class Handler(Path, SaveToFile, SHandler):
	def __init__(self):
		super().__init__()

	def __call__(self): 
		pass

	def on_delete_event(self, *argv):
		if self.get_changed_data() != None:
			self.question_dialog('save entered data?','{}'.format(self.get_changed_data()), data='unsaved')
			return False
		return False

	def on_destroy(self, *argv):
		if self.get_changed_data() != None:
			self.question_dialog('save entered data?','{}'.format(self.get_changed_data()), data='unsaved')
		self.get_application().quit()

	#XXX on_treeview_selection_changed XXX
	def on_treeview_selection_changed(self, treeselection, data=None):
		# get the model and the iterator that points at the data in the model
		(model, iter) = treeselection.get_selected()
		if iter is not None:
			# rowcontents = model[iter][0:3]  # for a 4 column treeview
			rownumobj = model.get_path(iter)
			intrownum = int(rownumobj.to_string())
			selected_name = ("%s" % (model[iter][0]))
			selected_num = rownumobj.to_string()
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
					self.log.debug("{} : {} : Page: {}".format(__name__, selected_name, selected_num))

				elif stack_name is None:
					self.log.debug("{} : {} : No child with this parent : {}".format(__name__,selected_name, selected_num))
				else:
					self.log.error("error")

	def on_radio_button_toggled_view(self, radiobutton, data=None):
		name = radiobutton.get_label()
		if name == "View style 1":
			self.stack_2.set_transition_type(2)
			self.stack_2.set_visible_child_name('1')
		else:
			self.stack_2.set_transition_type(3)
			self.stack_2.set_visible_child_name('2')

	def on_check_button_toggled_menu(self, checkbutton, data=None):
		name = checkbutton.get_label()
		settings = Gtk.Settings.get_default()
		if name == 'Dark theme':
			if checkbutton.get_active():
				settings.set_property('gtk-application-prefer-dark-theme', True)
				self.cfg.write('dark', True)
			else:
				settings.set_property('gtk-application-prefer-dark-theme', False)
				self.cfg.write('dark', False)
		elif name == 'Right panel':
			if checkbutton.get_active():
				self.frame_3.show()
				self.cfg.write('panel', True)
			else:
				self.frame_3.hide()
				self.cfg.write('panel', False)

