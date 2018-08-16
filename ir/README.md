# Raspberry Pi AC Controller (IR)

## Overview

The repository houses code for a basic IR transmitter which is programmed to use
codes that will interact with my AC unit.

## Components

1. Raspberry Pi with WiFi dongle and SD card (case, if you please)
2. Half-size breadboard
3. Jumper cables
3. 1 IR 5mm LED
4. 1 220 Ohm resistor
5. 1 10k Ohm resistor
6. PN2222 transistor
7. IR receiver for testing
8. A minor amount of programming skill

## The System

The AC unit has a hard constraint that it should not be turned on within 3
minutes of turning it off. Let's keep that in mind as we design.

Let's build an API to "press the buttons" on the raspberry pi IR remote.

## Hardware Setup

Refer to the image below, borrowed from [here](https://www.hackster.io/austin-stanton/creating-a-raspberry-pi-universal-remote-with-lirc-2fd581)
for an example layout. I used a Raspberry Pi Model B Rev 2, so the connections were
slightly different.

1. Connect the 3.3V to the positive breadboard rail
2. Connect the ground to the negative breadboard rail
3. Wire up the IR receiver as indicated. I connected it to GPIO 22
4. Wire up the IR LED as indicated. Positive end connects, through a 220 Ohm resistor,
to 3.3V. Negative connects to the collector on the transistor,
while the emitter connects to ground. The base connects, through a 10k Ohm
resistor, to GPIO 23.

![wiring](./wiring.jpeg)

## Program Execution

For a quick and dirty setup, run

```bash
python2.7 main.py
```

from the `ir` folder.