#!/usr/bin/python3
from spark.sparkothers import settings

class Config:
	def __init__(self):
		self.config_dict = {}
		self.read_config()

	def read_config(self):
		with open(settings.CONFIG_FILE, "r") as f:
			for line in f:
				if not line.strip():
					continue
				elif line.startswith('#'):
					continue
				else:
					key_value = (line.strip())
					if len(key_value) > 0:
						key = key_value.split()[0]
						value = key_value.split()[2:]
						value = ' '.join(value).replace("\"", "")
						self.config_dict[key] = value
			f.close()

	def write_config(self):
		with open(settings.CONFIG_FILE, 'w') as f:
			f.write(f"# {settings.APP_NAME} config\n\n")
			f.close()

		with open(settings.CONFIG_FILE, 'a') as f:
			for kay, value in self.config_dict.items():
				f.write(f"{kay} = \"{value}\"\n")
			f.close()

	def set_config(self, key, *value):
		if len(value) == 0:
			if key in self.config_dict.keys():
				self.config_dict.pop(key)
		else:
			value = ' '.join(map(str, value))
			self.config_dict[key] = value
		self.write_config()

	def get_config(self, key=None):
		if key != None:
			value = self.config_dict.get(key)
			return value
		else:
			return None


if __name__ == "__main__":
	config = Config()
	config.set_config('Ahmad', 'ag', 'spark')
	print(config.get_config('Ahmad'))
	print(config.get_config('Ali'))


