category = [("Basic Options"),
	("User Settings"),
	("Network Configuration"),
	("Partition Information"),
	("Apt Sources Configuration"),
	("Package Selection"),
	("Boot Loader Options"),
	("Pre-Installation Script"),
	("Post-Installation Script"),
	("Finishing up the installation")
	]
#category.append(("Network Console")) # Installer over ssh
#category.append(("Create an ISO image"))

s = '-symbolic'
s = ''
category_icons = {
	"User Settings": f'system-users{s}',
	"Network Configuration": f'preferences-system-network{s}',
	"Basic Options": f'preferences-desktop-locale{s}',
	"Partition Information": f'drive-harddisk{s}',
	"Apt Sources Configuration": f'software-update-available{s}',
	"Package Selection": f'system-software-install{s}',
	"Boot Loader Options": f'system-run{s}',
	"Pre-Installation Script": f'application-x-executable{s}',
	"Post-Installation Script": f'application-x-executable{s}',
	"Network Console": f'utilities-terminal{s}',
	"Create an ISO image": f'media-optical{s}',
	"Finishing up the installation": f'system-shutdown{s}',
}

account = (
	{'question': 'passwd/user-fullname', 'label_text': 'Full name', 'widget_type': 'entry'},
	{'question': 'passwd/username', 'label_text': 'Username', 'widget_type': 'entry'},
	{'question': 'passwd/user-password-crypted', 'label_text': 'User password', 'widget_type': 'entry'},
	{'question': 'passwd/user-default-groups', 'label_text': 'User default groups', 'widget_type': 'entry'},
	{'question': 'passwd/root-login', 'label_text': 'Disable the root login', 'widget_type': 'checkbutton'},
	{'question': 'passwd/root-password-crypted', 'label_text': 'Root password', 'widget_type': 'entry'},
)

network = (
	{'question': 'netcfg/get_hostname', 'label_text': 'Hostname', 'widget_type': 'entry'},
	{'question': 'netcfg/get_domain', 'label_text': 'Domain', 'widget_type': 'entry'},
	{'question': 'netcfg/choose_interface', 'label_text': 'Interface', 'widget_type': 'comboboxtext_with_entry'},
	{'question': 'netcfg/wireless_security_type', 'label_text': 'Wireless Security Type', 'widget_type': 'comboboxtext'},
	{'question': 'netcfg/wireless_essid', 'label_text': 'Wireless SSID', 'widget_type': 'entry'},
	{'question': 'netcfg/wireless_wep', 'label_text': 'Wireless WEP Security Key', 'widget_type': 'entry'},
#	{'question': 'netcfg/wireless_wpa', 'label_text': 'Wireless WPA Security Key', 'widget_type': 'entry'},
	{'question': 'netcfg/disable_dhcp', 'label_text': 'IP4 Method', 'widget_type': 'comboboxtext'},
	{'question': 'netcfg/get_ipaddress', 'label_text': 'IP Address', 'widget_type': 'entry'},
	{'question': 'netcfg/get_netmask', 'label_text': 'Netmask', 'widget_type': 'entry'},
	{'question': 'netcfg/get_gateway', 'label_text': 'Gateway', 'widget_type': 'entry'},
	{'question': 'netcfg/get_nameservers', 'label_text': 'Name Servers', 'widget_type': 'entry'},
)

network_console = (
	{'question': 'network-console/password', 'label_text': 'Network console password', 'widget_type': 'entry'},
	{'question': 'network-console/password-again', 'label_text': 'Network console password again', 'widget_type': 'entry'},
)

localization = (
	{'question': 'debian-installer/locale', 'label_text': 'Locale', 'widget_type': 'combobox'},
	{'question': 'debian-installer/language', 'label_text': 'Language code', 'widget_type': 'entry'},
	{'question': 'debian-installer/country', 'label_text': 'Country code', 'widget_type': 'entry'},
	{'question': 'keyboard-configuration/xkb-keymap', 'label_text': 'Default keyboard language', 'widget_type': 'combobox'},
	{'question': 'keyboard-configuration/layoutcode', 'label_text': 'Keyboard multi language code', 'widget_type': 'entry'},
	{'question': 'keyboard-configuration/toggle', 'label_text': 'Keyboard toggle', 'widget_type': 'entry'},
	{'question': 'localechooser/supported-locales', 'label_text': 'Language Support', 'widget_type': 'treeview'},
	{'question': 'time/zone', 'label_text': 'Time zone', 'widget_type': 'combobox'},
	{'question': 'clock-setup/utc', 'label_text': 'Set Hardware clock to UTC', 'widget_type': 'checkbutton'},
	{'question': 'clock-setup/ntp', 'label_text': 'Use NTP to set the clock during the install', 'widget_type': 'checkbutton'},
)

