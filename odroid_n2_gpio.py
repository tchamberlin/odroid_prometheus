#!/usr/bin/env python

import argparse
import logging

import odroid_wiringpi as wpi


logger = logging.getLogger(__name__)

# Composed from: https://wiki.odroid.com/odroid-n2/hardware/expansion_connectors
ODROID_N2_PIN_MAP = {
    1: {
        "v": None,
        "mode": None,
        "name": "3.3V",
        "wpi_num": None,
        "io": None,
        "long_name": "3.3V Power",
    },
    2: {
        "v": None,
        "mode": None,
        "name": "5V",
        "wpi_num": None,
        "io": None,
        "long_name": "5.0V Power",
    },
    3: {
        "v": 1,
        "mode": "ALT1",
        "name": "SDA.2",
        "wpi_num": 8,
        "io": 493,
        "long_name": "I2C_EE_M2_SDA/GPIOX_17(#)",
    },
    4: {
        "v": None,
        "mode": None,
        "name": "5V",
        "wpi_num": None,
        "io": None,
        "long_name": "5.0V Power",
    },
    5: {
        "v": 1,
        "mode": "ALT1",
        "name": "SCL.2",
        "wpi_num": 9,
        "io": 494,
        "long_name": "I2C_EE_M2_SCL/GPIOX_18(#)",
    },
    6: {
        "v": None,
        "mode": None,
        "name": "0V",
        "wpi_num": None,
        "io": None,
        "long_name": "Ground",
    },
    7: {
        "v": 1,
        "mode": "ALT1",
        "name": "IO.473",
        "wpi_num": 7,
        "io": 473,
        "long_name": "SPDIF_OUT/GPIOA_13(#)",
    },
    8: {
        "v": 1,
        "mode": "IN",
        "name": "TxD1",
        "wpi_num": 15,
        "io": 488,
        "long_name": "GPIOX_12(#)/UART_EE_A_TX",
    },
    9: {
        "v": None,
        "mode": None,
        "name": "0V",
        "wpi_num": None,
        "io": None,
        "long_name": "Ground",
    },
    10: {
        "v": 1,
        "mode": "IN",
        "name": "RxD1",
        "wpi_num": 16,
        "io": 489,
        "long_name": "GPIOX_13(#)/UART_EE_A_RX",
    },
    11: {
        "v": 1,
        "mode": "OUT",
        "name": "IO.479",
        "wpi_num": 0,
        "io": 479,
        "long_name": "PWM_D/GPIOX_3(#)",
    },
    12: {
        "v": 1,
        "mode": "IN",
        "name": "IO.492",
        "wpi_num": 1,
        "io": 492,
        "long_name": "GPIOX_16(#)/PWM_E",
    },
    13: {
        "v": 1,
        "mode": "IN",
        "name": "IO.480",
        "wpi_num": 2,
        "io": 480,
        "long_name": "GPIO_4(#)",
    },
    14: {
        "v": None,
        "mode": None,
        "name": "0V",
        "wpi_num": None,
        "io": None,
        "long_name": "Ground",
    },
    15: {
        "v": 1,
        "mode": "IN",
        "name": "IO.483",
        "wpi_num": 3,
        "io": 483,
        "long_name": "PWM_B/PWM_F/GPIOX_7(#)",
    },
    16: {
        "v": 1,
        "mode": "IN",
        "name": "IO.476",
        "wpi_num": 4,
        "io": 476,
        "long_name": "GPIOX_0(#)",
    },
    17: {
        "v": None,
        "mode": None,
        "name": "3.3V",
        "wpi_num": None,
        "io": None,
        "long_name": "3.3V Power",
    },
    18: {
        "v": 1,
        "mode": "IN",
        "name": "IO.477",
        "wpi_num": 5,
        "io": 477,
        "long_name": "GPIOX_1(#)",
    },
    19: {
        "v": 1,
        "mode": "IN",
        "name": "MOSI",
        "wpi_num": 12,
        "io": 484,
        "long_name": "SPI_A_MOSI/GPIOX_8(#)",
    },
    20: {
        "v": None,
        "mode": None,
        "name": "0V",
        "wpi_num": None,
        "io": None,
        "long_name": "Ground",
    },
    21: {
        "v": 1,
        "mode": "IN",
        "name": "MISO",
        "wpi_num": 13,
        "io": 485,
        "long_name": "SPI_A_MOSO/GPIOX_9(#)",
    },
    22: {
        "v": 1,
        "mode": "IN",
        "name": "IO.478",
        "wpi_num": 6,
        "io": 478,
        "long_name": "GPIOX_2(#)",
    },
    23: {
        "v": 1,
        "mode": "IN",
        "name": "SCLK",
        "wpi_num": 14,
        "io": 487,
        "long_name": "SPI_A_SCLK/GPIOX_11(#)",
    },
    24: {
        "v": 1,
        "mode": "IN",
        "name": "CE0",
        "wpi_num": 10,
        "io": 486,
        "long_name": "GPIOX_10(#)/SPI_A_SSO",
    },
    25: {
        "v": None,
        "mode": None,
        "name": "0V",
        "wpi_num": None,
        "io": None,
        "long_name": "Ground",
    },
    26: {
        "v": 0,
        "mode": "IN",
        "name": "IO.464",
        "wpi_num": 11,
        "io": 464,
        "long_name": "GPIOX_4(#)",
    },
    27: {
        "v": 1,
        "mode": "ALT2",
        "name": "SDA.3",
        "wpi_num": 30,
        "io": 474,
        "long_name": "I2C_EE_M3_SDA/GPIOA_14(#)",
    },
    28: {
        "v": 1,
        "mode": "ALT2",
        "name": "SCL.3",
        "wpi_num": 31,
        "io": 475,
        "long_name": "GPIOX_15(#)/I2C_EE_M3_SCL",
    },
    29: {
        "v": 1,
        "mode": "IN",
        "name": "IO.490",
        "wpi_num": 21,
        "io": 490,
        "long_name": "UART_EE_A_CTS/GPIOX_14(#)",
    },
    30: {
        "v": None,
        "mode": None,
        "name": "0V",
        "wpi_num": None,
        "io": None,
        "long_name": "Ground",
    },
    31: {
        "v": 1,
        "mode": "IN",
        "name": "IO.491",
        "wpi_num": 22,
        "io": 491,
        "long_name": "UART_EE_A_RTS/GPIOX_15(#)",
    },
    32: {
        "v": 0,
        "mode": "IN",
        "name": "IO.472",
        "wpi_num": 26,
        "io": 472,
        "long_name": "GPIOA_12(#)",
    },
    33: {
        "v": 1,
        "mode": "IN",
        "name": "IO.481",
        "wpi_num": 23,
        "io": 481,
        "long_name": "PWM_C/GPIOX_5(#)",
    },
    34: {
        "v": None,
        "mode": None,
        "name": "0V",
        "wpi_num": None,
        "io": None,
        "long_name": "Ground",
    },
    35: {
        "v": 0,
        "mode": "IN",
        "name": "IO.482",
        "wpi_num": 24,
        "io": 482,
        "long_name": "PWM_D/GPIOX_6(#)",
    },
    36: {
        "v": 1,
        "mode": "OUT",
        "name": "IO.495",
        "wpi_num": 27,
        "io": 495,
        "long_name": "PWM_8/GPIOX_19(#)",
    },
    37: {
        "v": None,
        "mode": None,
        "name": "AIN.3",
        "wpi_num": 25,
        "io": None,
        "long_name": "ADC.AIN3",
    },
    38: {
        "v": None,
        "mode": None,
        "name": "1V8",
        "wpi_num": 28,
        "io": None,
        "long_name": "VDDIO_AO1V8",
    },
    39: {
        "v": None,
        "mode": None,
        "name": "0V",
        "wpi_num": None,
        "io": None,
        "long_name": "Ground",
    },
    40: {
        "v": None,
        "mode": None,
        "name": "AIN.2",
        "wpi_num": 29,
        "io": None,
        "long_name": "ADC.AIN2",
    },
}


def read_pin(physical_pin_number):
    if physical_pin_number is not None:
        return wpi.digitalRead(ODROID_N2_PIN_MAP[physical_pin_number]["wpi_num"])


def main():
    # TODO: Where do we put this?
    wpi.wiringPiSetup()
    args = parse_args()
    if args.verbose:
        init_logging(logging.DEBUG)
    else:
        init_logging(logging.INFO)

    gpio()


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--verbose", action="store_true")
    return parser.parse_args()


def init_logging(level):
    """Initialize logging"""
    logging.getLogger().setLevel(level)
    _logger = logging.getLogger(__name__)
    console_handler = logging.StreamHandler()
    # console_handler = logging.StreamHandler()
    console_handler.setFormatter(logging.Formatter("%(levelname)s %(message)s"))
    _logger.addHandler(console_handler)
    _logger.setLevel(level)


if __name__ == "__main__":
    main()
