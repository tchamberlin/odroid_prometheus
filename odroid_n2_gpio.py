#!/usr/bin/env python

from pathlib import Path
import logging

import yaml

import odroid_wiringpi as wpi


logger = logging.getLogger(__name__)


def load_pin_map(pin_map_path=None):
    if pin_map_path is None:
        script_dir = Path(__file__).resolve().parent
        pin_map_path = script_dir / "odroid_n2_pin_map.yaml"

    with open(pin_map_path) as file:
        odroid_n2_pin_map = yaml.safe_load(file)

    return odroid_n2_pin_map


def read_pin(physical_pin_number, pin_map_path=None):
    odroid_n2_pin_map = load_pin_map(pin_map_path)

    return wpi.digitalRead(odroid_n2_pin_map[physical_pin_number]["wpi_num"])
