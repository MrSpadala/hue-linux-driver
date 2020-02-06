
#cp usb_skeleton.ko /lib/modules/`uname -r`

#depmod -a `uname -r` /lib/modules/5.3.0-28-generic/usb_skeleton.ko

rm /lib/modules/5.3.0-28-generic/kernel/drivers/usb/skeleton/usb_skeleton.ko
cp usb_skeleton.ko /lib/modules/5.3.0-28-generic/kernel/drivers/usb/skeleton/
