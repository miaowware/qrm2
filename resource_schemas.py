"""
Resource schemas generator for qrm2.
---
Copyright (C) 2021-2023 classabbyamp, 0x5c

SPDX-License-Identifier: LiLiQ-Rplus-1.1
"""

import json

import utils.resources_models as models


print("Generating schema for index.json")
with open("./dev-notes/rs_index_schema.json", "w") as file:
    json.dump(models.Index.model_json_schema(), file)

print("Done!")
