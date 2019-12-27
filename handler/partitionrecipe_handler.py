#--------------------------------------------------------------------------------------------------
swap_line = '{sizes} {fstype} method{{ swap }} format{{ }} . '
efi_line = '{sizes} {fstype} method{{ efi }} format{{ }} $bootable{{ }} filesystem{{ {fstype} }} mountpoint{{ {mpoint} }} label{{ {label} }} . '
bios_boot_line = '{sizes} {fstype} method{{ biosgrub }} . '
else_line = '{sizes} {fstype} method{{ format }} format{{ }} use_filesystem{{ }} filesystem{{ {fstype} }} mountpoint{{ {mpoint} }} label{{ {label} }} . '
#--------------------------------------------------------------------------------------------------

class Handler:
	def __init__(self):
		pass

	def on_view_selection_changed_partition(self, treeselection):
		(model, iter) = treeselection.get_selected()
		if iter !=  None:
			self.remove_p.set_sensitive(True)

	def on_comboboxtext_changed_partition(self, comboboxtext):
		active_text = comboboxtext.get_active_text()
		(model, iter) = self.view_p_selection.get_selected()
		if iter !=  None:
			for i, text in enumerate(self.text_completed, 0):
				if (''.join(text[0])) == active_text:
					for col, text_completed in enumerate(self.text_completed[i][1], 1):
						(model[iter][col]) = text_completed
					self.to_recipe()
					break

	def text_edited_partition(self, widget, path, text, col):
		if col >= 1: 
			if len(text) > 0:
				#self.recipe_store[path][i] = int(float(text))
				self.recipe_store[path][col] = text
				self.to_recipe()


	def on_combo_changed_partition(self, widget, path, text, col):
		if col >= 1: 
			if len(text) > 0:
				if 'swap' in text:
					for _col, text_completed in enumerate(self.text_completed[3][1], 1):
						self.recipe_store[path][_col] = text_completed
				elif 'efi' in text:
					for _col, text_completed in enumerate(self.text_completed[2][1], 1):
						self.recipe_store[path][_col] = text_completed
				elif 'fat32' in text:
					for _col, text_completed in enumerate(self.text_completed[2][1], 1):
						self.recipe_store[path][_col] = text_completed
				elif 'free' in text:
					for _col, text_completed in enumerate(self.text_completed[1][1], 1):
						self.recipe_store[path][_col] = text_completed
				else:
					self.recipe_store[path][col] = text
				self.to_recipe()
		return True


	def on_button_clicked_partition(self, button, data=None):
		#XXX Add row
		name = button.get_label()
		if name == 'Add': 
			pt = self.id.get('partman-partitioning/default_label').get_active_id()
			self.disk = self.id.get('partman-auto/disk').get_active_id()
			if self.disk == None:
				self.disk = '/dev/sda'

			row = [self.disk + str(len(self.recipe_store)+1)] + self.text_completed[0][1]
			(model, iter) = self.view_p_selection.get_selected()
			if iter is not None:
				self.recipe_store.insert_after(iter, row)
				for path in range(len(self.recipe_store)):
					self.recipe_store[path][0] = self.disk + str(path+1)
			else:
				self.recipe_store.append(row)
			self.to_recipe()
			self.remove_p.set_sensitive(False)
			self.remove_all_p.set_sensitive(True)

			if len(self.recipe_store) == 4:
				if pt != 'gpt':
					self.log.info("limited")
					self.statusbar.push(self.statusbar_context_1,'limited msdos partition table maximum 4 partitions')
					self.add_p.set_sensitive(False)

			elif len(self.recipe_store) == 10:
				self.log.info("limited")
				self.statusbar.push(self.statusbar_context_1,'limited maximum 10 partitions')
				self.add_p.set_sensitive(False)
			else:
				self.add_p.set_sensitive(True)

		#XXX remove one row
		elif name == 'Remove':
			(model, iter) = self.view_p_selection.get_selected()
			if iter is not None:
				self.log.info("%s has been removed" % (model[iter][0]))
				self.recipe_store.remove(iter)
				for path in range(len(self.recipe_store)):
					self.recipe_store[path][0] = self.disk + str(path+1)
				self.to_recipe()
				self.add_p.set_sensitive(True)
				if len(self.recipe_store) == 0:
					self.remove_p.set_sensitive(False)
					self.remove_all_p.set_sensitive(False)
		#XXX remove all rows
		elif name == 'Remove All':
			if len(self.recipe_store) != 0:
			# remove all the entries in the model
				for i in range(len(self.recipe_store)):
					iter = self.recipe_store.get_iter(0)
					self.log.info("%s has been removed" % self.recipe_store[iter][0])
					self.recipe_store.remove(iter)
				self.to_recipe()
				self.add_p.set_sensitive(True)
				self.remove_p.set_sensitive(False)
				self.remove_all_p.set_sensitive(False)

	def to_recipe(self):
		emty_col = False
		spark_recipe = ''
		recipe = self.recipe_store
		if len(self.recipe_store) != 0:
			for row in range(len(recipe)):
				for col in range(1, 7):
					if recipe[row][col] == None:
						emty_col = True
						break

				if  emty_col != True:
					sizes = (' '.join(recipe[row][3, 4 , 5]))
					fstype = (''.join(recipe[row][1]))
					mpoint = (''.join(recipe[row][2]))
					label = (''.join(recipe[row][6]))
					if fstype == "linux-swap":
						line = swap_line.format(sizes=sizes, fstype=fstype )
					elif 'efi' in mpoint:
						line = efi_line.format(sizes=sizes, fstype=fstype, mpoint=mpoint, label=label)
					elif 'free' in fstype:
						line = bios_boot_line.format(sizes=sizes, fstype=fstype )
					else:
						line = else_line.format(sizes=sizes, fstype=fstype, mpoint=mpoint, label=label)
					spark_recipe  += line
					self.log.debug("{}:{}: {}".format(__name__ ,'spark recipe', spark_recipe))
					self.store_update('partman-auto/choose_recipe', 'spark_recipe')
					value =  'spark_recipe :: '+ spark_recipe
					key = 'partman-auto/expert_recipe'
					self.store_update(key, value)


					if recipe[row][2] == '/boot/efi':
						self.store_update('partman-efi/non_efi_system', 'false')
					else:
						self.store_update('partman-efi/non_efi_system', 'true')

		elif len(self.recipe_store)== 0:
			self.store_update('partman-auto/choose_recipe', 'delete')
			self.store_update('partman-auto/expert_recipe', 'delete')
			self.store_update('partman-efi/non_efi_system', 'delete')







