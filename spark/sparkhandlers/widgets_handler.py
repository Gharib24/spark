#!/usr/bin/env python
from crypt import crypt, METHOD_SHA512

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

from spark.sparkhandlers.col_data_handler import Handler as ColDataHandler
from spark.sparkhandlers.data_Handler import Handler as DataHandler


class Handler(DataHandler, ColDataHandler):
	def __init__(self):
		DataHandler.__init__(self)
		super().__init__()

	def do_data_Handler(self, question, answer):
		self.set_answer_question(question, answer)
		self.log.info(self.get_answer_question(question))
		self.count_answered_question()

	def on_entry_changed(self, entry):
		question = entry.question
		value = entry.get_text()
		if len(value) <= 0 or value.isspace():
			value = 'delete'
		else:
			if question == "passwd/user-fullname":
				if len(value.split()) <= 1:
						self.widgets_object_dict.get('entry_passwd_username').set_text(value.lower())
				elif len(value.split()) == 2:
					initial = (value.split()[0][:1].lower() + value.split()[1][:1].lower())
					self.widgets_object_dict.get('entry_passwd_username').set_text(initial)
			elif "crypted" in question:
				value = (crypt(value, METHOD_SHA512))
		answer = value
		self.do_data_Handler(question, answer)

	def on_checkbutton_toggled(self, check_button):
		question = check_button.question
		active = check_button.get_active()
		value = str(active).lower()
		if question == 'passwd/root-login':
			self.widgets_object_dict.get("entry_passwd_root_password_crypted").set_sensitive(not active)
			value = str(not active).lower()

		elif 'apt-setup/services-select' in question:
			listValues = []
			for i in range(0, 3):
				check_button = self.widgets_object_dict.get('checkbutton_apt_setup_services_select'+str(i))
				active = check_button.get_active()
				if active:
					value = check_button.get_label().split()[0].lower()
					listValues.append(value)
			question = 'apt-setup/services-select'
			value = ', '.join(listValues)
			if len(value) <= 0 or value.isspace():
				value = 'delete'
		elif question == 'apt-setup/cdrom/set-first':
			value = str(not active).lower()
		elif question == 'finish-install/reboot_in_progress':
			if value == 'true':
				value = " "
			else:
				value = "delete"

		self.do_data_Handler(question, value)

	def partman_auto_question_auto_answer(self):
		question_auto_answer=(
				('partman-efi/non_efi_system', 'true'),
				('partman-auto/method', 'regular'),
				('partman-auto/purge_lvm_from_device', 'true'),
				('partman-partitioning/confirm_write_new_label', 'true'),
				('partman/choose_partition', 'finish'),
				('partman/confirm_write_new_label', 'true'),
				('partman/confirm_nooverwrite', 'true'),
				('partman/confirm', 'true'),
		)
		for items in question_auto_answer:
			self.do_data_Handler(items[0], items[1])

	def on_comboboxtext_changed(self, comboboxtext):
		question = comboboxtext.question
		name = comboboxtext.get_name()
		text = comboboxtext.get_active_text()
		value =  comboboxtext.get_active_id()
		if question not in ['partman-auto/expert_recipe', "apt-setup/local0/repository"]:
			if len(value) <= 0 or value.isspace():
				value = 'delete'

			if question == 'partman-partitioning/default_label':
				self.partman_auto_question_auto_answer()
				model = self.widgets_object_dict.get('liststore_partman_auto_expert_recipe')
				if len(model) < 10:
					self.widgets_object_dict.get('button_0_partman_auto_expert_recipe').set_sensitive(True)
	#
			elif question == "netcfg/wireless_security_type":
				self.widgets_object_dict.get('entry_netcfg_wireless_wep').set_text('')
				self.labels_object_dict.get('label_netcfg_wireless_wep').set_text(f"Wireless {text.split('/')[0]} Security Key")
				self.widgets_object_dict.get('entry_netcfg_wireless_wep').set_name(f"netcfg/wireless_{value.split('/')[0]}")
				self.widgets_object_dict.get('entry_netcfg_wireless_wep').question = f"netcfg/wireless_{value.split('/')[0]}"

			elif question == "netcfg/disable_dhcp":
				 # XXX SENSITIVE
				list =('entry_netcfg_get_ipaddress', 'entry_netcfg_get_netmask', 'entry_netcfg_get_gateway', 'entry_netcfg_get_nameservers')
				for i, widget in  enumerate(list, 0):
					self.widgets_object_dict.get(widget).set_text('')
					self.widgets_object_dict.get(widget).set_sensitive(eval(value.title()))

			elif question == "partman-auto/choose_recipe":
				if value == 'spark_recipe':
					self.frame_partman_auto_expert_recipe.set_sensitive(True)
					self.col_data_handler('partman-auto/expert_recipe')
				else:
					self.frame_partman_auto_expert_recipe.set_sensitive(False)
					self.do_data_Handler('partman-auto/expert_recipe', 'delete')

			self.do_data_Handler(question, value)
		elif question in ['partman-auto/expert_recipe', "apt-setup/local0/repository"]:
			active_text = comboboxtext.get_active_text()
			row_cell_text_completed = getattr(self, f"completed_text_{name}")
			treeselection = self.widgets_object_dict.get(f"treeselection_{self.naming(question)}")
			(model, iter) = treeselection.get_selected()
			if iter !=  None:
				for i, text in enumerate(row_cell_text_completed, 0):
					if text[0] == active_text:
						for col, text_completed in enumerate(row_cell_text_completed[i][1], 1):
							(model[iter][col]) = text_completed
						break
				self.col_data_handler(question)

	def on_comboboxtext_with_entry_changed(self, comboboxtext):
		question = comboboxtext.question
		name = comboboxtext.get_name()
		text = comboboxtext.get_active_text()
		value =  comboboxtext.get_active_id()
		tree_iter = comboboxtext.get_active_iter()
		if tree_iter is not None:
			model = comboboxtext.get_model()
			value = model[tree_iter][0]
		else:
			entry = comboboxtext.get_child()
			value = entry.get_text()
		if len(value) <= 0 or value.isspace():
			value = 'delete'
		self.do_data_Handler(question, value)

		if question == 'netcfg/choose_interface':
			if 'wlan' in value:
				SENSITIVE = True
