import json
import os

file_path = "/tmp/refresh_tokens.json"

# Check if the file exists before attempting to open it
if os.path.exists(file_path):
    try:
        with open(file_path) as file:
            d = json.load(file)
            for k, v in d.items():
                cmd = f'gh secret set {k} --body "{v}"'
                os.system(cmd)
    except Exception as e:
        pass
