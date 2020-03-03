import argparse
import math
import os
import sys
import time

import SI1132
import BME280
import odroid_wiringpi as wpi
from odroid_n2_gpio import ODROID_N2_PIN_MAP

I2C_DEVICE_FILE = "/dev/i2c-2"

wpi.wiringPiSetup()


def main():
    args = parse_args()
    si1132 = SI1132.SI1132(I2C_DEVICE_FILE)

    requested_state = args.state

    light_visible_lux = si1132.readVisible()
    current_state = "on" if light_visible_lux > 800 else "off"

    if current_state == requested_state:
        print(f"Lights are already {current_state}; exiting")
        return False

    physical_pin_number = 11
    wpi.pinMode(physical_pin_number, 1)
    wpi.digitalWrite(
        ODROID_N2_PIN_MAP[physical_pin_number]["wpi_num"],
        1 if requested_state == "on" else 0,
    )
    time.sleep(0.5)
    light_visible_lux = si1132.readVisible()
    current_state = "on" if light_visible_lux > 800 else "off"
    if current_state != requested_state:
        print(
            f"ERROR: Changed state of pin {physical_pin_number} to {requested_state}, "
            f"but lights did not go {requested_state}",
        )
    return True


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("state", choices=("on", "off"))
    return parser.parse_args()


if __name__ == "__main__":
    main()
