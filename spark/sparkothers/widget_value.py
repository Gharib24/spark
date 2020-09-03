#!/usr/bin/python3
import os
import pwd


class WidgetValue:
	def __init__(self):
		super().__init__()

		self.completed_text_partman_auto_expert_recipe = (
			(('Empty'), (None,None,None,None,None,None)),
			(('BIOS Boot Partition'), ('free','N/A', '1','1','1', 'N/A')),
			(('EFI System Partition'), ('fat32','/boot/efi', '537','537','537', 'ESP')),
			(('Swap Partition'), ('linux-swap','N/A', '50%','100%','100%', 'N/A')),
			(('Boot Partion'), ('ext4','/boot', '250','500','1000', 'boot')),
			(('Root Partition'), ('ext4','/', '10000','20000','30000', 'root')),
			(('Home Partition'), ('ext4','/home', '4000','8000','16000', 'home')),
			(('Data storage'), ('ext4','/mnt/storage', '4000','8000','16000', 'storage')),
		)

		self.completed_text_apt_setup_local0_repository = (
			(('Empty'), (None,None,None,False)),
			(('VirtualBox repository'),
				('deb [arch=amd64] http://download.virtualbox.org/virtualbox/debian buster contrib',
					'https://www.virtualbox.org/download/oracle_vbox_2016.asc',
					'VirtualBox',
				 False)
			),
			(('Google repository'),
			 ('deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main',
				 'http://dl.google.com/linux/linux_signing_key.pub',
				 'Google Chrome Browser',
				 False)
			)
		)

		self.tasksel_first=(
				('Debian desktop environment', 'desktop'),
				('Gnome desktop','gnome-desktop'),
				('Xfce desktop','xfce-desktop'),
				('KDE Plasma desktop','kde-desktop'),
				('Cinnamon desktop', 'cinnamon-desktop'),
				('MATE desktop', 'mate-desktop'),
				('LXDE desktop', 'lxde-desktop'),
				('LXQt desktop', 'lxqt-desktop'),
				('Web server', 'web-server'),
				('Print server', 'print-server'),
				('SSH server', 'ssh-server'),
				('Laptop', 'laptop'),
				('Standard tools', 'standard'),
			)

#-------------------------------------------------------------------------------

	def get_list_for_liststore_model(self, name):
		thislist = []
		if name =='debian_installer_locale' or name == 'localechooser_supported_locales':
			File = '/usr/share/i18n/SUPPORTED'
			with open(File, "r") as f:
				for line in f:
					thislist.append([line.strip()])
#					thislist.append([line.strip().split()[0], line.strip()])
				f.close

		elif name == 'keyboard_configuration_xkb_keymap':
			File = '/usr/share/X11/xkb/rules/base.lst'
			layout = False
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
							thislist.append([alias, name])
					else:
						continue
				f.close

		elif name == 'time_zone':
			cmd = 'cd /usr/share/zoneinfo/posix && find * -type f -or -type l | sort && cd $PWD'
			for line in os.popen(cmd):
				thislist.append(line.strip())

		elif name == 'tasksel_first':
			thistuple = self.tasksel_first
			thislist = list(thistuple)

		elif name == 'fullname':
			thislist = list((pwd.getpwuid(os.getuid())[4].replace(',,,', ''), os.environ.get('USER'),))
		elif name == 'username':
			thislist = list((os.environ.get('USER'),))
		elif name == 'groups':
			pass
#			with open('/etc/group', "r") as f:
#				new_list = []
#				for line in f:
#					new_list.append(line.split(':')[0])
#			thislist = new_list
		elif name == 'hostname':
			thislist = list((os.uname()[1], 'debian','localhost', 'test', 'server', 'desktop', 'pc'),)
		elif name == 'domain':
			thislist = list(('localdomain', 'local'),)
		elif name == 'ipaddress':
			thislist = list(('192.168.0.0', '172.16.0.0', '10.0.0.0'),)
		elif name == 'netmask':
			thislist = list(('255.255.0.0', '255.240.0.0', '255.0.0.0'),)
		elif name == 'gateway':
			thislist = list(('192.168.0.0', '172.16.0.0', '10.0.0.0'),)
		elif name == 'nameservers':
			thislist = list(('192.168.0.0', '172.16.0.0', '10.0.0.0'),)
