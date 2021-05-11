#!/sbin/sh

mkdir -p /mnt/vendor/persist/t6_twrp
rm -rf /mnt/vendor/persist/t6_twrp/*
cp -rf /mnt/vendor/persist/t6/* /mnt/vendor/persist/t6_twrp
