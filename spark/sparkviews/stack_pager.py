import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GObject

from spark.sparkviews.base_container import BaseContainer
from spark.sparkviews.base_widget import BaseWidget
from spark.sparkviews.framing import Framing
from spark.sparkviews.scripting import Scripting

from spark.sparkhandlers.widgets_handler import Handler as WidgetsHandler
from spark.sparkhandlers.rebuild_handler import Handler as RebuildHandler


class StackPager(RebuildHandler, BaseContainer, BaseWidget, Framing, Scripting, WidgetsHandler):

	def __init__(self):
		super().__init__()

	def stack_containers(self):
		element = self.static_data.stack_components.items()
		for index, (key, values) in enumerate(element):
			if key in self.static_data.category:
				grid = self.base_grid(namespace=key)
				vbox = self.base_vbox(namespace=key)
				vbox.add(grid)
				stack_page_name = str(self.static_data.category.index(key))
				self.stack_1.add_named(vbox, stack_page_name)
				del grid
				del vbox

	def widgets_parking(self, components):
		components =  components.items()
		for index, (key, components_tuple) in enumerate(components):
			if key in self.static_data.category:
				grid_name = f"grid_{self.naming(key)}"
				grid = getattr(self, grid_name)
				top_attach = 0
				widget = None

				for index, components_dict in enumerate(components_tuple, 0):
					question = components_dict.get('question')
					label_text = components_dict.get('label_text')
					if 'widget_type' in list(components_dict.keys()):
						widget_type = components_dict.get('widget_type')
						widget_type_sort_name = components_dict.get('widget_type').split('_')[0]
						# left labels
						if widget_type not in ('checkbutton', 'button', 'spinner', 'label', 'progressbar'):
							label = self.base_label(question, label_text)
							grid.attach(label, 0, top_attach, 1, 1)
							top_attach += 1

						# widget next label
						if hasattr(BaseWidget, f"base_{widget_type_sort_name}"):
							base_widget = getattr(BaseWidget, f"base_{widget_type_sort_name}")
							if widget_type in ('checkbutton', 'button', 'label', 'filechooserbutton', 'progressbar'):
								widget = base_widget(self, question, label_text)
							elif widget_type_sort_name == 'comboboxtext':
								widget = base_widget(self, question, widget_type)
							else:
								widget = base_widget(self, question)
							self.question_to_own_widget_object_dict[question] = widget
						else:
							self.log.error(f"attribute does not exist. base_{widget_type_sort_name}")

						if widget != None:
							widget_type_name = GObject.type_name(widget)
#							self.log.info(widget_type_name)
							if widget_type_name in ("GtkCheckButton", "GtkButton",):
								grid.attach(widget, 1, top_attach,1, 1)
								top_attach += 1

							elif widget_type_name in ("GtkTreeView", "GtkTextView"):
								label.set_alignment(xalign=0, yalign=0)
								scrolledwindow = self.base_scrolledwindow(key)
								grid.attach_next_to(scrolledwindow,label,
										Gtk.PositionType.RIGHT, 1, 10)
								top_attach += 10
								scrolledwindow.add(widget)

							elif widget_type_name in ('GtkSpinner' ,'GtkLabel', 'GtkProgressBar'):
								if widget_type_name == "GtkLabel":
									widget.set_xalign(0.5)
								grid.attach(widget, 0, top_attach, 2, 1)
								top_attach += 1

							else:
								grid.attach_next_to(widget, label, Gtk.PositionType.RIGHT, 1, 1)

						# all separator
						if self.static_data.separator.get(key) != None:
							if index in self.static_data.separator.get(key):
								separator = self.base_separator()
								grid.attach(separator, 0, top_attach, 2, 1)
								top_attach += 1

					elif 'container_type' in list(components_dict.keys()):
						container_type = components_dict.get('container_type')

						if container_type == "frame":
							frame = self.framing(question, label_text)
	#						if GObject.type_name(frame) == "GtkFrame":
							vbox_name = f"box_{self.naming(key)}"
							vbox = getattr(self, vbox_name)
							vbox.add(frame)

						elif container_type == "scripting":
							scripting = self.scripting(question, label_text)
							vbox_name = f"box_{self.naming(key)}"
							vbox = getattr(self, vbox_name)
							vbox.add(scripting)
#				widget = None
		for index, (key, widget) in enumerate(self.widgets_object_dict.items()):
#			self.log.debug(key, widget)
			self.do_widget_connect_handler(widget, data=None)

#		for index, (key, label) in enumerate(self.labels_object_dict.items()):
#			self.log.debug(key, label)
#-------------------------------------------------------------------------------

	def do_widget_connect_handler(self, widget, data=None):
			widget_type_name_sort = GObject.type_name(widget).replace('Gtk', "").lower()
			#self.log.info(widget_type_name_sort)

			if widget_type_name_sort in ('liststore', 'treeview', 'spinner', 'progressbar'):
				pass
			elif 'rebuild' in widget.question:
				if hasattr(widget, 'signal_name'):
					signal_name = self.naming(widget.signal_name)
					if hasattr(self, f"on_{widget_type_name_sort}_{signal_name}_rebuild"):
						handler = getattr(self, f"on_{widget_type_name_sort}_{signal_name}_rebuild")
						widget.connect(f"{widget.signal_name}", handler)
					else:
						self.log.warn(f"{widget_type_name_sort}: HANDLER does not exit")
						print(f'def on_{widget_type_name_sort}_{signal_name}_rebuild(self, {widget_type_name_sort}):')
				else:
					self.log.warn(f"{widget_type_name_sort}: SIGNAL_NAME does not exit")

			else:
				if widget_type_name_sort == 'comboboxtext':
					if widget.get_has_entry():
						widget_type_name_sort+= "_with_entry"
				if hasattr(widget, 'signal_name'):
					signal_name = self.naming(widget.signal_name)
					if hasattr(self, f"on_{widget_type_name_sort}_{signal_name}"):
						handler = getattr(self, f"on_{widget_type_name_sort}_{signal_name}")
						widget.connect(f"{widget.signal_name}", handler)
					else:
						self.log.warn(f"{widget_type_name_sort}: HANDLER does not exit")
						print(f'def on_{widget_type_name_sort}_{signal_name}(self, {widget_type_name_sort}):')
				else:
					self.log.warn(f"{widget_type_name_sort}: SIGNAL_NAME does not exit")



