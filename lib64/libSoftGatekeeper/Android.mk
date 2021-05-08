LOCAL_PATH := $(call my-dir)

include $(CLEAR_VARS)

LIBSOFTGATEKEEPER_LIBS := gatekeeper.default.so
LIBSOFTGATEKEEPER_SYMLINKS := $(addprefix $(PRODUCT_OUT)/recovery/root/vendor/lib64/hw/,$(notdir $(LIBSOFTGATEKEEPER_LIBS)))
$(LIBSOFTGATEKEEPER_SYMLINKS): $(LOCAL_INSTALLED_MODULE)
	@echo "LibSoftGatekeeper lib link: $@"
	@mkdir -p $(dir $@)
	@rm -rf $@
	$(hide) ln -sf libSoftGatekeeper.so $@

ALL_DEFAULT_INSTALLED_MODULES += $(LIBSOFTGATEKEEPER_SYMLINKS)
