"""
Common tools for the bot.
---
Copyright (C) 2019 Abigail Gold, 0x5c

This file is part of discord-qrmbot and is released under the terms of the GNU
General Public License, version 2.
---

`colours`: Colours used by embeds.

`cat`: Category names for the HelpCommand.
"""

from types import SimpleNamespace


colours = SimpleNamespace(good=0x43B581,
                          neutral=0x7289DA,
                          bad=0xF04747)
# meow
cat = SimpleNamespace(lookup='Information Lookup',
                      fun='Fun',
                      maps='Mapping',
                      ref='Reference',
                      study='Exam Study',
                      weather='Land and Space Weather')
