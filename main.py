import pycom
import time
import os
from network import WLAN
from machine import SD

# Disable default LED heartbeat
pycom.heartbeat(False)

# Load WLAN module in station mode
wlan = WLAN(mode=WLAN.STA)

# Mount and prepare SD card
SD_MNT_PNT = '/sd'
FILE_DIR = 'dump_data'
FILE_PATH = SD_MNT_PNT + '/' + FILE_DIR

sd = SD()
os.mount(sd, SD_MNT_PNT)

if FILE_DIR not in os.listdir(SD_MNT_PNT):
    os.mkdir(SD_MNT_PNT + FILE_PATH)

# Constant WIFI scanning
while True:

    line_entry = 'SSID: {} - ENC: {}'
    sec_state = 3

    nets = wlan.scan()

    for net in nets:

        print(line_entry.format(net.ssid, net.sec))

        # Update minimum sec in current scan and set LED
        if net.sec < sec_state:
            sec_state = net.sec

    print('-------------------------------')

    # Update LED according to least secure wifi
    if sec_state == 0:  # no encryption
        pycom.rgbled(0xFF0000)

    if sec_state == WLAN.WEP:
        pycom.rgbled(0xFFA500)

    if sec_state == WLAN.WPA:
        pycom.rgbled(0x0000FF)

    if sec_state == WLAN.WPA2:
        pycom.rgbled(0x0000FF)

    if sec_state == WLAN.WPA2_ENT:
        pycom.rgbled(0xFFFFFF)
