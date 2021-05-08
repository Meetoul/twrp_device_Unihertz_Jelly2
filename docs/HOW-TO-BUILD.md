How to build TWRP for the Unihertz Atom L and XL
=================================================

This guide is focused on building the recovery under a Linux host environment.
Because good building instructions for TWRP are very hard to come by I will try to sum up all the steps that are needed.

## Setting up the build environment

In general follow one of the many build instructions found at the LineageOS wiki.
For example the instructions for the [Google Nexus 5 aka hammerhead](https://wiki.lineageos.org/devices/hammerhead/build).
Here is a short summing up.

### Install the build packages

To successfully build TWRP, you’ll need

```bash
sudo apt-get install bc bison build-essential ccache curl flex g++-multilib gcc-multilib git gnupg gperf imagemagick lib32ncurses5-dev lib32readline-dev lib32z1-dev liblz4-tool libncurses5 libncurses5-dev libsdl1.2-dev libssl-dev libxml2 libxml2-utils lzop pngcrush rsync schedtool squashfs-tools xsltproc zip zlib1g-dev
```

For Ubuntu versions older than 16.04 (xenial), you’ll need

```bash
sudo apt-get install libwxgtk2.8-dev	
```

For Ubuntu versions older than 20.04 (focal), you’ll also need

```bash
sudo apt-get install libwxgtk3.0-dev
```

### Install the platform-tools

Only if you haven’t previously installed adb and fastboot

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
	
### Install the repo command

Download the binary and make it executable

```bash
mkdir -p ~/bin
curl https://storage.googleapis.com/git-repo-downloads/repo > ~/bin/repo
chmod a+x ~/bin/repo
```
	
Update your PATH variable for your environment

```bash
gedit ~/.profile
```
	
Add the following
	
```bash
# set PATH so it includes user's private bin if it exists
if [ -d "$HOME/bin" ] ; then
  PATH="$HOME/bin:$PATH"
fi	
```

Then update your environment

```bash
source ~/.profile
```
	
### Configure git

repo requires you to identify yourself to sync Android

```bash
git config --global user.email "you@example.com"
git config --global user.name "Your Name"
```
	
### (optional) Turn on caching to speed up build

Update your build environment

```bash
gedit ~/.bashrc	
```

Add the following
	
```bash
export USE_CCACHE=1
export CCACHE_EXEC=/usr/bin/ccache
export CCACHE_COMPRESS=1
```

### Initialize the TWRP source repository

Create the project folder and download the source code

```bash
mkdir -p ~/android/twrp
cd ~/android/twrp
repo init -u https://github.com/minimal-manifest-twrp/platform_manifest_twrp_omni.git -b twrp-10.0
```
	
Now let's add this very device repo to the local_manifest

```bash
gedit cd ~/android/twrp/.repo/local_manifests/roomservice.xml
```
	
Add the following

```xml
<?xml version="1.0" encoding="UTF-8"?>
<manifest>
  <project name="ADeadTrousers/twrp_device_Unihertz_Atom_LXL" path="device/Unihertz/Atom_LXL" remote="github" revision="master" />
  <!-- For the Atom L region eea add -->  
  <project name="ADeadTrousers/twrp_device_Unihertz_Atom_L_EEA" path="device/Unihertz/Atom_L_EEA" remote="github" revision="master" />
  <!-- For the Atom XL region eea add -->  
  <project name="ADeadTrousers/twrp_device_Unihertz_Atom_XL_EEA" path="device/Unihertz/Atom_XL_EEA" remote="github" revision="master" />
  <!-- For the Atom L region tee add -->  
  <project name="ADeadTrousers/twrp_device_Unihertz_Atom_L_TEE" path="device/Unihertz/Atom_L_TEE" remote="github" revision="master" />
  <!-- For the Atom XL region tee add -->  
  <project name="ADeadTrousers/twrp_device_Unihertz_Atom_XL_TEE" path="device/Unihertz/Atom_XL_TEE" remote="github" revision="master" />
</manifest>
```

To finish everything up sync the repo

```bash
cd ~/android/twrp
repo sync --force-sync
```

## Extracting the vendor blobs

### Use imjtool (formerly known as imgtool) to extract from stock rom files

First follow [the instructions to extract and mount the stock rom files](HOW-TO-EXTRACT_FILES.md) 

Then extract all the files we need

```bash
# For the Atom L EEA use
~/android/twrp/device/Unihertz/Atom_L_EEA/extract-files.sh ~/unihertz/extracted
# For the Atom XL EEA use
~/android/twrp/device/Unihertz/Atom_XL_EEA/extract-files.sh ~/unihertz/extracted
# For the Atom L TEE use
~/android/twrp/device/Unihertz/Atom_L_TEE/extract-files.sh ~/unihertz/extracted
# For the Atom XL TEE use
~/android/twrp/device/Unihertz/Atom_XL_TEE/extract-files.sh ~/unihertz/extracted
```

### Use an allready rooted device

If you were able to root your device this is just a small step. Plug in your device and do the follwing

```bash
# For the Atom L EEA use
~/android/twrp/device/Unihertz/Atom_L_EEA/extract-files.sh 
# For the Atom XL EEA use
~/android/twrp/device/Unihertz/Atom_XL_EEA/extract-files.sh
# For the Atom L TEE use
~/android/twrp/device/Unihertz/Atom_L_TEE/extract-files.sh 
# For the Atom XL TEE use
~/android/twrp/device/Unihertz/Atom_XL_TEE/extract-files.sh
```
	
## Building the rom

Prepare the build	

```bash
cd ~/android/twrp
source build/envsetup.sh
# For the Atom L EEA use
lunch omni_Atom_L_EEA
# For the Atom XL EEA use
lunch omni_Atom_XL_EEA
# For the Atom L TEE use
lunch omni_Atom_L_TEE
# For the Atom XL TEE use
lunch omni_Atom_XL_TEE
```
	
Do the actual build
	
```bash
cd ~/android/twrp
ccache -M 50G
mka recoveryimage
```

## Updating the sorces (at a later time)

Make sure everything is up-to-date

```bash
cd ~/android/twrp
repo sync --force-sync
```
