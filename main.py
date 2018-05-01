import pycom
import os
import machine
from L76GNSS import L76GNSS
from pytrack import Pytrack
from network import WLAN
from machine import SD

# Disable default LED heartbeat
pycom.heartbeat(False)

# Initialize GPS / GLONASS
pytrk = Pytrack()
t = 30  # maximum time (s) for GPS fix

# wait for GPS uplink
while True:
    pycom.rgbled(0xFF0000)  # light LED red while waiting for GPS
    gps = L76GNSS(pytrk, timeout=t)
    if gps.coordinates()[0] is not None:
        pycom.rgbled(0x000000)  # disable LED once we have GPS,
        break

# Load WLAN module in station mode
wlan = WLAN(mode=WLAN.STA)


# Initialize RTC
rtc = machine.RTC()  # todo properly init RTC (GPS) - now only epoch start
# rtc.ntp_sync('pool.ntp.org')  # server to use for RTC synchronization

# set variables for file management
SD_MNT_PNT = '/sd'
FILE_DIR = 'dump_data'
FILE_NAME = 'wifi'
DIR_PATH = SD_MNT_PNT + '/' + FILE_DIR


# Mount and prepare SD card
sd = SD()
os.mount(sd, SD_MNT_PNT)

if FILE_DIR not in os.listdir(SD_MNT_PNT):
    os.mkdir(DIR_PATH)


# create new log file for each session
noFiles = len(os.listdir(DIR_PATH))
FILE_PATH = SD_MNT_PNT + '/' + FILE_DIR + '/' + FILE_NAME + str(noFiles) + ".log"


#blink green 3 times?


# Constant WIFI scanning
while True:

    # open log file
    log_file = open(FILE_PATH, 'a')



    # Get coordinates
    coord = gps.coordinates()

    line_entry = 'SSID: {} - ENC: {} - @ (LON: {} / LAT: {})'
    sec_state = 3


    # Scan wifis
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

        log_file.write('{},{},{},{},{},{},{},{}\n'.format(net.ssid,
                                                        net.bssid,
                                                        net.sec,
                                                        net.channel,
                                                        net.rssi,
                                                        rtc.now(),
                                                        coord[0],
                                                        coord[1]))

    print('-------------------------------')

    # Update LED according to least secure wifi
    if sec_state == 0:  # no encryption == white
        pycom.rgbled(0xFFFFFF)

    if sec_state == WLAN.WEP:
        pycom.rgbled(0xFF00FF)

    if sec_state == WLAN.WPA:
        pycom.rgbled(0x00FF00)

    if sec_state == WLAN.WPA2:
        pycom.rgbled(0x00FF00)

    if sec_state == WLAN.WPA2_ENT:
        pycom.rgbled(0xFF00FF)

    # Cleanup
    log_file.close()
