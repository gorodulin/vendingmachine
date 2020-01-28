# Simple Vending Machine

_**Keywords:** вендинговый, python, автомат, vending, rpi, docker, vendingmachine, p20200119a_

Written in Python 3 for RPi-based vending machine, containerized with Docker.

Based on finite state machine (FSM) programming pattern and threads.

The routine:

- Collect money
- Wait for user to press button
- Eject item
- Generate receipt
- repeat

Components utilized:

- Coin acceptor (CCTALK protocol over USB)
- Dispenser (USB)
- Button switch (GPIO, hw debounce)
- Button LED backlight (GPIO, MOSFET)
- Front panel backlight (I2C-controlled relay switch)
- Internet connection
- no hopper, thus no change :-)

Features:

- Fully configurable via .ini file.
- Enters "out-of-service" state on hardware/software error.
- Recovers last state when the error is gone.
- Makes digitaly signed JSON requests to OrangeData API (Generate a receipt, send a copy to tax authorities)
- Continuous background self-test, built-in watchdog.
- Continuous reporting.
- Autorecovery after power failure.
- Autorecovery after dispenser failure.
- Saves its state in a built-in persistent file storage optimized for flash based drives.
- Systemctl-controlled container. Autostart and graceful shutdown.

