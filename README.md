# Simple Vending Machine

_**Keywords:** p20200119a, python, vending machine, rpi, docker, vendingmachine, вендинговый автомат_

### Description

Written in Python 3 for RPi-based vending machine, containerized with Docker.

Based on finite state machine (FSM) programming pattern and threads.

Features:

- Fully configurable via .ini file.
- Enters "out-of-service" state on hardware/software error.
- Saves its state in a built-in persistent file storage optimized for flash based drives.
- Recovers last state when the error is gone.
- Indicates current state by flashing LED and controlling front panel backlight.
- Generates and sends digitally signed receipts to tax authorities through [OrangeData API](https://github.com/orangedata-official/API/blob/master/API%202.15.0%20(English).docx) (wip)
- Continuous background self-test, built-in watchdog.
- Continuous reporting.
- Autorecovery after power failure.
- Autorecovery after dispenser failure.
- Systemctl-controlled container. Autostart and graceful shutdown.

Machine routine:

- Collect coins
- Wait for user to press button
- Eject an item
- Generate a receipt
- (repeat)

Hardware components:

- Raspberry Pi 3B+
- Coin acceptor ([CCTALK](https://en.wikipedia.org/wiki/CcTalk) protocol over USB)
- Dispenser ([ESC/POS](https://en.wikipedia.org/wiki/ESC/P) protocol over USB), model: "Custom VKP80III"
- Button switch (GPIO, hw debounce)
- Button LED backlight (GPIO, MOSFET switch)
- Front panel backlight (I2C-controlled relay switch)
- no hopper, thus no change :-)
