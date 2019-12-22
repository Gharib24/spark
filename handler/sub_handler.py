import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

from crypt import crypt, METHOD_SHA512
from datastore import *
from partitionrecipe_handler import Handler as PHandler
from additional_repos_handler import Handler as AHandler
from dialog_handler import Handler as DHandler
from rebuild_handler import Handler as RHandler
from review import View
v = View()
locales_list = []
tasksel_list = []
services_select = []
layoutcode_list = []
#--------------------------------------------------------------------------------------------------
c = 0
class Handler(PHandler ,RHandler, DHandler, AHandler, DataStore):
	def __init__(self):
		super().__init__()
	def __call__(self): 
		pass

	def store_update(self, question, value):
		try:
			self.set(question ,value)
			#self.log.info("{}".format(self.get(question)))
			v.view(True)
			if self.get_changed_data() != None:
				self.statusbar.push(self.statusbar_context_1, self.get_changed_data())
		except NameError as e:
				self.log.error(e)

	def on_entry_changed(self, entry, question=None):
		value = entry.get_text()
		if len(value) <= 0:
			if question == 'netcfg/wireless_wep':
					if self.w_comboboxtext.get_active_text() == 'wpa':
						question = 'netcfg/wireless_wpa'
			value = 'delete'
		elif len(value) > 0:
			if question == "passwd/user-fullname":
#				if self.id.get('passwd/username') != None:
				if len(value.split()) <= 1:
						self.id.get('passwd/username').set_text(value.lower())
				elif len(value.split()) == 2:
					initial = (value.split()[0][:1].lower() + value.split()[1][:1].lower())
					self.id.get('passwd/username').set_text(initial)
			elif "crypted" in question:
				value = (crypt(value, METHOD_SHA512))
			elif question == 'netcfg/wireless_wep':
				if self.w_comboboxtext.get_active_id() == 'wpa':
					question =  'netcfg/wireless_wpa'
		self.store_update(question, value)
		if question == 'netcfg/wireless_essid':
			self.store_update('netcfg/wireless_essid_again', value)


	# XXX on_combobox_changed XXX
	def on_combobox_changed(self, combobox, question=None):
		treeiter = combobox.get_active_iter()
		model = combobox.get_model()
		if question == 'time/zone':
			value = (model[treeiter][0])
		elif question == 'debian-installer/locale':
			value = (model[treeiter][1])
			language_code = (value.split('_')[0])
			country_code = (value.split('_')[1][0:2])
			self.id.get('debian-installer/language').set_text(language_code)
			self.id.get('debian-installer/country').set_text(country_code)
		elif question == 'keyboard-configuration/xkb-keymap':
			value = (model[treeiter][0])
			layoutcode = self.id.get('keyboard-configuration/layoutcode').get_text()
			add = True
			for i in layoutcode.replace(',', '').split():
				if i == value:
					add = False
					break
				
			if add == True:
				if len(layoutcode) <= 0:
					self.id.get('keyboard-configuration/layoutcode').set_text("{}".format(value))
				else:
					self.id.get('keyboard-configuration/layoutcode').set_text("{}, {}".format(layoutcode, value))
					self.id.get('keyboard-configuration/toggle').set_text('No toggling')
		self.store_update(question, value)


	# XXX on_cell_toggled XXX
	def on_cell_toggled(self, widget, path, question=None):
		if question == 'tasksel/first':
			liststore = self.package_liststore
			liststore[path][0] = not liststore[path][0]
			state = (liststore[path][0])
			value = (liststore[path][1].split()[0])
			if state == True:
				tasksel_list.append(value)
				value = ', '.join(tasksel_list)
				self.store_update(question ,value)
			elif state == False:
				tasksel_list.remove(value)
				value = ', '.join(tasksel_list)
				if len(tasksel_list) == 0:
					value = 'delete'
		else:
			liststore = self.locales_supported_liststore
			liststore[path][0] = not liststore[path][0]
			state = (liststore[path][0])
			value = (liststore[path][1])
			if state == True:
				locales_list.append(value)
				value = ', '.join(locales_list)
			elif state == False:
				locales_list.remove(value)
				value = ', '.join(locales_list)
				if len(locales_list) == 0:
					value = 'delete'
		self.store_update(question, value)