partition =(
	{'question': 'partman-auto/disk', 'label_text': 'Disk', 'widget_type': 'comboboxtext_with_entry'},
	{'question': 'partman-partitioning/default_label', 'label_text': 'Partition table', 'widget_type': 'comboboxtext'},
	{'question': 'partman/mount_style', 'label_text': 'Mount style', 'widget_type': 'comboboxtext'},
	{'question': 'partman-auto/choose_recipe', 'label_text': 'Partition recipe', 'widget_type': 'comboboxtext'},
	{'question': 'partman/default_filesystem', 'label_text': 'Default filesystem', 'widget_type': 'comboboxtext_with_entry'},
	{'question': 'partman-auto/expert_recipe', 'label_text': 'Partitioned recipe.', 'container_type': 'frame'},
)
aptsources =(
	{'question': 'mirror/http/hostname', 'label_text': 'Official Debian mirror', 'widget_type': 'comboboxtext_with_entry'},
	{'question': 'mirror/http/directory', 'label_text': 'Mirror directory', 'widget_type': 'entry'},
#	{'question': 'mirror/http/proxy', 'label_text': 'Hostname', 'widget_type': 'disable'},
	{'question': 'apt-setup/security_host', 'label_text': 'Security host', 'widget_type': 'entry'},
#	{'question': 'apt-setup/volatile_host', 'label_text': 'Volatile host', 'widget_type': 'entry'},
	{'question': 'apt-setup/services-select0', 'label_text': 'Security services', 'widget_type': 'checkbutton'},
	{'question': 'apt-setup/services-select1', 'label_text': 'Updates services', 'widget_type': 'checkbutton'},
	{'question': 'apt-setup/services-select2', 'label_text': 'Volatile services', 'widget_type': 'checkbutton'},
	{'question': 'apt-setup/contrib', 'label_text': 'contrib software', 'widget_type': 'checkbutton'},
	{'question': 'apt-setup/non-free', 'label_text': 'non-free software', 'widget_type': 'checkbutton'},
	{'question': 'apt-setup/use_mirror', 'label_text': 'Use a network mirror', 'widget_type': 'checkbutton'},
#	{'question': 'apt-setup/cdrom/set-first', 'label_text': 'Disable scan for another CD', 'widget_type': 'checkbutton'},
	{'question': 'apt-setup/disable-cdrom-entries', 'label_text': "Remove the installation DVD from the apt-get's sources.list", 'widget_type': 'checkbutton'},
	{'question': 'apt-setup/local0/repository', 'label_text': 'Additional repositories 0~9 available.', 'container_type': 'frame'},
)

software = (
	{'question': 'tasksel/first', 'label_text': 'Install software', 'widget_type': 'treeview'},
	{'question': 'pkgsel/include', 'label_text': 'Install additional packages', 'widget_type': 'textview'},
	{'question': 'pkgsel/upgrade', 'label_text': 'Upgrade packages', 'widget_type': 'comboboxtext'},
#	{'question': 'popularity-contest/participate', 'label_text': 'Disable popularity-contest', 'widget_type': 'checkbutton'},
)

bootloader = (
	{'question': 'debian-installer/add-kernel-opts', 'label_text': 'Kernel boot parameters', 'widget_type': 'entry'},
	{'question': 'grub-installer/bootdev', 'label_text': 'Install Grub on device', 'widget_type': 'comboboxtext_with_entry'},
	{'question': 'grub-installer/only_debian', 'label_text': 'Only Debian', 'widget_type': 'checkbutton'},
	{'question': 'grub-installer/with_other_os', 'label_text': 'Detected other OS on the machine', 'widget_type': 'checkbutton'},
	{'question': 'grub-installer/force-efi-extra-removable', 'label_text': 'EFI extra removable', 'widget_type': 'checkbutton'},
#	{'question': 'lilo-installer/skip', 'label_text': 'Install Lilo bootloader instead of Grub bootloader', 'widget_type': 'checkbutton'},
)
finishup=(
	{'question': 'cdrom-detect/eject', 'label_text': 'Ejecting the CD during the reboot', 'widget_type': 'checkbutton'},
	{'question': 'finish-install/reboot_in_progress', 'label_text': 'Avoid that last message about the install being complete', 'widget_type': 'checkbutton'},
#	{'question': 'debian-installer/exit/halt', 'label_text': 'Halt the system', 'widget_type': 'checkbutton'},
	{'question': 'debian-installer/exit/poweroff', 'label_text': 'Power off the machine', 'widget_type': 'checkbutton'},
)
pre_installation_script = (
	{'question': 'preseed/run', 'label_text': None, 'container_type': 'scripting'},
)

late_command = (
	{'question': 'preseed/late_command', 'label_text': None, 'container_type': 'scripting'},
)

rebuild = (
	{'question': 'rebuild-select-iso-file', 'label_text': 'Select source Debian ISO file', 'widget_type': 'filechooserbutton'},
	{'question': 'rebuild-enter-file-name', 'label_text': 'File name', 'widget_type': 'entry'},
	{'question': 'rebuild-select-foldar', 'label_text': 'Safe in Foldar', 'widget_type': 'filechooserbutton'},
	{'question': 'rebuild-create-iso-file', 'label_text': 'Start create ISO file', 'widget_type': 'button'},
	{'question': 'rebuild-label', 'label_text': None, 'widget_type': 'label'},
	{'question': 'rebuild-spinner', 'label_text': 'spinner', 'widget_type': 'spinner'},
	{'question': 'rebuild-progressbar', 'label_text': 'job', 'widget_type': 'progressbar'},
)

separator = {"User Settings":(2, 3,),
	"Network Configuration":(2, 5),
	"Basic Options": (2, 5, 6),
	"Apt Sources Configuration": (12,),
	"Package Selection": (6,),
	"Boot Loader Options":(0,),
	"Network Console":(),
	"Create an ISO image":(2,),
}

stack_components = {
	"User Settings": account,
	"Network Configuration": network,
	"Basic Options": localization,
	"Partition Information": partition,
	"Apt Sources Configuration": aptsources,
	"Package Selection": software,
	"Boot Loader Options": bootloader,
	"Pre-Installation Script": pre_installation_script,
	"Post-Installation Script": late_command,
	"Network Console": network_console,
	"Finishing up the installation":finishup,
	"Create an ISO image": rebuild,
}

dialog_components = {
	"Create an ISO image": rebuild,
}




