LOCAL_PATH := $(call my-dir)

include $(CLEAR_VARS)

KMSETKEY_LIBS := kmsetkey.mt6771.so
KMSETKEY_SYMLINKS := $(addprefix $(PRODUCT_OUT)/recovery/root/vendor/lib64/hw/,$(notdir $(KMSETKEY_LIBS)))
$(KMSETKEY_SYMLINKS): $(LOCAL_INSTALLED_MODULE)
	@echo "Gatekeeper lib link: $@"
	@mkdir -p $(dir $@)
	@rm -rf $@
	$(hide) ln -sf kmsetkey.trustkernel.so $@

ALL_DEFAULT_INSTALLED_MODULES += $(KMSETKEY_SYMLINKS)