#	# XXX on_check_button_toggled XXX
	def on_check_button_toggled(self, checkbutton, question=None):
		active = checkbutton.get_active()
		value = str(active).lower()

		if question == 'passwd/root-login':
				self.id.get("passwd/root-password-crypted").set_sensitive(not active)
				value = str(not active).lower()
#				if active:
#					self.store_update('passwd/root-password-crypted', 'delete')
		elif question == 'apt-setup/services-select':
				VALUE = checkbutton.get_label()
				if active:
					services_select.append(VALUE)
					value = ', '.join(services_select)
				elif not active:
					services_select.remove(VALUE)
					if len(services_select) == 0 :
						value = 'delete'
					else:
						value = ', '.join(services_select)

		elif question == 'apt-setup/cdrom/set-first':
				value = str(not active).lower()
		elif question == 'finish-install/reboot_in_progress':
				if value == 'true':
					value = " "
				else:
					value = 'delete'

		self.store_update(question, value)


	# XXX on_comboboxtext_with_entry_changed XXX
	def on_comboboxtext_with_entry_changed(self, combobox, question=None):
		tree_iter = combobox.get_active_iter()
		if tree_iter is not None:
			model = combobox.get_model()
			value = model[tree_iter][0]
		else:
			entry = combobox.get_child()
			value = entry.get_text()

		if len(value) <= 0:
			value = 'delete'

		self.store_update(question, value)

		if question == 'netcfg/choose_interface':
			if 'wlan' in value:
				SENSITIVE = True
			else:
				SENSITIVE = False
			self.id.get('netcfg/wireless_essid').set_sensitive(SENSITIVE)
			self.id.get('netcfg/wireless_essid').set_text('')
			self.id.get('netcfg/wireless_wep').set_sensitive(SENSITIVE)
			self.id.get('netcfg/wireless_wep').set_text('')
			self.w_comboboxtext.set_sensitive(SENSITIVE)

		elif question == 'partman-auto/disk':
			 # partitionrecipe
			if value == 'delete':
				disk = '/dev/sda'
			else:
				disk = value
			for col in range(len(self.recipe_store)):
				self.recipe_store[col][0] = str(disk + str(col+1))

		elif question == 'mirror/http/hostname':
			self.store_update(question, value)
			self.id.get('mirror/http/directory').set_text('/debian')
			self.id.get('apt-setup/security_host').set_text('security.debian.org')
			self.id.get('apt-setup/volatile_host').set_text(' ')
			self.id.get('apt-setup/use_mirror').set_active(True)
			self.id.get('updates').set_active(True)
			self.id.get('security').set_active(True)
			self.id.get('apt-setup/cdrom/set-first').set_active(True)
			self.id.get('apt-setup/disable-cdrom-entries').set_active(True)
			self.store_update('mirror/http/proxy', '')


	# XXX on_comboboxtext_changed
	def on_comboboxtext_changed(self, comboboxtext, question=None):
		text = comboboxtext.get_active_text()
		value =  comboboxtext.get_active_id()
		if question == 'netcfg/disable_dhcp':
			self.store_update(question, value)
			 # XXX SENSITIVE
			list =['netcfg/get_ipaddress', 'netcfg/get_netmask', 'netcfg/get_gateway', 'netcfg/get_nameservers']
			if value == 'true':
				not_value = 'false'
				SENSITIVE = True
			else:
				not_value = 'true'
				SENSITIVE = False
				for i, widget in  enumerate(list, 0):
					self.id.get(widget).set_text('')
			self.store_update('netcfg/confirm_static', value)
			for i, widget in  enumerate(list, 0):
				self.id.get(widget).set_sensitive(SENSITIVE)

		elif question == "netcfg/wireless_security_type":
			self.store_update(question, value)
			self.id.get('netcfg/wireless_wep').set_text('')
			self.store_update('netcfg/wireless_wep', 'delete')
			self.store_update('netcfg/wireless_wpa', 'delete')

		elif question == "partman-partitioning/default_label":
			self.store_update(question, value)
			for i, question in enumerate(partition_questions, 0):
				if i <= 6:
					continue
				else:
					if question == 'partman-auto/method':
						auto_value = 'regular'
					elif question == 'partman/choose_partition':
						auto_value = 'finish'
					elif question == 'partman/early_command':
						auto_value = 'umount /media'

					elif question == 'partman/early_command':
						auto_value = 'umount /media'
					else:
						auto_value = 'true'
					self.store_update(question, auto_value)

		elif question == "partman-auto/choose_recipe":
			self.store_update(question, value)
			self.store_update('partman-efi/non_efi_system', 'true')
		else:
			self.store_update(question, value)

	# XXX on_radio_button_toggled
	def on_radio_button_toggled(self, radiobutton, question=None):
		if question ==  'partman-auto/choose_recipe':
			if radiobutton.get_active():
				self.choose_recipe_comboboxtext.set_sensitive(True)
				self.partitionrecipe_frame.set_sensitive(False)
				value = self.choose_recipe_comboboxtext.get_active_id()
				if value != None:
					self.store_update(question, value)
					self.store_update('partman-efi/non_efi_system', 'true')
			else:
				self.choose_recipe_comboboxtext.set_sensitive(False)
				self.partitionrecipe_frame.set_sensitive(True)
				self.store_update(question,'delete')
				self.store_update('partman-efi/non_efi_system', 'delete')
		elif question ==  'partman-auto/expert_recipe':
			if radiobutton.get_active():
				self.choose_recipe_comboboxtext.set_sensitive(False)
				self.partitionrecipe_frame.set_sensitive(True)
				self.to_recipe()
			else:
				self.choose_recipe_comboboxtext.set_sensitive(True)
				self.partitionrecipe_frame.set_sensitive(False)
				self.store_update(question,'delete')
				self.store_update('partman-efi/non_efi_system', 'delete')
				self.store_update('partman-auto/choose_recipe', 'delete')

		else:
			value = str(radiobutton.get_active()).lower()
			self.store_update(question, value)


	def on_text_changed(self, buffer, question=None, file=None):
		if question != None:
			if question == "preseed/run":
				if self.button_pre_save.get_sensitive() == False:
					self.button_pre_save.set_sensitive(True) 
			elif question == "preseed/late_command":
				if self.button_post_save.get_sensitive() == False:
					self.button_post_save.set_sensitive(True)

			else:
				start, end = buffer.get_bounds()
				value = buffer.get_text(start, end, include_hidden_chars = False).replace('\n', ' ')
				self.store_update(question ,value)

		elif file != None:
			start, end = buffer.get_bounds()
			text = buffer.get_text(start, end, include_hidden_chars = False)
			f = open(file, "w")
			f.write(text)
			f.close()
			self.info_dialog('Saved successfully', "<a href='file://{0}'>file: {0} </a>".format(file))

	def on_button_clicked(self, button, question=None, data=None):
			label = button.get_label()
			if label == "Save":
				if question == "preseed/run":
					buffer = self.text_buffer_a
					value = 'scripts/pre-installation-script.sh'
					self.on_text_changed(buffer, file=self.pre_installation_script)
					button.set_sensitive(False)
					self.button_pre_add.set_label("Remove")
				elif question == "preseed/late_command":
					buffer = self.text_buffer_b
					value = '[ "$file" ]&& sh /cdrom/preseed/scripts/post-installation-script.sh'
					self.on_text_changed(buffer, file=self.post_installation_script)
					button.set_sensitive(False)
					self.button_post_add.set_label("Remove")

			elif label == "Remove":
				value = 'delete'
				button.set_label("Add")

			elif label == "Add":
				if question == "preseed/run":
					value = 'scripts/pre-installation-script.sh'
				elif question == "preseed/late_command":
					value = '[ "$file" ]&& sh /cdrom/preseed/scripts/post-installation-script.sh'

				button.set_label("Remove")
			self.store_update(question, value)

#----------------------------------------------------------------------------------------------------------------------











