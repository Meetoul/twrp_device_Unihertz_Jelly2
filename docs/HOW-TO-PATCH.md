How to modify a (Meditek) Android kernel
=================================================
Some Meditek kernels have the pesky habit of not loading the touchscreen drivers in recovery mode. So I searched for a solution and found it on the Hovatek Forum.

https://forum.hovatek.com/thread-27132.html

What this guide lacks though is a more up-to-date and failsafe approach. It was written in 2019 but even back in those ancient times there existed something called (K)ASLR. A technique that should prevent (or at least slow down) the progress of hacking the device. Which is exactly what we are trying to do here in the first place. The following steps may also apply for other kernels so feel free to try it out (at yout own risk). The guide is written for a Windows PC only because a special piece of software needed for this I was only able to "obtain" a windows copy of. In principle it should also work in Linux although I haven't tested it.

## Requirements

- A rooted phone (Duh!)
- [ADB & fastboot](https://developer.android.com/studio) (The commandline tools are enough)
- [Android Image Kitchen](https://forum.xda-developers.com/showthr...?t=2073775)
- [7-zip](https://www.7-zip.org)
- [HXD hex editor](https://mh-nexus.de/en/hxd)
- [Gzip for windows](http://gnuwin32.sourceforge.net/packages/gzip.htm)
- An ominous, yet very powerful dissasembler used by many professionals

## Acquiring the recovery.img

An easy aproach would be to simply extract it from the zip file of a ROM update from your phone vendor.
If you don't have this luxury you could also extract it directly from your phone:

	adb shell
	su
	cat /proc/mtd

Now you should see a list of all the drives in your internal memory card. Use this information to download the one labeled as `recovery`:

(In my example it resides on drive `mtd10`)

	cat /dev/mtd/mtd10 > /sdcard/recovery.img
	exit
	exit
	adb pull /sdcard/recovery.img

## Unpack the recovery.img

This one is quite simple. Just put your `recovery.img` in the same folder as Android Image Kitchen and execute `unpackimg.bat`.
Inside the folder `split_img` you will find a file named `recovery.img-zImage` which is exactly what we need. The best thing would be to copy this file somewhere else and rename it to `Image.gz`

## Strip the kernel of "additional" data

To be able to load this zImage file the average bootloader of a phone needs some additional information and all of it is mashed togehter with the actual kernel. So to get a clean binary that we can use (and manipulate) we need to strip the kernel of this so called payload. But we also need it later on to once more combine it into a bootable kernel so we cannot afford to loose it. If we would try to simply unpack the kernel with 7-zip we would not be able to do so.

First of all a little excurse:

Back in the ancient times of computing, approximately around the year 1992, a revolutionary new file format was created: gzip. With this you were able to save plenty of space on your hard disk to store files. And don't get me wrong, but hard disk back then were a quite ... hard ... and heavy. This newly invented gzip was so successful that it even lives on today in the form of the default compression format used for modern day linux and android kernels. Most of its success probably comes from the fact that it is very small and easy to implement. 10 bytes of Header, 8 bytes of Footer and the rest is the actual data that is stored in between.

So now lest get back on track, shall we?

We need to strip all the information that preceeds the actual gzipped kernel image. To do that we open the `Image.gz` file with HXD hex editor and cut everything that comes before the magic hex-values `1F 8B` which indicate the start of a gzip file. Don't forget to paste the data into a new file and save it for later for example as `Image.gz-beginning`. Finding the end of a gzip file is a little more of a hassle but not that hard either. You need to open the remaining `Image.gz` with 7-zip and extract the file `Image` from inside it. Then switch back to HXD hex editor and look at the values of the offset 2 and 8 of `Image.gz`. These values indicate the compression method and the actual compression type. Most of the time it's `08` for "Deflate compression method" and `02` for "Max compression". Copy the previously extracted `Image` to the folder where gzip is installed and repack it but this time without the additional payload:

	gzip -n -k -9 Image

`-n` indicates the file should have no name

`-9` indicates max compression

`-k` keep the original file

Now also open the new `Image.gz` with HXD hex editor and compare the ending with the old file. You should see that the new one is almost identical to the old one except that it is a little bit shorter. Note the offset of the last byte in the new file and cut the old file at the exact same position. Again save the parts you cut in a additional file called `Image.gz-ending`.

## Get the symbols for analyzing the kernel

Now we need to identify the actual address where the touchscreen driver is located inside the kernel. To do this we ask our trusted (or should I say rooted) device for help:

	adb shell
	su
	echo 0 > /proc/sys/kernel/kptr_restrict
	sysctl -w kernel.randomize_va_space=0
	cat /proc/kallsyms >/sdcard/symbl.txt
	exit
	exit
	adb pull /sdcard/symbl.txt

With this you should get a file `symbl.txt` which we need to better identify the functions the kernel exists of.

## Analyse the kernel with that ominous tool

Fire up [*blackened*] and load the `Image` we extracted earlier. You will be asked for the architecture of your kernel file which you should answer truthfully. After hitting OK you will be asked for the "ROM start address" and the "Loading address". Because of the aforementioned (K)ASLR we need something different than the default values of `0xC0008000` (32-bit) and `0xFFFFFFC000080000` (64-bit). So open up your `symbl.txt` and copy the adress value of the very first entry. You need to put this value into both fields of the dialog in [*blackened*]. The values need to be in uppercase and starting with `0x`. When you compare the value with the default one I mentioned earlier you will see that they are quite similiar in the lower digits. In fact it has an additional `800` while the default one does not. This is because of the header of the kernel and simply needs to be removed. So for example `0xFFFFFF9B6B480800` becomes `0xFFFFFF9B6B480000`. Again click on OK and wait for the kernel to be analyzed by this awesome tool. If nothing seems to happen and the colorful bar at the top of the window keeps in the color of "Unexplored" select everything `Edit > Select all` and then analyze it with `Edit > Code`. This should take a while and after the analysis is finished we are now able to change all the things we came here for. So keep your Guidebook `symbl.txt` handy, let's do some researching.

First of all we need to `Jump to address` (right click in the adress column) of `tpd_i2c_probe` which is the beginning of the touchscreen driver inside the kernel. Next we need the exact address of `get_boot_mode`. A little bit further down from the entry point of the driver you schould find a line starting with `BL` followed by `sub_` and the mentioned address of `get_boot_mode`. This means that here the function `get_boot_mode` is being called and the next line is the comparing `CMP` of the result with the value of `#2`. This we need to change into `#0` to be recognized as `boot` instead of `recovery`. So go to `Options > General > Disassembly Tab > Number of opcode` and enter `6`. Starting with the `CMP` copy at least the hex-vales of at least 4 to 5 lines. In my case this would be `1F 08 00 71 80 05 00 54 A8 0B 80 52 E9 B5 00 90` and that is what we need to finally be able to modify the kernel. Close [*blackened*] and don't save anything.

## Modify the kernel

Now that we know what we need we can actually temper with the kernel itself. So head back to HXD hex editor and make sure `Image` is still loaded. Search for the hex-values you got earlier. As we still know the first byte of that value is the `CMP` so the second one `08` is what we need to change to `00`. So do just that. Basically we are forcing the touchscreen driver to behave as if it was running in `boot` instead of `recovery`. That also means that if you use this modified kernel in `boot` the touchpad driver will be deactivated. So be extra careful not to mix it up with your original kernel. Save your changes and we are done.

## Putting the kernel back together

First of all we need to get a gzip file of the kernel

	gzip -n -k -9 Image

Next check if the packed size of the new kernel matches the packed size of the old kernel. The best thing to do that would be using 7-zip. If it's not matching you need to add a `00` at the end of the unpacked kernel using HXD hex editor and repack it again. Do that as long as the sizes don't match. In fact I had to add quite a lot of `00` but it still didn't match at the end. Adding one more `00` I was 1 byte too big removing the `00` I was one byte too low. So I ended up adding an additional `00` to the packed kernel file itself to get it to match. If the sizes don't match the kernel would not boot in the end. As a final step just add the beginning `Image.gz-beginning` and the ending `Image.gz-ending` to your packed kernel file and you are good to go.
