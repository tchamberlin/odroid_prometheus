import math
import os
import sys
import time

import prometheus_client as prom

import SI1132
import BME280

I2C_DEVICE_FILE = "/dev/i2c-2"

# Adapted from: https://www.omnicalculator.com/physics/dew-point#howto
# TODO: Find better source
def get_dew_point(temperature, humidity):
    a = 17.62
    b = 243.12

    α = ((a * temperature) / (b + temperature)) + math.log(humidity / 100)
    dew_point = (b * α) / (a - α)

    return dew_point


def get_altitude(pressure, seaLevel):
    atmospheric = pressure / 100.0
    return 44330.0 * (1.0 - pow(atmospheric / seaLevel, 0.1903))


def main():
    verbose = len(sys.argv) > 1
    si1132 = SI1132.SI1132(I2C_DEVICE_FILE)
    bme280 = BME280.BME280(I2C_DEVICE_FILE, 0x03, 0x02, 0x02, 0x02)

    light_uv_index_gauge = prom.Gauge("light_uv_index", "UV Index")
    light_visible_lux_gauge = prom.Gauge("light_visible_lux", "Visible Light (Lux)")
    light_ir_lux_gauge = prom.Gauge("light_ir_lux", "Infrared Light (Lux)")

    atmosphere_temperature_celcius_gauge = prom.Gauge(
        "atmosphere_temperature_celcius", "Air Temperature (C)"
    )
    atmosphere_pressure_hpa_gauge = prom.Gauge(
        "atmosphere_pressure_hpa", "Air Pressure (hPa)"
    )
    atmosphere_altitude_meters_gauge = prom.Gauge(
        "atmosphere_altitude_meters", "Altitude (m)"
    )
    atmosphere_humidity_relative_gauge = prom.Gauge(
        "atmosphere_humidity_relative", "Humidity (%)"
    )
    atmosphere_dew_point_gauge = prom.Gauge(
        "atmosphere_dew_point", "Dew Point (C)"
    )


    while True:
        light_visible_lux = si1132.readVisible()

        if verbose:
            os.system("clear")
            print(f"lux: {light_visible_lux:e}")

        time.sleep(.05)


if __name__ == "__main__":
    main()
