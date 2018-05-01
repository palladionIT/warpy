# warpy
Wardriving on a pycom.io lopy4 with pytrack (GPS, accel, ...) shield.

## Installation
Download the necessary Pytrack library files from the [pycom.io lib repository](https://github.com/pycom/pycom-libraries) (including pycoproc.py from /lib/pycoproc) and upload them into a _lib_ folder on your board.

## Usage
Once you have the project uploaded to your pytrack (in particularn main.py and the libs), it will once powered continously collect nearby wifis and store them to the SD card with GPS coordinates.