#				self.widgets_object_dict.get('netcfg/wireless_essid').set_text('')
#				self.widgets_object_dict.get('netcfg/wireless_wep').set_text('')
			else:
				SENSITIVE = False
			self.widgets_object_dict.get(
				'comboboxtext_netcfg_wireless_security_type').set_sensitive(SENSITIVE)
			self.widgets_object_dict.get('entry_netcfg_wireless_essid').set_sensitive(SENSITIVE)
			self.widgets_object_dict.get('entry_netcfg_wireless_wep').set_sensitive(SENSITIVE)
		elif question == 'mirror/http/hostname':
			self.widgets_object_dict.get('entry_mirror_http_directory').set_text('/debian')
			self.widgets_object_dict.get('entry_apt_setup_security_host').set_text('security.debian.org')
		elif question == 'partman-auto/disk':
			 # partitionrecipe
			if value == 'delete':
				disk = '/dev/sda'
			else:
				disk = value
			model = self.widgets_object_dict.get('liststore_partman_auto_expert_recipe')
			for col in range(len(model)):
				model[col][0] = str(disk + str(col+1))

	def on_entrycompletion_match_selected(self, entry_completion, model, iter):
		question = entry_completion.question
		name = self.naming(question)
		combobox = self.widgets_object_dict.get(f"combobox_{name}")
		combobox.set_active_iter(iter)

	def on_combobox_changed(self, combobox):
		name = combobox.get_name()
		question = combobox.question
		treeiter = combobox.get_active_iter()
		model = combobox.get_model()
