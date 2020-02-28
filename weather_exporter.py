import os
import sys
import time

import prometheus_client as prom

import SI1132
import BME280

I2C_DEVICE_FILE = "/dev/i2c-2"


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

    prom.start_http_server(9191)
    print("Start server on localhost:9191")

    while True:
        light_uv_index = si1132.readUV() / 100.0
        light_uv_index_gauge.set(light_uv_index)

        light_visible_lux = si1132.readVisible()
        light_visible_lux_gauge.set(light_visible_lux)

        light_ir_lux = si1132.readIR()
        light_ir_lux_gauge.set(light_ir_lux)

        atmosphere_temperature_celcius = bme280.read_temperature()
        atmosphere_temperature_celcius_gauge.set(atmosphere_temperature_celcius)

        atmosphere_pressure_pa = bme280.read_pressure()
        atmosphere_pressure_hpa = atmosphere_pressure_pa / 100.0
        atmosphere_pressure_hpa_gauge.set(atmosphere_pressure_hpa)

        atmosphere_altitude_meters = get_altitude(atmosphere_pressure_pa, 1024.25)
        atmosphere_altitude_meters_gauge.set(atmosphere_altitude_meters)

        atmosphere_humidity_relative = bme280.read_humidity()
        atmosphere_humidity_relative_gauge.set(atmosphere_humidity_relative)

        if verbose:
            os.system('clear')
            print(f"{light_uv_index=}")
            print(f"{light_visible_lux=}")
            print(f"{light_ir_lux=}")
            print(f"{atmosphere_temperature_celcius=}")
            print(f"{atmosphere_pressure_hpa=}")
            print(f"{atmosphere_altitude_meters=}")
            print(f"{atmosphere_humidity_relative=}")

        time.sleep(1)


if __name__ == "__main__":
    main()
