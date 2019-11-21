"""
Information about callsigns for the vanity prefixes command in hamcog.
---
Copyright (C) 2019 Abigail Gold, 0x5c

This file is part of discord-qrmbot and is released under the terms of the GNU
General Public License, version 2.
"""

from collections import OrderedDict


us_calls = OrderedDict([('**Group A** (Extra Only)', ('**Any:** K, N, W (1x2)\n'
                                                      '    AA-AL, KA-KZ, NA-NZ, WA-WZ (2x1)\n'
                                                      '    AA-AL (2x2)\n'
                                                      '*Except*\n'
                                                      '**Alaska:** AL, KL, NL, WL (2x1)\n'
                                                      '**Caribbean:** KP, NP, WP (2x1)\n'
                                                      '**Pacific:** AH, KH, NH, WH (2x1)')),
                        ('**Group B** (Advanced and Extra Only)', ('**Any:** K, N, W (1x2)\n'
                                                                   '    AA-AL, KA-KZ, NA-NZ, WA-WZ (2x1)\n'
                                                                   '    AA-AL (2x2)\n'
                                                                   '*Except*\n'
                                                                   '**Alaska:** AL, KL, NL, WL (2x1)\n'
                                                                   '**Caribbean:** KP, NP, WP (2x1)\n'
                                                                   '**Pacific:** AH, KH, NH, WH (2x1)')),
                        ('**Group C** (Technician, General, Advanced, Extra Only)', ('**Any Region:** K, N, W (1x3)\n'
                                                                                     '*Except*\n'
                                                                                     '**Alaska:** KL, NL, WL (2x2)\n'
                                                                                     '**Caribbean:** NP, WP (2x2)\n'
                                                                                     '**Pacific:** KH, NH, WH (2x2)')),
                        ('**Group D** (Any License Class)', ('**Any Region:** KA-KZ, WA-WZ (2x3)\n'
                                                             '*Except*\n'
                                                             '**Alaska:** KL, WL (2x3)\n'
                                                             '**Caribbean:** KP, WP (2x3)\n'
                                                             '**Pacific:** KH, WH (2x3)')),
                        ('**Unavailable**', ('- KA2AA-KA9ZZ: reserved for US Army-authorized amateur stations in '
                                             'Japan.\n'
                                             '- KC4AAA-KC4AAF: reserved for the National Science Foundation\'s '
                                             'use at the South Pole.\n'
                                             '- KC4USA-KC4USZ: reserved for US Navy-authorized amateur stations '
                                             'at their Antarctic bases.\n'
                                             '- KG4AA-KG4ZZ: reserved for US Navy-authorized amateur stations at '
                                             'Guantanamo Bay).\n'
                                             '- KL9KAA-KL9KHZ: reserved for assignment to US personnel stationed '
                                             'in Korea.\n'
                                             'Due to the United States\' former administration of the Trust '
                                             'Territory of the Pacific Islands, '
                                             'hams in the TTPI were issued US call signs.\n'
                                             '- KC6AA-KC6ZZ -- KC6 was two DXCC entities: The Eastern Caroline '
                                             'Islands and the Western Caroline '
                                             'Islands. The Eastern Carolines became the Federated States of '
                                             'Micronesia (V6) and the Western Carolines '
                                             'became the Republic of Palau (T8).\n'
                                             '- KX6AA-KX6ZZ -- the former Marshall Islands, now the Republic of the '
                                             'Marshall Islands (V73).\n'
                                             '- Any suffix SOS or QRA-QUZ\n'
                                             '- Any 2x3 with X as the first suffix letter\n'
                                             '- Any 2x3 with AF, KF, NF, or WF prefix and suffix EMA\n'
                                             '- Any 2x3 with AA-AL, NA-NZ, WC, WK, WM, WR, or WT prefix\n'
                                             '- Any 2x1, 2x2, or 2x3 with KP, NP, WP prefix and 0, 6, 7, 8, 9 number\n'
                                             '- Any 1x1 callsign'))])
