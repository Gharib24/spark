#!/usr/bin/env python

SWAP_LINE = '{SIZES} {FSTYPE} method{{ swap }} format{{ }} .'
EFI_LINE = '{SIZES} {FSTYPE} method{{ efi }} format{{ }} $bootable{{ }} filesystem{{ {FSTYPE} }} mountpoint{{ {MPOINT} }} label{{ {LABEL} }} .'
BIOS_BOOT_LINE = '{SIZES} {FSTYPE} method{{ biosgrub }} .'
ELSE_LINE = '{SIZES} {FSTYPE} method{{ format }} format{{ }} use_filesystem{{ }} filesystem{{ {FSTYPE} }} mountpoint{{ {MPOINT} }} label{{ {LABEL} }} .'


class Handler:
	def __init__(self):
		pass

	def col_data_handler(self, question):
		name = self.naming(question)
		if name == 'partman_auto_expert_recipe':
			self.partition_recipe_data_handler(name)
		elif name == 'apt_setup_local0_repository':
			self.local_repository_data_handler(name)
		else:
			self.log.warn(name)

	def local_repository_data_handler(self, name):
		liststore = self.widgets_object_dict.get(f"liststore_{name}")
		emty_col = False

		if len(liststore) > 0:
			for row in range(len(liststore)):
				for col in range(1, 3):
					if liststore[row][col] == None:
						emty_col = True
						break
				if emty_col != True:
					local = liststore[row][0]
					repository = liststore[row][1]
					public_key = liststore[row][2]
					comment = liststore[row][3]
					deb_source =  str(liststore[row][4]).lower()
					for name, value  in zip(['repository', 'comment', 'source', 'key'], [repository, comment, deb_source, public_key]):
						self.do_data_Handler('apt-setup/'+local+'/'+name , value)

			for local in range(len(liststore), 10):
				for i, name in enumerate(['repository', 'comment', 'source', 'key'], 0):
					answer = self.get_answer_question(f'apt-setup/local{local}/{name}')
					if answer != None:
						self.do_data_Handler(f'apt-setup/local{local}/{name}', 'delete')

		elif len(liststore) == 0:
			for local in range(0, 10):
				for i, name in enumerate(['repository', 'comment', 'source', 'key'], 0):
					answer = self.get_answer_question(f'apt-setup/local{local}/{name}')
					if answer != None:
						self.do_data_Handler(f'apt-setup/local{local}/{name}', 'delete')

	def partition_recipe_data_handler(self, name):
		liststore = self.widgets_object_dict.get(f"liststore_{name}")
		emty_col = False
		spark_recipe = ''
		if len(liststore) != 0:
			for row in range(len(liststore)):
				for col in range(1, 7):
					if liststore[row][col] == None:
						emty_col = True
						break

				if emty_col != True:
					whitespace = " "
					sizes = (' '.join(liststore[row][3, 4 , 5])).strip()
					fstype = (''.join(liststore[row][1])).strip()
					mpoint = (''.join(liststore[row][2])).strip()
					label = (''.join(liststore[row][6])).strip()
					if fstype == "linux-swap":
						line = SWAP_LINE.format(SIZES=sizes, FSTYPE=fstype)
					elif 'efi' in mpoint:
						line = EFI_LINE.format(SIZES=sizes, FSTYPE=fstype, MPOINT=mpoint, LABEL=label)
					elif 'free' in fstype:
						line = BIOS_BOOT_LINE.format(SIZES=sizes, FSTYPE=fstype )
					else:
						line = ELSE_LINE.format(SIZES=sizes, FSTYPE=fstype, MPOINT=mpoint, LABEL=label)
					spark_recipe += whitespace+line
					value = 'spark_recipe ::'+spark_recipe
					name = 'partman-auto/expert_recipe'
					self.do_data_Handler(name, value)

					if 'efi' in spark_recipe:
						self.do_data_Handler('partman-efi/non_efi_system', 'false')
					else:
						self.do_data_Handler('partman-efi/non_efi_system', 'true')

		elif len(liststore)== 0:
			self.do_data_Handler('partman-auto/choose_recipe', 'delete')
			self.do_data_Handler('partman-auto/expert_recipe', 'delete')
			self.do_data_Handler('partman-efi/non_efi_system', 'delete')


