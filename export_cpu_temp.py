"""Prometheus Exporter for ODROID N2's two thermal zones"""


import time

import prometheus_client as prom


def parse_temperature(path, decimal_places=3):
    """Parse temperature from temperature file

    Value will be something like '30123', which is actually 30.123"""
    with open(path) as file:
        contents = file.read()
        # Split at where the decimal should be...
        num, decimal = (
            contents[: -(decimal_places + 1)],
            contents[-(decimal_places + 1) :],
        )
        # ...then stick it in there and convert to float
        return float(f"{num}.{decimal}")


def main():
    thermal_zone_0_celsius_gauge = prom.Gauge(
        "thermal_zone_0_celsius", "Thermal zone monitor (celsius)"
    )
    thermal_zone_1_celsius_gauge = prom.Gauge(
        "thermal_zone_1_celsius", "Thermal zone monitor (celsius)"
    )
    prom.start_http_server(9190)

    while True:
        thermal_zone_0_celsius_gauge.set(
            parse_temperature("/sys/devices/virtual/thermal/thermal_zone0/temp")
        )
        thermal_zone_1_celsius_gauge.set(
            parse_temperature("/sys/devices/virtual/thermal/thermal_zone1/temp")
        )

        time.sleep(1)


if __name__ == "__main__":
    main()
