#!/usr/bin/env python3

localization=(
	{'owner': 'd-i', 'question': 'debian-installer/locale', 'type': 'string', 'answer': '', 'comment': 'Localization'},
	{'owner': 'd-i', 'question': 'debian-installer/language', 'type': 'string', 'answer': '', 'comment': ''},
	{'owner': 'd-i', 'question': 'debian-installer/country', 'type': 'string', 'answer': '', 'comment': ''},
	{'owner': 'd-i', 'question': 'keyboard-configuration/xkb-keymap', 'type': 'select', 'answer': '', 'comment': 'Keyboard'},
	{'owner': 'd-i', 'question': 'keyboard-configuration/toggle', 'type': 'select', 'answer': '', 'comment': ''},

	{'owner': 'd-i', 'question': 'keyboard-configuration/layoutcode', 'type': 'multiselect', 'answer': '', 'comment': ''},
		{'owner': 'd-i', 'question': 'localechooser/supported-locales', 'type': 'multiselect', 'answer': '', 'comment': 'Locales'},
	{'owner': 'd-i', 'question': 'time/zone', 'type': 'select', 'answer': '', 'comment': 'Time'},
	{'owner': 'd-i', 'question': 'clock-setup/utc', 'type': 'boolean', 'answer': '', 'comment': ''},
	{'owner': 'd-i', 'question': 'clock-setup/ntp', 'type': 'boolean', 'answer': '', 'comment': ''},
)

account=(
	{'owner': 'd-i', 'question': 'passwd/user-fullname', 'type': 'string', 'answer': '', 'comment': 'User account'},
	{'owner': 'd-i', 'question': 'passwd/username', 'type': 'string', 'answer': '', 'comment': ''},
	{'owner': 'd-i', 'question': 'passwd/user-password-crypted', 'type': 'password', 'answer': '', 'comment': ''},
	{'owner': 'd-i', 'question': 'passwd/user-default-groups', 'type': 'string', 'answer': '', 'comment': 'User groups'},
	{'owner': 'd-i', 'question': 'passwd/root-login', 'type': 'boolean', 'answer': '', 'comment': 'Root account'},
	{'owner': 'd-i', 'question': 'passwd/root-password-crypted', 'type': 'password', 'answer': '', 'comment': ''},
)

network=(
	{'owner': 'd-i', 'question': 'netcfg/get_hostname', 'type': 'string', 'answer': '', 'comment': 'Network'},
	{'owner': 'd-i', 'question': 'netcfg/get_domain', 'type': 'string', 'answer': '', 'comment': ''},
	{'owner': 'd-i', 'question': 'netcfg/choose_interface', 'type': 'select', 'answer': '', 'comment': ''},
	{'owner': 'd-i', 'question': 'netcfg/wireless_security_type', 'type': 'select', 'answer': '', 'comment': ''},
	{'owner': 'd-i', 'question': 'netcfg/wireless_essid', 'type': 'string', 'answer': '', 'comment': ''},
	{'owner': 'd-i', 'question': 'netcfg/wireless_essid_again', 'type': 'string', 'answer': '', 'comment': ''},
	{'owner': 'd-i', 'question': 'netcfg/wireless_wep', 'type': 'string', 'answer': '', 'comment': ''},
	{'owner': 'd-i', 'question': 'netcfg/wireless_wpa', 'type': 'string', 'answer': '', 'comment': ''},
	{'owner': 'd-i', 'question': 'netcfg/disable_dhcp', 'type': 'boolean', 'answer': '', 'comment': ''},
	{'owner': 'd-i', 'question': 'netcfg/confirm_static', 'type': 'boolean', 'answer': '', 'comment': ''},
	{'owner': 'd-i', 'question': 'netcfg/get_ipaddress', 'type': 'string', 'answer': '', 'comment': 'IPv4'},
	{'owner': 'd-i', 'question': 'netcfg/get_netmask', 'type': 'string', 'answer': '', 'comment': ''},
	{'owner': 'd-i', 'question': 'netcfg/get_gateway', 'type': 'string', 'answer': '', 'comment': ''},
	{'owner': 'd-i', 'question': 'netcfg/get_nameservers', 'type': 'string', 'answer': '', 'comment': ''},
	{'owner': 'd-i', 'question': 'netcfg/confirm_static', 'type': 'boolean', 'answer': '', 'comment': ''},
	{'owner': 'd-i', 'question': 'anna/choose_modules', 'type': 'string', 'answer': '', 'comment': ''},
	{'owner': 'd-i', 'question': 'network-console/password', 'type': 'password', 'answer': '', 'comment': 'Network console'},
	{'owner': 'd-i', 'question': 'network-console/password-again', 'type': 'password', 'answer': '', 'comment': ''},
)

