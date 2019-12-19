localization = """
### Localization
d-i debian-installer/locale string
d-i debian-installer/language string
d-i debian-installer/country string

## Keyboard
d-i keyboard-configuration/xkb-keymap select
d-i keyboard-configuration/layoutcode multiselect
d-i keyboard-configuration/toggle select

# Optionally specify additional locales to be generated.
d-i localechooser/supported-locales multiselect

### Time
d-i time/zone select
d-i clock-setup/utc boolean
d-i clock-setup/ntp boolean
"""
account = """
## User
d-i passwd/user-fullname string
d-i passwd/username string
d-i passwd/user-password-crypted password

## Groups
d-i passwd/user-default-groups string

d-i passwd/root-login boolean
d-i passwd/root-password-crypted password
"""

network = """
### Network
d-i netcfg/get_hostname string
d-i netcfg/get_domain string

d-i netcfg/choose_interface select

d-i netcfg/wireless_security_type select
d-i netcfg/wireless_essid string
d-i netcfg/wireless_essid_again string

d-i netcfg/wireless_wep string
d-i netcfg/wireless_wpa string

d-i netcfg/disable_autoconfig string
d-i netcfg/confirm_static boolean

### IPv4
d-i netcfg/get_ipaddress string
d-i netcfg/get_netmask string
d-i netcfg/get_gateway string
d-i netcfg/get_nameservers string
d-i netcfg/confirm_static boolean

#d-i anna/choose_modules string network-console
#d-i network-console/password password
#d-i network-console/password-again password
"""

partition = """
### Partitioning
d-i partman-auto/disk string
d-i partman-partitioning/default_label select
d-i partman/mount_style select

d-i partman-auto/choose_recipe select
d-i partman/default_filesystem string
d-i partman-auto/expert_recipe string

#d-i partman/early_command string
d-i partman-efi/non_efi_system boolean
d-i partman-auto/method string

d-i partman-auto/purge_lvm_from_device boolean
d-i partman-partitioning/confirm_write_new_label boolean

d-i partman/choose_partition select
d-i partman/confirm_write_new_label boolean
d-i partman/confirm_nooverwrite boolean
d-i partman/confirm boolean
"""

aptsources = """
### Mirror
d-i mirror/country string
d-i mirror/http/hostname string
d-i mirror/http/directory string
d-i mirror/http/proxy string

d-i apt-setup/security_host string
d-i apt-setup/volatile_host string

d-i apt-setup/services-select multiselect

d-i apt-setup/contrib boolean
d-i apt-setup/non-free boolean
d-i apt-setup/use_mirror boolean

### Apt
# do not scan for another cd
apt-cdrom-setup apt-setup/cdrom/set-first boolean
# Disable CDROM entries after install
d-i apt-setup/disable-cdrom-entries boolean

### Additional repositories 0~9
"""
local = []
for i in range(0, 10):
	local.append('d-i apt-setup/local{}/comment string'.format(i))
	local.append('d-i apt-setup/local{}/source boolean'.format(i))
	local.append('d-i apt-setup/local{}/repository string'.format(i))
	local.append('d-i apt-setup/local{}/key string'.format(i))

local = ('\n'.join(map(str, local)))
aptsources = aptsources + local

software = """
### Software selection
tasksel tasksel/first multiselect

### Package Selection
# Individual additional packages to install
d-i pkgsel/include string

d-i pkgsel/upgrade select

# Disable popularity-contest
popularity-contest popularity-contest/participate boolean
"""

bootloader = """
### Boot loader installation
#d-i grub-installer/skip boolean
#d-i lilo-installer/skip boolean

## GRUB bootloader settings
d-i grub-installer/bootdev string

d-i grub-installer/only_debian boolean
d-i grub-installer/with_other_os boolean
d-i grub-installer/force-efi-extra-removable boolean

### kernel boot parameters
d-i debian-installer/add-kernel-opts string
"""

finishup = """
### Finishing up the installation
d-i cdrom-detect/eject boolean

# reboot into the installed system.
d-i finish-install/reboot_in_progress note
#d-i debian-installer/exit/halt boolean
# This will power off the machine instead of just halting it.
d-i debian-installer/exit/poweroff boolean
"""

command = """
### run scrpit 
d-i preseed/run string
### This command is run commands in the target system.
d-i preseed/late_command string
"""




