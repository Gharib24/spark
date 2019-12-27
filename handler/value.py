import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

class GetValue:
	def __init__(self, file):
		self.file = file
	def get_value(self, File=None):
		self.value = {}
		if not self.value:
			with open(self.file, "r") as f:
				for line in f:
					if '#' in line :
							continue
					elif not line.strip():
							continue
					else:
						_line = (line.strip().split())
						question = _line[1]
						if len(_line) >= 4:
							value = ' '.join((line.strip(' ').split()[3:]))
							self.value[question] = value
						elif len(_line) == 3:
							value = 'none_value'
							self.value[question] = value
				f.close


class Value:
	def __init__(self, f=None):
		self._file = f

	def value_length(self, f):
		v = GetValue(f)
		v.get_value()
		self.value = v.value
		length = len(self.value.values())
		return length

	def return_value(self):
		for i in self.id:
			value = self.value.get(i)
			widget = self.id.get(i)
			widget_type = (str(type(widget)).strip("'class<>").replace('.', ' ').split()[-1:][0])

			if value != None:
				if 'Entry' == widget_type:
					if value =='none_value':
						value = ' '
					if 'password-crypted' in i:
						widget.set_text('PASSWORD')
						self.store_update('passwd/user-password-crypted', value)
#						continue
					else:
						widget.set_text(value)
				elif 'CheckButton' == widget_type:
					if value =='true':
						value = True
					elif value =='false':
						value = False
					elif value =='none_value':
						value = True

					if i =='passwd/root-login':
						value = (not value)
					elif i == 'apt-setup/cdrom/set-first':
						value = (not value)

					elif i == 'apt-setup/services-select':
						value_list = value.replace(',','').split()
						for i in value_list:

							widget = self.id.get(i)
							widget.set_active(True)
					elif type(value) == bool:
						widget.set_active(value)

					if value == False:
						self.on_check_button_toggled(widget, question=i)
					elif value == True:
						widget.set_active(value)

				elif 'ComboBox' == widget_type:
						if i == "debian-installer/locale":
							for x, name in  enumerate(self.locales_supported_list, 0):
								if name[0] == value:
									widget.set_active(x)
									break
						elif i == "keyboard-configuration/xkb-keymap":
							for x in range(len(self.layout_list)):
								if self.layout_list[x][0] == value:
									widget.set_active(x)
									break
						elif i == "time/zone":
							for x, name in  enumerate(self.zoneinfo_list, 0):
								if name == value:
									widget.set_active(x)
									break

				elif 'CellRendererToggle' == widget_type:
					if i == "localechooser/supported-locales":
						for x, v in enumerate(value.replace(',', '').split(), 0):
							for path, name in  enumerate(self.locales_supported_list, 0):
								if v == name[0]:
									self.on_cell_toggled(widget, path, question=i)
#									self.locales_supported_liststore[x][0] = True
					elif i == "tasksel/first":
						for x, value in enumerate(value.replace(',', '').split(), 0):
							for path, name in  enumerate(self.package_liststore , 0):
								if value == name[1]:
									self.on_cell_toggled(widget, path, question=i)

				elif 'ComboBoxText' == widget_type:
					widget.set_active_id(value)
#					self.on_comboboxtext_with_entry_changed(widget , question=i)

				elif 'RadioButton' == widget_type:
					if value =='true':
						value = True
					elif value =='false':
						value = False

					if i == 'partman-auto/expert_recipe':
						widget.set_active(True)
						line = value.split()
						list = []
						for i in range(len(line)):
							if '.' in line[i]:
								self.disk = self.combobox_text_disk.get_active_text()
								if len(self.disk) == 0:
									self.disk = '/dev/sda'
								self.recipe_store.append([self.disk+str(len(self.recipe_store)+1), None,None,None,None,None,None])
								list.append([])
						counter = 0
						for i in range(len(line)):
							if i in [0, 1]:
								continue
							elif '.' in line[i]:
								counter += 1
								continue
							if i < (len(line)):
								list[counter].append(line[i])

						for counter in range(len(list)):
							for i, _str  in  enumerate(list[counter], 0):
								if i in [0]:
									self.recipe_store[counter][3] = _str
								elif i in [1]:
									self.recipe_store[counter][4] = _str
								elif i in [2]:
									self.recipe_store[counter][5] = _str
								if i in [3]:
									self.recipe_store[counter][1] = _str
								elif i in [15]:
									self.recipe_store[counter][2] = _str
								elif i in [18]:
									self.recipe_store[counter][6] = _str
								elif 'swap' in _str:
									self.recipe_store[counter][6] = 'N/A'
									self.recipe_store[counter][2] = 'N/A'
						self.to_recipe()
					else:
						widget.set_active(value)
						self.on_radio_button_toggled(widget , question=i)
				elif 'TextBuffer' == widget_type:
					if i == 'preseed/late_command':
						f = open(self.post_installation_script, "r")
						widget.set_text(f.read())
						f.close()
						self.on_button_clicked(self.button_post_add, question=i, data=None)
					elif i == 'preseed/run':
						f = open(self.pre_installation_script, "r")
						widget.set_text(f.read())
						f.close()
						self.on_button_clicked(self.button_pre_add, question=i, data=None)
					else:
						widget.set_text(value)
#				else:
#					print(widget_type)
#					print(i)
			elif i == 'netcfg/wireless_wep':
				key = self.value.get('netcfg/wireless_wpa')
				if key != None:
					widget.set_text(key)
			else:
				continue




		list = []
		for i in range(0, 10):
			local ='local'+str(i)
			value = self.value.get('apt-setup/'+local+'/repository')
			if value != None:
				list.append([])
				list[i].append(local)
			for text in ('repository','key', 'comment', 'source'):
				value = self.value.get('apt-setup/'+local+'/'+text)
				if value != None:
					if value =='true':
						value = True
					elif value =='false':
						value = False
					list[i].append(value)
		if len(self.repos_store) > 0:
			for i in range(len(self.repos_store)):
				iter = self.repos_store.get_iter(0)
				self.repos_store.remove(iter)

		for i in range(len(list)):
			self.repos_store.append(list[i])
			self.to_repos()
