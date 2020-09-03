#!/usr/bin/python3
import os

APP_NAME ='Spark'
APP_VERSION = '0.0.3'
APP_DESCRIPTION = "Graphical tool for creating preseed files, for Debian GNU/Linux, for fully automatic installations."
#APP_ICON = "/usr/share/pixmaps/spark.png"


WORK_DIR = os.path.expanduser('~/.cache/spark')
CD_ROOT_DIR = os.path.join(WORK_DIR, 'cd-root')
GRUB_DIR = os.path.join(CD_ROOT_DIR, 'boot', 'grub')
ISOLINUX_DIR = os.path.join(CD_ROOT_DIR, 'isolinux')
PRESEED_DIR = os.path.join(CD_ROOT_DIR, 'preseed')
SCRIPTS_DIR = os.path.join(PRESEED_DIR, 'scripts')
for DIR in (CD_ROOT_DIR, GRUB_DIR, ISOLINUX_DIR, PRESEED_DIR, SCRIPTS_DIR):
	if not os.path.exists(DIR):
		os.makedirs(DIR)

PRESEED_FILE = os.path.join(PRESEED_DIR, 'spark.sk')
PRE_INSTALLATION_SCRIPT = os.path.join(SCRIPTS_DIR, 'pre-installation-script.sh')
POST_INSTALLATION_SCRIPT = os.path.join(SCRIPTS_DIR, 'post-installation-script.sh')
ISOLINUX_FILE = os.path.join(ISOLINUX_DIR, 'isolinux.cfg')
GRUB_FILE = os.path.join(GRUB_DIR, 'grub.cfg')
CONFIG_FILE = os.path.join(WORK_DIR, '.spark_config')

for FILE in (PRESEED_FILE, PRE_INSTALLATION_SCRIPT, POST_INSTALLATION_SCRIPT, CONFIG_FILE):
	if not os.path.exists(FILE):
		FILE = open(FILE, "w")
		FILE.close()

