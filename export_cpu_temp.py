import prometheus_client as prom
import time


def parse_temperature(path, decimal_places=3):
    with open(path) as file:
        contents = file.read()
        num, decimal = (
            contents[: -(decimal_places + 1)],
            contents[-(decimal_places + 1) :],
        )
        return float(f"{num}.{decimal}")


if __name__ == "__main__":

    thermal_zone_0_celcius_gauge = prom.Gauge(
        "thermal_zone_0_celcius", "Thermal zone monitor (celcius)"
    )
    thermal_zone_1_celcius_gauge = prom.Gauge(
        "thermal_zone_1_celcius", "Thermal zone monitor (celcius)"
    )
    prom.start_http_server(9190)

    while True:
        thermal_zone_0_celcius_gauge.set(
            parse_temperature("/sys/devices/virtual/thermal/thermal_zone0/temp")
        )
        thermal_zone_1_celcius_gauge.set(
            parse_temperature("/sys/devices/virtual/thermal/thermal_zone1/temp")
        )

        time.sleep(1)
