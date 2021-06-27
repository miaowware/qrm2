"""
Resource schemas generator for qrm2.
---
Copyright (C) 2021 classabbyamp, 0x5c

SPDX-License-Identifier: LiLiQ-Rplus-1.1
"""


import utils.resources_models as models


print("Generating schema for index.json")
with open("./dev-notes/rs_index_schema.json", "w") as file:
    file.write(models.Index.schema_json(indent=4))

print("Done!")
