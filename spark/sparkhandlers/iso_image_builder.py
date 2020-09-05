SPARK_PRESEED_FILE = "file=/cdrom/preseed/spark.sk"
APPEND = "auto=true priority=critical net.ifnames=0  =5"
#-------------------------------------------------------------------------------
GRUB_TEMPLATE = """###
if loadfont $prefix/font.pf2 ; then
	set gfxmode=800x600
	set gfxpayload=keep
	insmod efi_gop
	insmod efi_uga
	insmod video_bochs
	insmod video_cirrus
	insmod gfxterm
	insmod png
	terminal_output gfxterm
fi

if background_image /isolinux/splash.png; then
	set color_normal=light-gray/black
	set color_highlight=white/black
elif background_image /splash.png; then
	set color_normal=light-gray/black
	set color_highlight=white/black
else
	set menu_color_normal=cyan/blue
	set menu_color_highlight=white/blue
fi

#insmod play
#play 960 440 1 0 4 440 1
set theme=/boot/grub/theme/1

insmod keystatus
if keystatus --shift; then
	set timeout=20
else
	set timeout=5
fi

set default=0
menuentry --hotkey=a 'Automated install' {{
	set background_color=black
	linux    /install.amd/vmlinuz {APPEND} {PRESEED_FILE} vga=788 --- quiet
	initrd   /install.amd/gtk/initrd.gz
}}"""

#-------------------------------------------------------------------------------
ISOLINUX_TEMPLATE = """###
path
default vesamenu.c32
prompt 0
timeout 50

menu hshift 4
menu width 70
menu title Debian GNU/Linux installer menu (BIOS mode)
menu background splash.png
menu color title	* #FFFFFFFF *
menu color border	* #00000000 #00000000 none
menu color sel		* #ffffffff #76a1d0ff *
menu color hotsel	1;7;37;40 #ffffffff #76a1d0ff *
menu color tabmsg	* #ffffffff #00000000 *
menu color help		37;40 #ffdddd00 #00000000 none
menu vshift 8
menu rows 12

label autoinstall
	menu default
	menu label ^Automated install
	kernel /install.amd/vmlinuz
	append  {APPEND} {PRESEED_FILE} vga=788 initrd=/install.amd/gtk/initrd.gz --- quiet """
#-------------------------------------------------------------------------------

UDISKSCTL_MOUNT_CMD = "udisksctl loop-setup -r -f {0}"
UDISKSCTL_UNMOUNT_CMD = "udisksctl unmount -b {0}p1"
UDISKSCTL_INFO_CMD = "udisksctl info -b {0}p1"
OS_XORRISO_CMD = """
xorriso -as mkisofs\
 -r -checksum_algorithm_iso md5,sha1,sha256,sha512\
 -V "{0}" -o {1}\
 -J -joliet-long -cache-inodes\
 -isohybrid-mbr {2} -b isolinux/isolinux.bin -c isolinux/boot.cat\
 -boot-load-size 4 -boot-info-table -no-emul-boot -eltorito-alt-boot -e boot/grub/efi.img -no-emul-boot\
 -isohybrid-gpt-basdat -isohybrid-apm-hfsplus {3} {4}
"""
# -quiet
#-------------------------------------------------------------------------------
#import re
import os
import subprocess