#		if treeiter is not None:
#			value = model[treeiter][0]
#		else:
#			entry = combobox.get_child()
#			value = entry.get_text()
		if treeiter is not None:
			value = model[treeiter][0]
			if question == 'debian-installer/locale':
				if len(value) > 2:
					language = (value.split(' ')[0])
					language_code = (language.split('_')[0])
					country_code = (language.split('_')[1][0:2])
					value = language
				elif len(value) == 2:
					language_code = value
					country_code = ''
				self.widgets_object_dict.get('entry_debian_installer_language').set_text(language_code)
				self.widgets_object_dict.get('entry_debian_installer_country').set_text(country_code)
			elif question == 'keyboard-configuration/xkb-keymap':
				layoutcode = self.widgets_object_dict.get('entry_keyboard_configuration_layoutcode').get_text()
				add = True
				for i in layoutcode.replace(',', '').split():
					if i == value:
						add = False
						break

				if add == True:
					if len(layoutcode) <= 0:
						self.widgets_object_dict.get('entry_keyboard_configuration_layoutcode').set_text(value)
					else:
						self.widgets_object_dict.get('entry_keyboard_configuration_layoutcode').set_text(f"{layoutcode}, {value}")
					self.widgets_object_dict.get('entry_keyboard_configuration_toggle').set_text('No toggling')
		else:
			entry = combobox.get_child()
			value = entry.get_text()
			if len(value) <= 0 or value.isspace():
				value = 'delete'
			else:
				value = None
		if value != None:
			self.do_data_Handler(question, value)

	def on_cellrenderertoggle_toggled(self, cellrenderertoggle, path):
		question = cellrenderertoggle.question
		treeselection = self.widgets_object_dict.get(f"treeselection_{self.naming(question)}")
		(model, iter) = treeselection.get_selected()
		column_number = cellrenderertoggle.column_number
		valuelist = cellrenderertoggle.list
		value = ''
		model[path][column_number] = not model[path][column_number]
		if question in ('localechooser/supported-locales', 'tasksel/first'):
			if question == 'tasksel/first':
				value = self.tasksel_first[int(path)][1]
			else:
				value = (model[path][1].split()[0])
			active = (model[path][0])
			if active == True:
				valuelist.append(value)
				value = ', '.join(valuelist)
			elif active == False:
				valuelist.remove(value)
				value = ', '.join(valuelist)
				if len(valuelist) == 0:
					value = 'delete'
			self.do_data_Handler(question, value)

		elif question == 'apt-setup/local0/repository':
			self.col_data_handler(question)

	def on_cellrenderertext_edited(self, cellrenderertext, path, text):
		question = cellrenderertext.question
		column_number = cellrenderertext.column_number
		treeselection = self.widgets_object_dict.get(f"treeselection_{self.naming(question)}")
		(model, iter) = treeselection.get_selected()
		if len(text) > 0:
			model[path][column_number] = text
			self.col_data_handler(question)

	def on_treeselection_changed(self, treeselection):
		question = treeselection.question
		(model, iter) = treeselection.get_selected()
		if question == "partman-auto/expert_recipe" or question == "apt-setup/local0/repository":
			if iter !=  None:
				self.widgets_object_dict.get(f'button_1_{self.naming(question)}').set_sensitive(1)

	def on_textbuffer_changed(self, textbuffer):
		question = textbuffer.question
		if question in ['pkgsel/include', 'debian-installer/add-kernel-opts']:
			start, end = textbuffer.get_bounds()
			value = textbuffer.get_text(start, end, include_hidden_chars = False).replace('\n', ' ')
			while '  ' in value:
				value = value.replace('  ', ' ')
			if len(value) <= 0 or value.isspace():
				value = 'delete'
			self.do_data_Handler(question ,value)

		elif question in ('preseed/run', 'preseed/late_command',):
			name = self.naming(question)
			button = self.widgets_object_dict.get(f'button_0_{name}')
			if button.get_sensitive() == False:
					button.set_sensitive(True)

	def set_buttons_sensitive(self, model_length, name):
		button_add = self.widgets_object_dict.get(f'button_0_{name}')
		button_remove_one = self.widgets_object_dict.get(f'button_1_{name}')
		button_remove_all = self.widgets_object_dict.get(f'button_2_{name}')

		if name == 'apt_setup_local0_repository':
			limited = f"limited additional repositories maximum {model_length}"
#
		elif name == 'partman_auto_expert_recipe':
			default_label = self.widgets_object_dict.get('comboboxtext_partman_partitioning_default_label').get_active_id()
			if default_label == None:
				self.widgets_object_dict.get('comboboxtext_partman_partitioning_default_label').set_active(1)
			default_label_text = self.widgets_object_dict.get('comboboxtext_partman_partitioning_default_label').get_active_text()
			limited = f"limited {default_label_text} maximum {model_length} partitions"

		if model_length == 4:
				if name == 'partman_auto_expert_recipe':
					if default_label != 'gpt':
						button_add.set_sensitive(False)
						self.log.info(limited)
						self.statusbar.push(self.statusbar_context_1, limited)

		elif model_length == 10:
			button_add.set_sensitive(False)
