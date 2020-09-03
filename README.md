# spark
A simple graphical tool for creating preseed files, for Debian GNU/Linux.


![screenshot](screenshot.png)

The program requires the xorriso install it first:
    sudo apt-get install xorriso

And then to install it run.
    sudo python3 setup.py install --install-layout=deb --install-scripts=/usr/bin/ --record file.txt

Or run it without installing
    ./sparking

