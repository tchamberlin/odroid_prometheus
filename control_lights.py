"""Control state of plant room lights

Technically, we are controlling a mechanical relay via GPIO. The lights
are plugged into that.

We also have a sanity check here where we ensure that the lights have _actually_
turned changed state -- this is done by checking the light level from the
ODROID Weather Board, via I2C"""

import argparse
import time
import sys

import SI1132
import odroid_wiringpi as wpi

from odroid_n2_gpio import ODROID_N2_PIN_MAP

# https://wiki.odroid.com/odroid-n2/application_note/software/weather_board#wiring
I2C_DEVICE_FILE = "/dev/i2c-2"

LIGHTS_ON_LUX_THRESHOLD = 800


def lights_are_actually_on(threshold_lux=LIGHTS_ON_LUX_THRESHOLD):
    """Use lux to determine if lights are on or off"""
    si1132 = SI1132.SI1132(I2C_DEVICE_FILE)
    light_visible_lux = si1132.readVisible()
    current_state = "on" if light_visible_lux > threshold_lux else "off"
    return current_state


def main():
    wpi.wiringPiSetup()
    args = parse_args()

    # Get requested state from user
    requested_state = args.state
    # Get actual current state
    current_state = lights_are_actually_on()

    if current_state == requested_state:
        print(f"Lights are already {current_state}; exiting", file=sys.stderr)
        return False

    physical_pin_number = 11
    # Set pin to "write" mode
    wpi.pinMode(physical_pin_number, 1)
    # Perform the write
    wpi.digitalWrite(
        ODROID_N2_PIN_MAP[physical_pin_number]["wpi_num"],
        1 if requested_state == "on" else 0,
    )
    # Wait a bit; it takes the LED driver a few tenths to activate
    time.sleep(0.5)

    # Now the lights _should_ be on, but let's make sure
    current_state = lights_are_actually_on()
    if current_state != requested_state:
        print(
            f"ERROR: Changed state of pin {physical_pin_number} to {requested_state}, "
            f"but lights did not go {requested_state}",
            file=sys.stderr,
        )
        sys.exit(1)
    return True


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("state", choices=("on", "off"))
    return parser.parse_args()


if __name__ == "__main__":
    main()
