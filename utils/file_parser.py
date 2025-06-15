import json
import tempfile
import zipfile
from typing import List

def extract_json_files(file: bytes) -> List[dict]:
    with tempfile.TemporaryDirectory() as tmpdir:
        with open(f"{tmpdir}/temp.zip", "wb") as f:
            f.write(file)

        with zipfile.ZipFile(f"{tmpdir}/temp.zip", "r") as zip_ref:
            zip_ref.extractall(tmpdir)

        json_data_list = []
        for filename in zip_ref.namelist():
            if filename.endswith(".json"):
                with open(f"{tmpdir}/{filename}", "r", encoding="utf-8") as json_file:
                    try:
                        data = json.load(json_file)
                        json_data_list.append(data)
                    except json.JSONDecodeError:
                        continue

        return json_data_list
