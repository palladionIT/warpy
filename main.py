import pycom
import time

pycom.heartbeat(False)

# Hello world blinking awesomeness
while True:
    pycom.rgbled(0xAA0000)
    time.sleep(1)
    pycom.rgbled(0x00AA00)
    time.sleep(1)
    pycom.rgbled(0x0000AA)
    time.sleep(1)

# two files:
#       main/scanner -> scans wifi and starts persistor
#       data_mngr -> writes to SD card (also checks size etc etc)
#                   -> if not moving for some time -> connect to known wifi (if there is) and upload to service
# dictionary of known WLANs (ssid key: (ssid, bssid, sec, channel, rssi))
# infinite loop of WLAN scanning (maybe add a delay)
# add to dictionary
