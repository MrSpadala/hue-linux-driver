# hue-linux-driver
Linux drivers for NZXT's HUE LED Strips, with some Python bindings (work in progrss).

After reading and learning how to write a usb device driver I discovered `usb-skeleton.c` in [linux/drivers/usb](https://github.com/torvalds/linux/blob/master/drivers/usb/usb-skeleton.c) which contained all that I need.

It creates a device under `/dev/skel2` onto which you can write using any language you want. Also I made a small Flask server 'cause why don't change led colors remotely.

Docs TBA