#			button_remove_one.set_sensitive(True)
			button_remove_all.set_sensitive(True)
			self.log.info(limited)
			self.statusbar.push(self.statusbar_context_1, limited)

		elif model_length == 0:
			button_add.set_sensitive(True)
			button_remove_one.set_sensitive(False)
			button_remove_all.set_sensitive(False)
			self.statusbar.pop(self.statusbar_context_1)
		else:
			button_add.set_sensitive(True)
		#	button_remove_one.set_sensitive(True)
			button_remove_all.set_sensitive(True)
			self.statusbar.pop(self.statusbar_context_1)

	def on_button_clicked(self, button, dialog=True):
		button_label = button.get_label()
#		button_name = button.get_name()
		question = button.question
		name = self.naming(question)

		if question in ('apt-setup/local0/repository', 'partman-auto/expert_recipe',):
			treeselection = self.widgets_object_dict.get(f"treeselection_{name}")
			(model, iter) = treeselection.get_selected()
			row_cell_index = self.widgets_object_dict.get(f"comboboxtext_{name}").get_active()
			row_cell_text = getattr(self, f"completed_text_{name}")[row_cell_index][1]

			if button_label == 'Add':
				if name == 'partman_auto_expert_recipe':
					disk = self.widgets_object_dict.get('comboboxtext_partman_auto_disk').get_active_id()
					if disk == None:
						self.widgets_object_dict.get('comboboxtext_partman_auto_disk').set_active(0)
						disk = self.widgets_object_dict.get('comboboxtext_partman_auto_disk').get_active_id()
					first_cell_text = disk
					add_number=1
				else:
					first_cell_text = 'local'
					add_number=0
				row = [first_cell_text  + str(len(model)+add_number), ] +list(row_cell_text)
				if iter is not None:
					model.insert_after(iter, row)
					for path in range(len(model)):
						model[path][0] = first_cell_text + str(path+add_number)
				else:
					model.append(row)

			elif button_label == 'Remove':
				if len(model) != 0:
					if iter is not None:
						self.log.info("%s has been removed" % (model[iter][0]))
						model.remove(iter)
						if name == 'partman_auto_expert_recipe':
							first_cell_text = self.widgets_object_dict.get('comboboxtext_partman_auto_disk').get_active_id()
							add_number=1
						else:
							first_cell_text = 'local'
							add_number=0
						for path in range(len(model)):
							model[path][0] = first_cell_text + str(path+add_number)

			elif button_label == 'Remove all':
				if len(model) != 0:
					for i in range(len(model)):
						iter = model.get_iter(0)
						local = (model[0][0])
						self.log.info("%s has been removed" % model[iter][0])
						model.remove(iter)

			self.set_buttons_sensitive(len(model), name)
			self.col_data_handler(question)

		elif question in ('preseed/run', 'preseed/late_command',):
			if button_label == 'Add':
				if question == "preseed/run":
					value = 'scripts/pre-installation-script.sh'

				elif question == "preseed/late_command":
					value = '[ "$file" ]&& sh /cdrom/preseed/scripts/post-installation-script.sh'
				button.set_label('Remove')

			elif button_label == 'Remove':
				value = 'delete'
				button.set_label('Add')

			elif button_label == 'Save':
				button.set_sensitive(False)
				if question == "preseed/run":
					script_file = self.settings.PRE_INSTALLATION_SCRIPT
					context = 'save_pre_script'
				elif question == "preseed/late_command":
					script_file = self.settings.POST_INSTALLATION_SCRIPT
					context = 'save_post_script'
				textbuffer = self.widgets_object_dict.get(f'textbuffer_{name}')
				start, end = textbuffer.get_bounds()
				text = textbuffer.get_text(start, end, include_hidden_chars = False)
				f = open(script_file, "w")
				f.write(text)
				f.close()
				if dialog:
					self.base_message_dialog('info', context, script_file)
			if button_label != 'Save':
				self.do_data_Handler(question, value)





