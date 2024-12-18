# RNode Flasher

A _work-in-progress_ web based firmware flasher for [Reticulum](https://github.com/markqvist/Reticulum) / [RNode_Firmware](https://github.com/markqvist/RNode_Firmware).

- It is written in javascript and uses the [Web Serial APIs](https://developer.mozilla.org/en-US/docs/Web/API/Web_Serial_API).
- It supports putting relevant devices into DFU mode.
- It supports flashing firmware from a zip file.

At this time, it does not support flashing bootloaders or softdevices for the nRF boards.

## How does it work?

I wanted something simple, for flashing RNode firmware to a nRF52 RAK4631 in a web browser.

So, I spent a bit of time working through the source code of [adafruit-nrfutil](https://github.com/adafruit/Adafruit_nRF52_nrfutil) and wrote a javascript implementation of [dfu_transport_serial.py](https://github.com/adafruit/Adafruit_nRF52_nrfutil/blob/master/nordicsemi/dfu/dfu_transport_serial.py)

Generally, you would use the following command to flash a firmware.zip to your device;

```
adafruit-nrfutil dfu serial --package firmware.zip -p /dev/cu.usbmodem14401 -b 115200 -t 1200
```

The [nrf52_dfu_flasher.js](js/nrf52_dfu_flasher.js) in this project implements a javascript, web based version of the above command.

There was an existing package called [pc-nrf-dfu-js](https://github.com/NordicSemiconductor/pc-nrf-dfu-js), however this repo had been archived and didn't appear to support the latest DFU protocol.

## How to use it?

- Open https://liamcottle.github.io/rnode-flasher/ in your web browser.
- Select your device.
- Put your device into DFU mode (for nRF52 boards)
- Select a firmware file and click flash.
- Once flashed, your device should reboot into the new firmware.
- For new devices that have never been provisioned, you should click "Provision" to configure the EEPROM.
- Every time you flash new firmware, you should also click "Set Firmware Hash".

> Note: At this time, firmware hashes for RNode are not automatically configured.

## What is needed to set up a new RNode?

> Note: This is a technical overview of how the RNode device provisioning works.
> Most of this is taken care of by the code base, and this section just makes it easier to understand what is going on.

To set up a new RNode device, you will need to do a few things;

- Obtain supported hardware, such as a RAK4631
- Obtain an RNode firmware file
- Put your device into DFU mode
- Flash the firmware file
- Provision the EEPROM

Once the firmware is flashed to the device, you will need to provision the EEPROM;

- Set firmware hash in eeprom
- Collect device info
  - `product`
  - `model`
  - `hardware_revision`
  - `serial_number`
  - `made` (unix timestamp of device creation)
- Write device info to eeprom
- Create an MD5 checksum of the device info
- Write 16 byte device info checksum to eeprom
- Sign device info checksum with signing key to use as signature
- Write 128 byte signature to eeprom
- Write `ROM.INFO_LOCK_BYTE` to `ROM.ADDR_INFO_LOCK` in eeprom
- Read eeprom and validate checksums and signatures to ensure all is correct

## TODO

- support configuring eeprom with device signatures and firmware hashes
- support flashing existing firmware files from api
- calculate on air bitrate based on tnc settings
- try using [web-serial-polyfill](https://github.com/google/web-serial-polyfill) to support flashing from Android device?

## License

MIT

## References

- https://github.com/adafruit/Adafruit_nRF52_nrfutil
- https://github.com/adafruit/Adafruit_nRF52_nrfutil/blob/master/nordicsemi/dfu/dfu_transport_serial.py
- https://github.com/markqvist/RNode_Firmware/blob/master/RNode_Firmware.ino
- https://github.com/markqvist/RNode_Firmware/blob/master/Framing.h
- https://github.com/markqvist/RNode_Firmware/blob/master/Utilities.h