#		else:
#			print(f"		elif name == '{name}':\n			pass")
		return thislist

#-------------------------------------------------------------------------------

	def get_title_for_treeview(self, name):
		partman_auto_expert_recipe=(
				'Part NO.', 'Filesystem type', 'Mount point', 'Min size (MB)', 'Priority size (MB)', 'Max size (MB) ','Label'
		)
		apt_setup_local0_repository = ('Repos NO.', 'Repository URL ', 'Public key URL', 'Comment', "Enable deb-src")
		localechooser_supported_locales =  ('Select', 'Locales')
		tasksel_first = ('Select', 'Tasksel')

		try:
			data = locals()[name]
			return data
		except NameError:
			self.log.error(NameError, name)
		except KeyError:
			self.log.error(KeyError, name)
		finally:
			del locals()[name]

	def get_value_for_comboboxtext(self, name):
		apt_setup_local0_repository = tuple(
			(str(i), self.completed_text_apt_setup_local0_repository[i][0],)
			for i in range(len(self.completed_text_apt_setup_local0_repository))
		)
		partman_auto_expert_recipe= tuple(
			(str(i), self.completed_text_partman_auto_expert_recipe[i][0],)
			for i in range(len(self.completed_text_partman_auto_expert_recipe))
		)
		partman_partitioning_default_label=(('gpt', 'GUID Partition Table'), ('msdos', 'Master Boot Record'))
		partman_auto_disk=(('/dev/sda', '/dev/sda'),('/dev/sdb', '/dev/sdb'), ('/dev/sdc', '/dev/sdc'))
		partman_mount_style=(('uuid', 'UUID'), ('label', 'Label'), ('name', 'Name'))
		partman_auto_choose_recipe=(
			('atomic', 'Automatic all files in one partition'),
			('home', 'Automatic separate /home partition'),
			('multi', 'Automatic  separate /home, /usr, /var, and /tmp partitions'),
			('spark_recipe', 'Custom partitioned recipe'),
		)
		partman_default_filesystem=(('ext4', "ext4"), ('ext3', "ext3"), ('ext2', "ext2"))
		mirror_http_hostname=(
				("http.us.debian.org", "http.us.debian.org"),
				("deb.debian.org", "deb.debian.org"),
				("ftp.debian.org", "ftp.debian.org"),
		)
		netcfg_choose_interface=(('auto', 'auto'), ('eth0', 'eth0'), ('wlan0', 'wlan0'))
		netcfg_wireless_security_type = (('wep/open', 'WEP/OPEN'), ('wpa', 'WPA'))
		netcfg_disable_dhcp = (('false', 'DHCP'),('true', 'Static IP'))
		grub_installer_bootdev = (('default', 'default'),) + partman_auto_disk
		pkgsel_upgrade = (("safe-upgrade", "Safe upgrade"), ("full-upgrade", "Full upgrade"), ("none", "None"))

		try:
			data = locals()[name]
			return data
		except NameError:
			self.log.error(self.whoami(), NameError, name)
		except KeyError:
			self.log.error(self.whoami(), KeyError, name)
			locals()[name] = ('test'), ('test')
			data = locals()[name]
			return data
		finally:
			del locals()[name]

#-------------------------------------------------------------------------------

	def get_label_text_for_button(self , name):
		tow_label_text = ('Save','Add')
		three_label_text=('Add','Remove', 'Remove all')
		partman_auto_expert_recipe = three_label_text
		apt_setup_local0_repository = three_label_text

		preseed_run = tow_label_text
		preseed_late_command = tow_label_text
		try:
			data = locals()[name]
			return data
		except NameError:
			self.log.error(self.whoami(), NameError, name)
		except KeyError:
			self.log.error(self.whoami(), KeyError, name)
		finally:
			del locals()[name]


