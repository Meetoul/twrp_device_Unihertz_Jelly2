Common device configuration for the Unihertz Atom L and XL
=================================================
This common device tree is intended for a special useage in a TWRP or similar environment.

If you are looking for a device tree for the usage in a LineageOS or similar environment head over to https://github.com/ADeadTrousers/android_device_Unihertz_Atom_LXL.

The Unihertz Atom L (codenamed simply _"Atom_L"_) and the Atom XL (codenamed simply _"Atom_XL"_) are two rugged small smartphones from Unihertz, released in July 2020. They are both almost identical except the Atom XL offers an integrated digital mobile radio (DMR).

# Dependencies

Additionally to this common device tree, you'll need one or all of the four regional device trees

- [Atom L Region EEA (european union)](https://github.com/ADeadTrousers/twrp_device_Unihertz_Atom_L_EEA)
- [Atom XL Region EEA (european union)](https://github.com/ADeadTrousers/twrp_device_Unihertz_Atom_XL_EEA)
- [Atom L Region TEE (non-european union)](https://github.com/ADeadTrousers/twrp_device_Unihertz_Atom_L_TEE)
- [Atom XL Region TEE (non-european union)](https://github.com/ADeadTrousers/twrp_device_Unihertz_Atom_XL_TEE)

## Releases

For the actual releases head on over to the device tree of the individual devices:
- [Atom L Region EEA (european union)](https://github.com/ADeadTrousers/twrp_device_Unihertz_Atom_L_EEA/releases)
- [Atom XL Region EEA (european union)](https://github.com/ADeadTrousers/twrp_device_Unihertz_Atom_XL_EEA/releases)
- [Atom L Region TEE (non-european union)](https://github.com/ADeadTrousers/twrp_device_Unihertz_Atom_L_TEE/releases)
- [Atom XL Region TEE (non-european union)](https://github.com/ADeadTrousers/twrp_device_Unihertz_Atom_XL_TEE/releases)

## Documentations

- [HOW-TO-BUILD.md](docs/HOW-TO-BUILD.md) - Building instructions for TWRP.
- [HOW-TO-INSTALL.md](docs/HOW-TO-INSTALL.md) - Installation instructions for the Atom XL.
- [HOW-TO-UPDATE.md](docs/HOW-TO-UPDATE.md) - Update instructions for the Atom XL.
- [HOW-TO-EXTRACT_FILES.md](docs/HOW-TO-EXTRACT_FILES.md) - Instructions to extract files directly from the Atom L/XL stock rom files.
- [HOW-TO-PATCH.md](docs/HOW-TO-PATCH.md) - Patching the prebuilt kernel to activate touchscreen in recovery mode.

## Special Thanks To

- [PeterCxy from the XDA forum](https://forum.xda-developers.com/member.php?u=5351691) for helping me and providing the device tree for Atom L.
- [The device tree for the Atom L](https://cgit.typeblog.net/android/device/unihertz/Atom_L/) which was a great step-by-step guide to complete the Atom XL.
- [SachinBorkar from the Hovatek forum](https://forum.hovatek.com/thread-27132.html) for finding a solution to get the touchpad driver working in recovery mode.
