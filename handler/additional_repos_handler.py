class Handler:
	def __init__(self):
		super().__init__()

	def on_view_selection_changed_repos(self, treeselection):
		(model, iter) = treeselection.get_selected()
		if iter !=  None:
			rownumobj = model.get_path(iter)
			liststore_length = len(self.repos_store)
			intrownum = int(rownumobj.to_string())
			intrownum +=1
			if intrownum  == liststore_length:
				self.remove_r.set_sensitive(True)
			else:
				self.remove_r.set_sensitive(False)

	def on_comboboxtext_changed_repos(self, comboboxtext):
		active_text = comboboxtext.get_active_text()
		(model, iter) = self.view_selection_r.get_selected()
		if iter !=  None:
			for i, text in enumerate(self.local_repos, 0):
				if (''.join(text[0])) == active_text:
					for col, text_completed in enumerate(self.local_repos[i][1], 1):
						(model[iter][col]) = text_completed
					self.to_repos()
					break



	def text_edited_repos(self, widget, path, text, col):
		if col >= 1: 
			if len(text) > 0:
				#self.repos_store[path][i] = int(float(text))
				self.repos_store[path][col] = text
				self.to_repos()

	def on_cell_toggled_repos(self, widget, path):
		self.repos_store[path][4] = not self.repos_store[path][4]
		self.to_repos()


	def on_button_clicked_repos(self, button, data=None):
		name = button.get_label()
		#XXX Add row
		if name == 'Add':
			row = ['local' + str(len(self.repos_store))] + self.local_repos[0][1]
			self.repos_store.append(row)
			self.to_repos()
#			self.comboboxtext_add_r.set_active(0)
			self.remove_r.set_sensitive(False)
			self.remove_all_r.set_sensitive(True)
			if len(self.repos_store) == 10:
				self.log.info("limited additional repositories maximum 10")
				self.statusbar.push(self.statusbar_context_1,'limited additional repositories maximum 10')
				self.add_r.set_sensitive(False)
			else:
				self.add_r.set_sensitive(True)


		#XXX remove one row
		elif name == 'Remove':
			if len(self.repos_store) != 0:
				(model, iter) = self.view_selection_r.get_selected()
				if iter is not None:
					local = (model[iter][0])
					self.log.info("%s has been removed" % local)
					self.repos_store.remove(iter)
					for i, name in enumerate(['repository', 'comment', 'source', 'key'], 0):
						self.store_update('apt-setup/'+local+'/'+name, 'delete')
				if len(self.repos_store) == 0:
					self.add_r.set_sensitive(True)
					self.remove_r.set_sensitive(False)
					self.remove_all_r.set_sensitive(False)
		#XXX remove all rows
		elif name == 'Remove All':
			if len(self.repos_store) != 0:
			# remove all the entries in the model
				for i in range(len(self.repos_store)):
					iter = self.repos_store.get_iter(0)
					local = (self.repos_store[0][0])
					for i, name in enumerate(['repository', 'comment', 'source', 'key'], 0):
						self.store_update('apt-setup/'+local+'/'+name, 'delete')
					self.repos_store.remove(iter)
				self.add_r.set_sensitive(True)
				self.remove_r.set_sensitive(False)
				self.remove_all_r.set_sensitive(False)


	def to_repos(self):
		emty_col = False
		if len(self.repos_store) != 0:
			for row in range(len(self.repos_store)):
				for col in range(1, 3):
					if self.repos_store[row][col] == None:
						emty_col = True
						break
				if  emty_col != True:
					local = self.repos_store[row][0]
					repository = self.repos_store[row][1]
					public_key = self.repos_store[row][2]
					comment = self.repos_store[row][3]
					deb_source =  str(self.repos_store[row][4]).lower()
					for name, value  in zip(['repository', 'comment', 'source', 'key'], [repository, comment, deb_source, public_key]):
						self.store_update('apt-setup/'+local+'/'+name , value)

