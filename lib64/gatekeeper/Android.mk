LOCAL_PATH := $(call my-dir)

include $(CLEAR_VARS)

GATEKEEPER_LIBS := gatekeeper.mt6771.so gatekeeper.$(PRODUCT_BOARD).so
GATEKEEPER_SYMLINKS := $(addprefix $(PRODUCT_OUT)/recovery/root/vendor/lib64/hw/,$(notdir $(GATEKEEPER_LIBS)))
$(GATEKEEPER_SYMLINKS): $(LOCAL_INSTALLED_MODULE)
	@echo "Gatekeeper lib link: $@"
	@mkdir -p $(dir $@)
	@rm -rf $@
	$(hide) ln -sf gatekeeper.trustkernel.so $@

ALL_DEFAULT_INSTALLED_MODULES += $(GATEKEEPER_SYMLINKS)
