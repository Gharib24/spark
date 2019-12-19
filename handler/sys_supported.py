import os
class Locales_Zone_Info:
	def __init__(self):
		pass
	def __locales_supported(self):
		File = '/usr/share/i18n/SUPPORTED'
		self.locales_supported_list = []
		if not self.locales_supported_list:
			with open(File, "r") as f:
				for line in f:
#					self.locales_supported_list.append(line.strip())
					self.locales_supported_list.append([line.strip().split()[0], line.strip()])
				f.close

	def __zoneinfo(self):
		cmd = 'cd /usr/share/zoneinfo/posix && find * -type f -or -type l | sort && cd $PWD'
		self.zoneinfo_list = []
		for line in os.popen(cmd):
			self.zoneinfo_list.append(line.strip())

	def __Keyboard_layouts(self):
		File = '/usr/share/X11/xkb/rules/base.lst'
		self.layout_list = []
		layout = False
		if not self.layout_list:
			with open(File, "r") as f:
				for line in f:

					if '! layout' in line:
						layout = True
					elif'! variant' in line:
						break
					if layout == True:
						if '! layout' in line :
							continue
						elif not line.strip():
							continue
						else:
							alias = (line.strip().split()[0])
							name = ' '.join((line.strip(' ').split()[1:]))
							self.layout_list.append([alias, name])
					else:	
						continue
				f.close
	def locales_zone_info(self):
		self.__Keyboard_layouts()
		self.__zoneinfo()
		self.__locales_supported()


class Path:
	def __init__(self):
		pass

	def __dir(self):
		self.work_path = os.path.expanduser('~/spark/')
		self.scrpits_path = self.work_path+'cd-root/preseed/scripts/'
		self.grub_config_path = self.work_path+'cd-root/boot/grub/'
		self.isolinux_config_path  = self.work_path+'cd-root/isolinux/'
		for i, path in enumerate([self.scrpits_path, self.grub_config_path, self.isolinux_config_path], 0):
			if not os.path.exists(path):
				os.makedirs(path)

		self.cd_root = self.work_path+'cd-root/'
		self.preseed_path = self.cd_root+'preseed/'

	def files_dir(self):
		self.__dir()

		self.preseed_file = self.preseed_path+"spark.sk"
		self.pre_installation_script = self.scrpits_path+'pre-installation-script.sh'
		self.post_installation_script = self.scrpits_path+'post-installation-script.sh'
		self.config_file = self.work_path+".config"

		for i, file in enumerate([self.preseed_file, self.pre_installation_script, self.post_installation_script, self.config_file], 0):
			if not os.path.exists(file):
				f = open(file, "w")
				f.close()

		self.log_file = self.work_path+'.spark.log'
		self.isolinux_config_file = self.isolinux_config_path+'isolinux.cfg'
		self.grub_config_file = self.grub_config_path+'grub.cfg'


class Config:
	def __init__(self, config_file):
		self.config_file = config_file
		self.config_value = {}
		with open(self.config_file, "r") as f:
			for line in f:
				if not line.strip():
					continue
				else:
					_line = (line.strip())
					if len(_line) > 0:
						key = _line.split()[0]
						value = ' '.join(_line.split()[2:])
						self.config_value[key] = value
			f.close()

	def write(self, key=None,value=None):
		with open(self.config_file, 'w') as f:
			f.write("")
			f.close()
		self.config_value[key] = value
		with open(self.config_file, 'a') as f:
			for k, v in self.config_value.items():
				f.write('{}' ' = ' '{}\n'.format(k, v))
			f.close()

	def get(self, key=None):
		v = self.config_value.get(key)
		if v == 'True':
			value = True
		elif v == 'False':
			value = False
		else :
			value = v
		return value








