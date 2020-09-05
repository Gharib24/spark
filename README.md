# Spark
A simple graphical tool for creating preseed files, for Debian GNU/Linux.


![screenshot](screenshot/screenshot.png)

The program requires the xorriso, install xorriso first:

	sudo apt-get install xorriso

And then to install Spark run:

	sudo python3 setup.py install --install-layout=deb --install-scripts=/usr/bin/ --record file.txt

Or run Spark without installing:

	./sparking


dev=/dev/sdb
sudo fdisk -l "$dev" | sed -ne '/^\//s,\(^[^ ]*\) .*,\1,p' | while read part
do dd "if=$part" "of=$(basename "$part")"
done
