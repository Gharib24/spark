#!/usr/bin/python3.7
from template import *
questions_group_names = ['localization', 'account', 'network', 'partition', 'aptsources', 'software', 'bootloader' , 'finishup', 'command']
questions_template = [localization, account, network, partition, aptsources, software, bootloader, finishup, command]
lists =[]
all_questions = []
datastore = []
saved = 0
changed_field = []
deleted_field = []
add_field = []
data_state = []

for i, name in enumerate(questions_group_names, 0):
	list_name =  globals()[ name+'_questions'] = []
	lists.append(list_name)

if len(questions_template) == len(lists):
	for c, l in enumerate(questions_template, 0):
		for i in questions_template[c].splitlines():
			if '#' in i :
				continue
			elif not i.strip():
				continue
			else:
				lists[c].append(i.split()[1])
				all_questions.append(i.split()[1])
				datastore.append(i.split())

class DataStore(object):
	def set(self, question, value):
		if question in all_questions:
			self.question = question
			if value == 'delete':
				if len(datastore[all_questions.index(question)]) == 4:
					self.log.debug("{}: {}".format('remove value of ', question))
					datastore[all_questions.index(question)].pop(3)
					if question not in deleted_field:
						deleted_field.insert(0, question)
					if question in add_field:
						add_field.remove(question)
					if question in changed_field:
						changed_field.remove(question)

			elif len(datastore[all_questions.index(question)]) == 3:
				datastore[all_questions.index(question)].insert(3, value)
				self.log.debug("{}: {}".format('add value of ', question))
				if question not in add_field:
						add_field.insert(0, question)

			elif len(datastore[all_questions.index(question)]) == 4:
				datastore[all_questions.index(question)].pop(3)
				datastore[all_questions.index(question)].insert(3, value)
				self.log.debug("{}: {}".format('update value of ', question))
				if question not in changed_field:
					if question not in add_field:
						changed_field.insert(0, question)
				if question in deleted_field:
						deleted_field.remove(question)

			else:
				self.log.error('{}''{}''{}'.format('store error set ', question ,' out of range'))
		else:
			self.log.error('{}''{}''{}'.format('store error set ', question ,' not in lisut'))

	def get_answered(self):
		c = 0
		for i in range(len(datastore)):
			if len(datastore[i]) == 4:
				c +=1
		return c

	def get_total(self):
		c = 0
		for i in range(len(datastore)):
			if len(datastore[i]) > 1:
				c +=1
		return c

	def get(self, question):
		if  question  in all_questions:
			return  ' '.join(datastore[all_questions.index(question)])
		else:
			return 'store error get '+ question +' not in list'

class SaveToFile:
	def __init__(self):
		pass
	def save_to_file(self, caller, file):
		global saved
		global old_question
		global changed
		global field_changed
		changed = 0

		field_changed  = None
		saved = 0
		with open(file, 'w') as w: # XXX erase file
			w.write("# generated by spark *\n\n")
			w.close()

		with open(file , 'a') as a: # XXX writ to file
			for i in range(len(datastore)):
				if len(datastore[i]) == 4:
					line = (datastore[i][0], datastore[i][1], datastore[i][2],datastore[i][3])
					line = ' '.join(line)
					a.write(line+'\n')
					saved +=1
			a.close()	
			self.info_dialog('Saved successfully', "<a href='file://{0}'>file: {0} </a>".format(file))
			self.log.info("{} {}".format('Saved successfully', file))
			message = "all field saved {}".format(saved)
			self.statusbar.push(self.statusbar_context_1, message)

			changed_field.clear()
			deleted_field.clear()
			add_field.clear()
			data_state.clear()

	def get_changed_data(self):
		a = len(add_field)
		c = len(changed_field)
		d = len(deleted_field)
		if a+ c + d == 0:
			return None
		else:
			if a == 1:
				data_state.append(str(a)+' field unsaved')
			elif a > 1:
				data_state.append(str(a)+' fields unsaved')

			if c == 1:
				data_state.append(str(c)+' fields changed')
			elif c > 1:
				data_state.append(str(c)+' field changed')

			if d == 1:
				data_state.append(str(d)+' field deleted')
			elif d > 1:
				data_state.append(str(d)+' fields deleted')

			s = '  '.join(data_state)
			data_state.clear()
			return s






