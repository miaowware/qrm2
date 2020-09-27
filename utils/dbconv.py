"""
Some handy functions and classes to handle voltage/power/antenna gain in dB and scalar units
---
Copyright (C) 2020 Abigail Gold, 0x5c

This file is part of qrm2 and is released under the terms of
the GNU General Public License, version 2.
"""


import math
from enum import Enum


__all__ = ["DbConverter"]


class DbConverter:
    def __init__(self, value: float, unit1: str, unit2: str):
        self.initial: float = value
        self.unit1: Unit = Unit(unit1)
        self.unit2: Unit = Unit(unit2)
        self.converted: float = self._convert(self.initial, self.unit1, self.unit2)

    def _convert(self, initial: float, unit1, unit2):
        if unit1.type == unit2.type:
            # dB to dB
            if unit1.is_db and unit2.is_db:
                if unit1.mult == unit2.mult:
                    return initial
                elif unit1.type == UnitType.voltage:
                    return _calc_volt_db(_calc_volt(initial, unit1.mult), unit2.mult)
                elif unit1.type == UnitType.power:
                    return _calc_power_db(_calc_power(initial, unit1.mult), unit2.mult)
                elif unit1.type == UnitType.antenna:
                    return initial + (unit1.mult - unit2.mult)
            # V/W to V/W
            elif not unit1.is_db and not unit2.is_db:
                if unit1.mult == unit2.mult:
                    return initial
                return initial * unit1.mult / unit2.mult
            # dB to V/W
            elif unit1.is_db and not unit2.is_db:
                if unit1.type == UnitType.voltage:
                    return _calc_volt(initial, unit1.mult) / unit2.mult
                elif unit1.type == UnitType.power:
                    return _calc_power(initial, unit1.mult) / unit2.mult
            # V/W to dB
            elif not unit1.is_db and unit2.is_db:
                if unit1.type == UnitType.voltage:
                    return _calc_volt_db(initial * unit1.mult, unit2.mult)
                elif unit1.type == UnitType.power:
                    return _calc_power_db(initial * unit1.mult, unit2.mult)
        raise ValueError(f"Can't convert between {unit1} and {unit2}")


class Unit:
    def __init__(self, raw: str):
        self.raw: str = raw
        self.unit: str
        self.type: UnitType
        self.is_db: bool
        self.mult: int
        self._parse()

    def _parse(self):
        s = self.raw.lower()
        if len(s) > 2 and s[:2] == "db":
            self.is_db = True
            if s[2:] in units:
                u = units[s[2:]]
                self.mult = u["mult"]
                self.unit = u["log"]
                self.type = u["type"]
        elif s in units:
            self.is_db = False
            u = units[s]
            self.mult = u["mult"]
            self.unit = u["scalar"]
            self.type = u["type"]
        else:
            raise ValueError(f"Invalid unit: {self.raw}")

    def __str__(self):
        return self.unit


class UnitType(Enum):
    voltage = 1
    power = 2
    antenna = 3


units = {
    # voltage
    "uv": {"mult": 1e-6,  "scalar": "µV", "log": "dBµV", "type": UnitType.voltage},
    "µv": {"mult": 1e-6,  "scalar": "µV", "log": "dBµV", "type": UnitType.voltage},
    "mv": {"mult": 1e-3,  "scalar": "mV", "log": "dBmV", "type": UnitType.voltage},
    "v":  {"mult": 1,     "scalar":  "V", "log":  "dBV", "type": UnitType.voltage},
    # power
    "fw": {"mult": 1e-15, "scalar": "fW", "log":  "dBf", "type": UnitType.power},
    "f":  {"mult": 1e-15, "scalar": "fW", "log":  "dBf", "type": UnitType.power},
    "mw": {"mult": 1e-3,  "scalar": "mW", "log":  "dBm", "type": UnitType.power},
    "m":  {"mult": 1e-3,  "scalar": "mW", "log":  "dBm", "type": UnitType.power},
    "w":  {"mult": 1,     "scalar":  "W", "log":  "dBW", "type": UnitType.power},
    "kw": {"mult": 1e3,   "scalar": "kW", "log":  "dBk", "type": UnitType.power},
    "k":  {"mult": 1e3,   "scalar": "kW", "log":  "dBk", "type": UnitType.power},
    # antenna
    "q":  {"mult": -0.85, "scalar": None, "log":  "dBq", "type": UnitType.antenna},
    "i":  {"mult": 0,     "scalar": None, "log":  "dBi", "type": UnitType.antenna},
    "d":  {"mult": 2.15,  "scalar": None, "log":  "dBd", "type": UnitType.antenna},
}


def _calc_power_db(p: float, ref: float):
    return 10 * math.log10(p / ref)


def _calc_power(db: float, ref: float):
    return 10 ** (db / 10) * ref


def _calc_volt_db(v: float, ref: float):
    return 20 * math.log10(v / ref)


def _calc_volt(db: float, ref: float):
    return 10 ** (db / 20) * ref


# testing code
if __name__ == "__main__":
    while(True):
        try:
            ip = input("> ").split()
            conv = DbConverter(float(ip[0]), ip[1], ip[2])
            print(f"{conv.initial:.2f} {conv.unit1} = {conv.converted:.2f} {conv.unit2}")
        except ValueError as e:
            print(e)
