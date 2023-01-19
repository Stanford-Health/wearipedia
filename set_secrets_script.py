import json
import os

d = json.load(open("/tmp/refresh_tokens.json"))

for k, v in d.items():
    cmd = f'gh secret set {k} --body "{v}"'
    print(cmd)
    os.system(cmd)
