# Raspberry Pi AC Controller

## Overview

The repository houses code for a basic closed-loop controller meant to
bring my air conditioning unit out of the Stone Age into the 21st
century.

## AC Unit

The AC unit has several inputs:

1. Power (on/off)
2. Energy Saver Mode (on/off)
3. Fan Speed (low/hi)
4. Cool Strength (dial)

However, the cool strength dial pretty much doesn't work. Below 5 (on
a range from 1 to 10) the unit never turns on, and above 5 it is always
on.

## The Solution

So how can we solve the problem through overcomplication? What about
a timer outlet that turns the unit off and on every 30 minutes? Too easy.
Build a robot to turn the unit on and off based on the current temperature
in the room.

## Components

1. Raspberry Pi with WiFi dongle and SD card (case, if you please)
2. Half-size breadboard
3. Jumper cables
3. 2 red 3mm LEDs
4. 2 330 Ohm resistors (220 Ohm is fine too)
5. TMP36 analog temperature sensor
6. SG92R micro servo
7. Power on/off push button
8. A minor amount of programming skill

## The System

The AC unit has a hard constraint that it should not be turned on within 3
minutes of turning it off. Let's keep that in mind as we design. When the
temperature drops below 73 degrees, let's turn the AC unit off. And when the
temperature goes above 75 degrees, let's turn the AC unit on. Can we
dampen the system a little to prevent constant on/off behavior? Sure.
When the temperature drops below 73 degrees on average over 1 minute,
turn the unit off. Over 75 degrees on average over 1 minute? Turn the unit
on. Oh, all the while ensuring we don't switch on or off within 3 minutes.

We can mount the servo like the figure below (add figure), meaning
no additional parts are required. It may be best to hot glue or foam
tape the servo to get the right mounting.

How about configurability? We'll build a web portal and API for the user
to go in and make changes to their settings. They can turn the system
on and off, increase or decrease their set temperature, or full
override the system to have the AC always on.

The power button can be a physical switch to interface against the web
portal. Pressing the power button once will either completely shut down
the system or start it up again (don't forget the 3 minute rule). Pressing
the power button twice will engage full override to have the AC always on.

## The Code

I guess I gotta write something now.
