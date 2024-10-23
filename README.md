# E5KDAQ

STATUS: Currently a work-in-progress.

Python port of interface library with USB support for EDAM-5019 DAQ.
Aimed primarily at GNU/Linux systems using the [`pyusb`](https://github.com/pyusb) library.

InLog provide Windows library, example code and documentation. The provided utility works in Wine for network access, but USB doesn't work. That is particularly unhelpful as a good use for these interface modules is with an SBC such as a Raspberry Pi and a power bank for remote monitoring.

The high-level API is mostly documented but it's not particularly clear how things like alarms and events are supposed to work.

The USB interface presents as `ID 04b4:8613 Cypress Semiconductor Corp. CY7C68013 EZ-USB FX2 USB 2.0 Development Kit` with four endpoints `BULK OUT`, `BULK IN`, `Interrupt`, `Isochronous`.

The tricky work here is digging into the `E5KDAQ.DLL` windows library to determine how the device is accessed via USB. This hasn't been obfuscated but it's a pity the source code for this isn't made available.
