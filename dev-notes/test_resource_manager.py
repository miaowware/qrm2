from pathlib import Path
from utils.resources_manager import ResourcesManager


path = Path("./data/resources")
url = "https://qrmresources.miaow.io/resources/"
versions = {
        "bandcharts": "v1",
        "img": "v1",
        "maps": "v1",
        "morse": "v1",
        "phonetics": "v1",
        "qcodes": "v1",
        "funetics": "v1"
    }

rm = ResourcesManager(path, url, versions)
print(rm.index)
