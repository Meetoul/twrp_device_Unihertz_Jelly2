ifneq ($(filter Atom_L_EEA Atom_L_TEE Atom_XL_EEA Atom_XL_TEE ,$(TARGET_DEVICE)),)

LOCAL_PATH := device/Unihertz/Atom_LXL

include $(call all-makefiles-under,$(LOCAL_PATH))

endif