partition=(
	{'owner': 'd-i', 'question': 'partman-auto/disk', 'type': 'string', 'answer': '', 'comment': 'Partitioning'},
	{'owner': 'd-i', 'question': 'partman-partitioning/default_label', 'type': 'select', 'answer': '', 'comment': ''},
	{'owner': 'd-i', 'question': 'partman/mount_style', 'type': 'select', 'answer': '', 'comment': ''},
	{'owner': 'd-i', 'question': 'partman-auto/choose_recipe', 'type': 'select', 'answer': '', 'comment': ''},
	{'owner': 'd-i', 'question': 'partman/default_filesystem', 'type': 'string', 'answer': '', 'comment': ''},
	{'owner': 'd-i', 'question': 'partman/early_command', 'type': 'string', 'answer': '', 'comment': ''},
	{'owner': 'd-i', 'question': 'partman-efi/non_efi_system', 'type': 'boolean', 'answer': '', 'comment': ''},
	{'owner': 'd-i', 'question': 'partman-auto/method', 'type': 'string', 'answer': '', 'comment': ''},
	{'owner': 'd-i', 'question': 'partman-auto/purge_lvm_from_device', 'type': 'boolean', 'answer': '', 'comment': ''},
	{'owner': 'd-i', 'question': 'partman-partitioning/confirm_write_new_label', 'type': 'boolean', 'answer': '', 'comment': ''},
	{'owner': 'd-i', 'question': 'partman/choose_partition', 'type': 'select', 'answer': '', 'comment': ''},
	{'owner': 'd-i', 'question': 'partman/confirm_write_new_label', 'type': 'boolean', 'answer': '', 'comment': ''},
	{'owner': 'd-i', 'question': 'partman/confirm_nooverwrite', 'type': 'boolean', 'answer': '', 'comment': ''},
	{'owner': 'd-i', 'question': 'partman/confirm', 'type': 'boolean', 'answer': '', 'comment': ''},
	{'owner': 'd-i', 'question': 'partman-auto/expert_recipe', 'type': 'string', 'answer': '', 'comment': 'Partitioning recipe'},
)
aptsources=(
	{'owner': 'd-i', 'question': 'mirror/country', 'type': 'string', 'answer': '', 'comment': 'Mirror'},
	{'owner': 'd-i', 'question': 'mirror/http/hostname', 'type': 'string', 'answer': '', 'comment': 'Mirror'},
	{'owner': 'd-i', 'question': 'mirror/http/directory', 'type': 'string', 'answer': '', 'comment': ''},
	{'owner': 'd-i', 'question': 'mirror/http/proxy', 'type': 'string', 'answer': '', 'comment': ''},
	{'owner': 'd-i', 'question': 'apt-setup/security_host', 'type': 'string', 'answer': '', 'comment': 'Apt setup'},
	{'owner': 'd-i', 'question': 'apt-setup/volatile_host', 'type': 'string', 'answer': '', 'comment': ''},
	{'owner': 'd-i', 'question': 'apt-setup/services-select', 'type': 'multiselect', 'answer': '', 'comment': ''},
	{'owner': 'd-i', 'question': 'apt-setup/contrib', 'type': 'boolean', 'answer': '', 'comment': ''},
	{'owner': 'd-i', 'question': 'apt-setup/non-free', 'type': 'boolean', 'answer': '', 'comment': ''},
	{'owner': 'd-i', 'question': 'apt-setup/use_mirror', 'type': 'boolean', 'answer': '', 'comment': ''},
	{'owner': 'apt-cdrom-setup', 'question': 'apt-setup/cdrom/set-first', 'type': 'boolean', 'answer': '', 'comment': 'Do not scan for another cd'},
	{'owner': 'd-i', 'question': 'apt-setup/disable-cdrom-entries', 'type': 'boolean', 'answer': '', 'comment': "Remove the installation DVD from the apt-get's sources.list"},
)

