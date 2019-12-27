import os

PRESEED_FILE="file=/cdrom/preseed/spark.sk"
APPEND="auto=true priority=critical net.ifnames=0 DEBCONF_DEBUG=5"
grub_template = """###
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

isolinux_template = """###
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


mount_cmd = "udisksctl loop-setup -r -f {0}"
unmount_cmd = "udisksctl unmount -b {0}p1"
xorriso_cmd="""
xorriso -as mkisofs -quiet \
 -r -checksum_algorithm_iso md5,sha1,sha256,sha512 \
 -V "{0}" -o {1} \
 -J -joliet-long -cache-inodes \
 -isohybrid-mbr {2} -b isolinux/isolinux.bin -c isolinux/boot.cat \
 -boot-load-size 4 -boot-info-table -no-emul-boot -eltorito-alt-boot -e boot/grub/efi.img -no-emul-boot \
 -isohybrid-gpt-basdat -isohybrid-apm-hfsplus {3} {4}"""



loop = None
class SysCmd():
	def __init__(self):
		super().__init__()

	def get_iso_label(self, iso_file):
		global iso_label
		if iso_file != None:
			f = open(iso_file,'rb')
			f.seek(0x8028,0) #from the begin Hexadecimal 0X8028 = 32808
			iso_label = (f.read(32).decode("utf-8").strip())
			f.close()
			return iso_label
		
	def __run_cmd(self, cmd , caller= None):
		global loop
		stream = os.popen(cmd)
		output = stream.read()
		if len(output) > 0:
			self.log.debug("{}".format(output))

		if caller == 'mount':
			loop = (output.split()[-1][:-1])
		elif caller == 'unmount':
			loop = None

	def __mount(self, iso_file):
			self.__unmount()
			self.__run_cmd(mount_cmd.format(iso_file), 'mount')
			self.get_iso_label(iso_file)

	def __unmount(self):
		if loop != None:
			self.__run_cmd(unmount_cmd.format(loop), 'unmount')

	def __copy_mbr(self, iso_file):
		with open(iso_file, 'rb') as rb, open(self.work_path+'isohdpfx.bin', 'wb') as wb:
			isohdpfx = rb.read(432)
			wb.write(isohdpfx)
			rb.close()
			wb.close()

	def __write_boot_config_files(self):
		with open(self.grub_config_file , 'w') as w_g, open(self.isolinux_config_file , 'w') as w_i:
			w_g.write(grub_template.format(APPEND=APPEND, PRESEED_FILE=PRESEED_FILE))
			w_i.write(isolinux_template.format(APPEND=APPEND, PRESEED_FILE=PRESEED_FILE))
			w_g.close()
			w_i.close()

	def __xorriso(self, iso_file, filename):
		label = self.get_iso_label(iso_file)
		pretty_label =  label.strip()
		point = iso_label.replace(" ", "\ ")
		mount_point = '/media/$USER/'+point
		self.__run_cmd(xorriso_cmd.format(pretty_label, self.work_path+filename, self.work_path+'isohdpfx.bin', mount_point, self.cd_root))
		self.log.debug(xorriso_cmd.format(pretty_label, self.work_path+filename, self.work_path+'isohdpfx.bin', mount_point, self.cd_root))

	def new_image(self, iso_file, filename):

		self.__write_boot_config_files()
		self.__copy_mbr(iso_file)
		self.__mount(iso_file)
		os.sync()
		self.__xorriso(iso_file, filename)
		os.sync()
		self.__unmount()
		if os.path.exists(self.work_path+'isohdpfx.bin'):
			os.remove(self.work_path+'isohdpfx.bin')