class IsoImageBuilder:
	def __init__(self):
		super().__init__()
		self.loop = None
		self.process = None
		self.exitcode = None

	def get_iso_label(self, source_iso_file):
		f = open(source_iso_file,'rb')
		f.seek(0x8028, 0) #from the begin Hexadecimal 0X8028 = 32808
		iso_label = (f.read(32).decode("utf-8").strip())
		f.close()
		return iso_label

	def __execute(self, cmd=None):
		if cmd != None and self.process == None:
			self.process = subprocess.Popen(['sh', cmd],stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
			return self.process
		else:
			return None

	def __os_execute_cmd(self, cmd):
		os_stream = os.popen(cmd)
		os_output = os_stream.read()
		return os_output

	def __iso_mount(self, source_iso_file):
			self.__iso_unmount()
			mount_output_cmd = self.__os_execute_cmd(UDISKSCTL_MOUNT_CMD.format(source_iso_file))
			thislist = mount_output_cmd.split()
			if 'Mapped' in thislist:
				self.loop = (thislist[-1].replace('.', ''))
				label = self.labels_object_dict.get('label_rebuild_label')
				label.set_text(f'mount {self.loop} Ok')
			self.log.debug('mount', self.loop)

	def __get_mount_path(self):
		if self.loop != None:
			info_output_cmd = self.__os_execute_cmd(UDISKSCTL_INFO_CMD.format(self.loop))
			thislist = []
			for text in info_output_cmd.splitlines():
				if 'MountPoints:' in text:
					templist = text.split()
					templist.remove('MountPoints:')
					thislist += templist
					break
			return (" ".join(thislist).replace(" ", "\ "))

	def __iso_unmount(self):
		if self.loop != None:
			unmount_output_cmd = self.__os_execute_cmd(UDISKSCTL_UNMOUNT_CMD.format(self.loop))
			if 'Unmounted' in unmount_output_cmd.split():
				self.log.debug('unmount', self.loop)
				label = self.labels_object_dict.get('label_rebuild_label')
				label.set_text(f'unmount {self.loop} Ok')
				self.loop = None

	def __mbr_dump(self, source_iso_file):
		with open(source_iso_file, 'rb') as rb, open(f"{self.settings.WORK_DIR}/isohdpfx.bin", 'wb') as wb:
			isohdpfx = rb.read(432)
			wb.write(isohdpfx)
			rb.close()
			wb.close()

	def __write_boot_config_files(self):
		new_append = APPEND
		with open(self.settings.GRUB_FILE, 'w') as w_grub, open(self.settings.ISOLINUX_FILE , 'w') as w_isolinux:
			w_grub.write(GRUB_TEMPLATE.format(APPEND=new_append, PRESEED_FILE=SPARK_PRESEED_FILE))
			w_isolinux.write(ISOLINUX_TEMPLATE.format(APPEND=new_append, PRESEED_FILE=SPARK_PRESEED_FILE))
			w_grub.close()
			w_isolinux.close()

	def __run_xorriso(self, source_iso_file, output_iso_file_name):
		#mount_point = '/media/$USER/'+iso_label.replace(" ", "\ ")
		mount_point = self.__get_mount_path()
		iso_label = self.get_iso_label(source_iso_file)
		pretty_label = iso_label.strip()
		cmd = OS_XORRISO_CMD.format(pretty_label, output_iso_file_name, f"{self.settings.WORK_DIR}/isohdpfx.bin", mount_point, self.settings.CD_ROOT_DIR)
		self.log.debug(cmd)
#		self.__os_execute_cmd(cmd)

		with open(f"{self.settings.WORK_DIR}/xorriso.sh", 'w') as script:
			script.write(cmd)
			script.close()

		cmd = f"{self.settings.WORK_DIR}/xorriso.sh"
		label = self.labels_object_dict.get('label_rebuild_label')
		progressbar = self.widgets_object_dict.get('progressbar_rebuild_progressbar')

		process = self.__execute(cmd)
		for line in iter(process.stdout.readline, ''):
			data = line.decode().split()
			if "done" in data or "done," in data:
				stdout_text = ' '.join(data[2:6]).strip(',')
				stdout_progres = (' '.join(data[4:5]).strip('%'))
				progressbar.set_fraction(float(stdout_progres[:-2])/ 100)
				label.set_text(stdout_text)
			if process.poll() is not None:
				rc = process.returncode
				if rc == 0:
					self.exitcode = rc
					self.process = None
					progressbar.set_fraction(1)
					label.set_text('Completeed')
				else:
					self.exitcode = rc
				break

	def __cleen_up_file(self):
		label = self.labels_object_dict.get('label_rebuild_label')
		label.set_text('Cleen up...')
		cleen_up_file = ("isohdpfx.bin", "xorriso.sh",)
		for f in  cleen_up_file:
			if os.path.exists(f"{self.settings.WORK_DIR}/{f}"):
				os.remove(f"{self.settings.WORK_DIR}/{f}")

	def make_new_image(self, source_iso_file, output_iso_file_name):
		self.__write_boot_config_files()
		self.__mbr_dump(source_iso_file)
		self.__iso_mount(source_iso_file)
		os.sync()
		self.__run_xorriso(source_iso_file, output_iso_file_name)
		os.sync()
		self.__iso_unmount()
		self.__cleen_up_file()





