"""
Conversion extension for qrm
---
Copyright (C) 2020 Abigail Gold, 0x5c

This file is part of qrm2 and is released under the terms of
the GNU General Public License, version 2.
"""


import math
from enum import Enum
from typing import Optional

import discord.ext.commands as commands

import common as cmn
from data import options as opt


# not sure why but UnitConverter and Unit need to be defined before DbConvCog and convert()
class UnitConverter(commands.Converter):
    async def convert(self, ctx: commands.Context, argument: str):
        try:
            return Unit(argument)
        except ValueError as e:
            raise commands.BadArgument(message=str(e))


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


class DbConvCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(name="dbconv", aliases=["dbc"], category=cmn.cat.ref)
    async def _db_conv(self, ctx: commands.Context,
                       value: Optional[float] = None,
                       unit_from: Optional[UnitConverter] = None,
                       unit_to: Optional[UnitConverter] = None):
        """
        Convert between decibels and scalar values for voltage, power, and antenna gain.

        **Valid Units**
        *Voltage:* V, mV, µV, uV, dBV, dBmV, dBµV, dBuV
        *Power:* fW, mW, W, kW, dBf, dBm, dBW, dBk
        *Antenna Gain:* dBi, dBd, dBq
        """
        embed = cmn.embed_factory(ctx)
        if value is not None and unit_from is not None and unit_to is not None:
            converted = convert(value, unit_from, unit_to)

            embed.title = f"{value:.3g} {unit_from} = {converted:.3g} {unit_to}"
            embed.colour = cmn.colours.good
        else:
            embed.title = "Decibel Quick Reference"
            embed.description = (
                "Decibels are a great way to easily represent large quantities that are common in electronics. "
                "There are a few main types that are used often in radio: voltage, power, and antenna gain. "
                "Here are some commonly-used reference levels for each type:"
            )
            v_db_info = ("**dBV** = relative to 1 V\n"
                         "**dBmV** = relative to 1 mV (1e-3 V)\n"
                         "**dBµV** = relative to 1 µV (1e-6 V)")
            embed.add_field(name="Voltage Decibels", value=v_db_info, inline=False)
            p_db_info = ("**dBW** = relative to 1 W\n"
                         "**dBk** = relative to 1 kW (1e3 W)\n"
                         "**dBm** = relative to 1 mW (1e-3 W)\n"
                         "**dBf** = relative to 1 fW (1e-15 W)")
            embed.add_field(name="Power Decibels", value=p_db_info, inline=False)
            a_db_info = ("**dBi** = relative to a theoretical __i__sotropic radiator in free space "
                         "(equal radiation in all directions)\n"
                         "**dBd** = relative to a dipole in free space (0 dBd = 2.15 dBi)\n"
                         "**dBq** = relative to a quarter-wave antenna in free space (0 dBq = -0.85 dBi)")
            embed.add_field(name="Antenna Gain Decibels", value=a_db_info, inline=False)
            embed.add_field(name="Use the bot to do the conversions",
                            value=f"`{opt.display_prefix}dbconv [value] [unit_from] [unit_to]`",
                            inline=False)
        await ctx.send(embed=embed)


def setup(bot: commands.Bot):
    bot.add_cog(DbConvCog(bot))


def convert(initial: float, unit1: Unit, unit2: Unit):
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
            initial = float(ip[0])
            unit1 = Unit(ip[1])
            unit2 = Unit(ip[2])
            conv = convert(initial, unit1, unit2)
            print(f"{initial:.2f} {unit1} = {conv:.2f} {unit2}")
        except ValueError as e:
            print(e)
