import pycom
import os
import machine
from L76GNSS import L76GNSS
from pytrack import Pytrack
from network import WLAN
from machine import SD

# Disable default LED heartbeat
pycom.heartbeat(False)

# Load WLAN module in station mode
wlan = WLAN(mode=WLAN.STA)

# Initialize GPS / GLONASS
t = 30  # maximum time (s) for GPS fix
pytrk = Pytrack()
gps = L76GNSS(pytrk, timeout=t)

# Initialize RTC
rtc = machine.RTC()  # todo properly init RTC (GPS) - now only epoch start
# rtc.ntp_sync('pool.ntp.org')  # server to use for RTC synchronization

# Mount and prepare SD card
SD_MNT_PNT = '/sd'
FILE_DIR = 'dump_data'
FILE_NAME = 'wifi.log'
DIR_PATH = SD_MNT_PNT + '/' + FILE_DIR
FILE_PATH = SD_MNT_PNT + '/' + FILE_DIR + '/' + FILE_NAME

sd = SD()
os.mount(sd, SD_MNT_PNT)

if FILE_DIR not in os.listdir(SD_MNT_PNT):
    os.mkdir(SD_MNT_PNT + DIR_PATH)

# log_file = open(FILE_PATH, 'a')

# Constant WIFI scanning
while True:

    # Get coordinates
    coord = gps.coordinates()

    # todo - only continue if GPS fix was found -> then scan etc etc

    line_entry = 'SSID: {} - ENC: {} - @ (LON: {} / LAT: {})'
    sec_state = 3

    nets = wlan.scan()

    for net in nets:

        print(line_entry.format(net.ssid, net.sec, coord[0], coord[1]))

        # Update minimum sec in current scan and set LED
        if net.sec < sec_state:
            sec_state = net.sec

        print('{},{},{},{},{},{},{},{}'.format(net.ssid,
                                                net.bssid,
                                                net.sec,
                                                net.channel,
                                                net.rssi,
                                                rtc.now(),
                                                coord[0],
                                                coord[1]))

        '''log_file.write('{},{},{},{},{},{},{},{}'.format(net.ssid,
                                                        net.bssid,
                                                        net.sec,
                                                        net.channel,
                                                        net.rssi,
                                                        rtc.now(),
                                                        coord[0],
                                                        coord[1]))'''

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

# Cleanup
#log_file.close()