thislist = []
for i in range(0, 10):
	if i == 0:
		comment = 'Additional repositories 0~9'
	else:
		comment = ''
	thislist.append({'owner': 'd-i', 'question': 'apt-setup/local'+str(i)+'/comment', 'type': 'string', 'answer': '', 'comment': comment},)
	thislist.append({'owner': 'd-i', 'question': 'apt-setup/local'+str(i)+'/source' , 'type': 'boolean', 'answer': '', 'comment': ''},)
	thislist.append({'owner': 'd-i', 'question': 'apt-setup/local'+str(i)+'/repository', 'type': 'string', 'answer': '', 'comment': ''},)
	thislist.append({'owner': 'd-i', 'question': 'apt-setup/local'+str(i)+'/key', 'type': 'string', 'answer': '', 'comment': ''},)
additional_repositories=tuple(thislist)
del thislist

software=(
	{'owner': 'tasksel', 'question': 'tasksel/first', 'type': 'multiselect', 'answer': '', 'comment': 'Software selection'},
	{'owner': 'd-i', 'question': 'pkgsel/include', 'type': 'string', 'answer': '', 'comment': 'Individual additional packages to install'},
	{'owner': 'd-i', 'question': 'pkgsel/upgrade', 'type': 'select', 'answer': '', 'comment': ''},
	{'owner': 'popularity-contest', 'question': 'popularity-contest/participate', 'type': 'boolean', 'answer': '', 'comment': ' Disable popularity-contest'},
)

bootloader=(
	{'owner': 'd-i', 'question': 'lilo-installer/skip', 'type': 'boolean', 'answer': '', 'comment': 'Lilo bootloader settings'},
	{'owner': 'd-i', 'question': 'grub-installer/bootdev', 'type': 'string', 'answer': '', 'comment': 'Grub bootloader settings'},
	{'owner': 'd-i', 'question': 'grub-installer/only_debian', 'type': 'boolean', 'answer': '', 'comment': ''},
	{'owner': 'd-i', 'question': 'grub-installer/with_other_os', 'type': 'boolean', 'answer': '', 'comment': ''},
	{'owner': 'd-i', 'question': 'grub-installer/force-efi-extra-removable', 'type': 'boolean', 'answer': '', 'comment': 'EFI extra removable'},
	{'owner': 'd-i', 'question': 'debian-installer/add-kernel-opts', 'type': 'string', 'answer': '', 'comment': 'Kernel boot parameters'},
)

finishup=(
	{'owner': 'd-i', 'question': 'cdrom-detect/eject', 'type': 'boolean', 'answer': '', 'comment': 'Ejecting the CD during the reboot,'},
	{'owner': 'd-i', 'question': 'finish-install/reboot_in_progress', 'type': 'note', 'answer': '', 'comment': 'Avoid that last message about the install being complete.'},
	{'owner': 'd-i', 'question': 'debian-installer/exit/halt', 'type': 'boolean', 'answer': '', 'comment': 'Halt the system'},
	{'owner': 'd-i', 'question': 'debian-installer/exit/poweroff', 'type': 'boolean', 'answer': '', 'comment': 'Power off the machine'},
)

scrpit=(
	{'owner': 'd-i', 'question': 'preseed/run', 'type': 'string', 'answer': '', 'comment': 'Pre-installation script'},
	{'owner': 'd-i', 'question': 'preseed/late_command', 'type': 'string', 'answer': '', 'comment': 'This command is run commands in the target system.'},
)

preseed_questions_identifier =(
	localization
	+account
	+network
	+partition
	+aptsources
	+additional_repositories
	+software
	+bootloader
	+finishup
	+scrpit
)



















