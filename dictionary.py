import requests, os
from spylls.hunspell import Dictionary

DIC_URL = "https://raw.githubusercontent.com/titoBouzout/Dictionaries/master/Armenian%20(Eastern).dic"
AFF_URL = "https://raw.githubusercontent.com/titoBouzout/Dictionaries/master/Armenian%20(Eastern).aff"
DIC_PATH = "data/armenian_eastern.dic"
AFF_PATH = "data/armenian_eastern.aff"


def download_dictionary():
    os.makedirs("data", exist_ok=True)
    for url, path in [(DIC_URL, DIC_PATH), (AFF_URL, AFF_PATH)]:
        if not os.path.exists(path):
            print(f"Downloading {path}...")
            r = requests.get(url)
            with open(path, "w", encoding="utf-8") as f:
                f.write(r.text)


def load_dictionary() -> Dictionary:
    download_dictionary()
    return Dictionary.from_files("data/armenian_eastern")
