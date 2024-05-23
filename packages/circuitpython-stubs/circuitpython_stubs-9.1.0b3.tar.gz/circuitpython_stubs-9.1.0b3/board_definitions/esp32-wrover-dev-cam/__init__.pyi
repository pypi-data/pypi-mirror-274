# SPDX-FileCopyrightText: 2024 Justin Myers
#
# SPDX-License-Identifier: MIT
"""
Board stub for Freenove ESP32-WROVER-DEV-CAM
 - port: espressif
 - board_id: esp32-wrover-dev-cam
 - NVM size: 8192
 - Included modules: _asyncio, _bleio, _pixelmap, adafruit_bus_device, adafruit_pixelbuf, aesio, alarm, analogbufio, analogio, array, atexit, audiobusio, audiocore, audiomixer, audiomp3, binascii, bitbangio, bitmaptools, board, builtins, builtins.pow3, busdisplay, busio, busio.SPI, busio.UART, canio, codeop, collections, countio, digitalio, displayio, epaperdisplay, errno, espcamera, espidf, espnow, espulp, fontio, fourwire, framebufferio, frequencyio, getpass, gifio, hashlib, i2cdisplaybus, io, ipaddress, jpegio, json, keypad, keypad.KeyMatrix, keypad.Keys, keypad.ShiftRegisterKeys, keypad_demux, keypad_demux.DemuxKeyMatrix, locale, math, max3421e, mdns, memorymap, microcontroller, msgpack, neopixel_write, nvm, onewireio, os, os.getenv, paralleldisplaybus, ps2io, pulseio, pwmio, qrio, rainbowio, random, re, rotaryio, rtc, sdcardio, select, sharpdisplay, socketpool, ssl, storage, struct, supervisor, synthio, sys, terminalio, time, touchio, traceback, ulab, usb, vectorio, warnings, watchdog, wifi, zlib
 - Frozen libraries: 
"""

# Imports
import microcontroller


# Board Info:
board_id: str


# Pins:
LED: microcontroller.Pin  # GPIO2
LED_INVERTED: microcontroller.Pin  # GPIO2
BUTTON: microcontroller.Pin  # GPIO0
CAMERA_DATA2: microcontroller.Pin  # GPIO4
CAMERA_DATA3: microcontroller.Pin  # GPIO5
CAMERA_DATA4: microcontroller.Pin  # GPIO18
CAMERA_DATA5: microcontroller.Pin  # GPIO19
CAMERA_DATA6: microcontroller.Pin  # GPIO36
CAMERA_DATA7: microcontroller.Pin  # GPIO39
CAMERA_DATA8: microcontroller.Pin  # GPIO34
CAMERA_DATA9: microcontroller.Pin  # GPIO35
CAMERA_VSYNC: microcontroller.Pin  # GPIO25


# Members:

# Unmapped:
#   none
