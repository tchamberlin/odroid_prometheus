"""Real-time monitor of light level"""

import math
import os
import sys
import time

import prometheus_client as prom

import SI1132
import BME280

I2C_DEVICE_FILE = "/dev/i2c-2"


def main():
    verbose = len(sys.argv) > 1
    si1132 = SI1132.SI1132(I2C_DEVICE_FILE)

    while True:
        light_visible_lux = si1132.readVisible()

        if verbose:
            os.system("clear")
            print(f"lux: {light_visible_lux:e}")

        time.sleep(0.05)


if __name__ == "__main__":
    main()
