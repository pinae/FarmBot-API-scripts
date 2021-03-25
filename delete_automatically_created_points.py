import json
import requests
from acquire_token import get_headers

response = requests.get('https://my.farmbot.io/api/points', headers=get_headers())
points = response.json()
print(json.dumps(points, indent=2))

points_for_deletion = []
for p in points:
    if p["name"] == "Detected Plant" and p["meta"]["created_by"] == "plant-detection":
        points_for_deletion.append(str(p["id"]))
print("Deleting the following points: " + ",".join(points_for_deletion))
requests.delete('https://my.farmbot.io/api/points/' + ",".join(points_for_deletion), headers=get_headers())
