import prometheus_client as prom
import time


from odroid_n2_gpio import read_pin


def main():
    lights = prom.Enum(
        "lights_state", "State of plant room lights (commanded)", states=["on", "off"],
    )

    prom.start_http_server(9192)

    while True:
        lights_control_pin_state = read_pin(11)
        lights.state("on") if lights_control_pin_state == 1 else lights.state("off")
        time.sleep(1)


if __name__ == "__main__":
    main()
