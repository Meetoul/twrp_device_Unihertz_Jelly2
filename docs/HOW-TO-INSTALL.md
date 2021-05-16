How to install TWRP for the Unihertz Jelly2
=================================================

## Getting adb and fastboot

### Linux or MacOS

If you are using a Linux or a similar operating system on your PC or Mac chances are very high that you already have these two applications installed.
Open a terminal and exectute the following commands.

```bash
adb version
fastboot --version
```

If one or both of these output an error you need to (re-)install adb and fastboot.

```bash
wget https://dl.google.com/android/repository/platform-tools-latest-linux.zip
unzip platform-tools-latest-linux.zip -d ~
```

Update your PATH variable for your environment

```bash
gedit ~/.profile
```
	
Add the following
	
```bash
# add Android SDK platform tools to path
if [ -d "$HOME/platform-tools" ] ; then
  PATH="$HOME/platform-tools:$PATH"
fi	
```

Then update your environment

```bash
source ~/.profile
```

### Windows

Download [the latest version of adb and fastboot](https://dl.google.com/android/repository/platform-tools-latest-windows.zip) to a directory of your choice and extract the archive.

Note: I've had reports that under Windows adb/fastboot might not recognize the phone while in TWRP. For now I don't know whats causing this. So if that happends to you try using linux instead.

## Unlocking

To be able to install anything on the Unihertz Jelly2 we first need to unlock the bootloader.

1. Boot your device into the official OS.
2. Go to `Settings > About phone`, tap the "build number" several times to enable developer settings.
3. Go to `Settings > System > Developer Settings`, enable OEM unlocking and ADB debugging.
4. Connect your phone to your PC and open a terminal or a command line window.
5. Run `adb reboot bootloader` on your PC (there is no way to enter bootloader directly, only possible through adb).
6. Once your device has finished booting run `fastboot flashing unlock` and comfirm unlock on device (**THIS WILL WIPE ALL DATA!**).
6. Run `fastboot reboot` to reboot your device and now you should see an unlocked warning during boot screen.

## Disabling AVB (Android Verified Boot)

To get TWRP to boot proberly we also need to disable AVB. Otherwise the bootloader will check the ROM with the wrong authorization keys and prevent the loading.

- [Jelly2 Region TEE (non-european union)](https://github.com/Meetoul/twrp_device_Unihertz_Jelly2_TEE/releases)

1. Download `vbmeta.img` from the latest release page of your device.
2. Connect your phone to your PC and open a terminal or a command line window.
3. Run `adb reboot bootloader` on your PC to put your device in bootloader mode.
4. Once your device has finished booting run `fastboot flash --disable-verification --disable-verity vbmeta vbmeta.img`.
5. Then run `fastboot flash --disable-verification --disable-verity vbmeta_system vbmeta.img`.
6. Also run `fastboot flash --disable-verification --disable-verity vbmeta_vendor vbmeta.img`.

## Installing TWRP recovery

- [Jelly2 Region TEE (non-european union)](https://github.com/Meetoul/twrp_device_Unihertz_Jelly2_TEE/releases)

1. Download `recovery.img` from the latest release page of your device.
2. Connect your phone to your PC and open a terminal or a command line window.
3. Run `adb reboot bootloader` on your PC to put your device in bootloader mode.
4. Once your device has finished booting run `fastboot erase recovery`. For some reason, image may be not actually flashed, even if fastboot reported success (at least over the stock recovery image), so in order make sure that the custom image is always flashed it's better to always erase the partition before flashing. After the erasing run `fastboot flash recovery recovery.img`.
5. Run `fastboot reboot` and after the screen goes dark press volume up until you see the TWRP logo. Also you can type `fastboot reboot recovery` to boot to recovery mode immediately.
