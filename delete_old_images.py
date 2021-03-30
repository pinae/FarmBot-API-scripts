import json
import requests
from acquire_token import get_headers
from datetime import datetime, timedelta
import pytz

response = requests.get('https://my.farmbot.io/api/images', headers=get_headers())
images = response.json()
print(json.dumps(images, indent=2))
now = datetime.now(tz=pytz.timezone("Europe/Berlin"))
for image in images:
    create_date = datetime.strptime(image["created_at"], "%Y-%m-%dT%H:%M:%S.%fZ")
    create_date = create_date.replace(tzinfo=pytz.timezone("Europe/Berlin"))
    print(str(create_date) + " < " + str(now - timedelta(days=1, hours=12)) +
          " = " + str(create_date < now - timedelta(days=1, hours=12)))
    if create_date < now - timedelta(days=1, hours=12):
        print("Deleting because of old age: " + str(image["id"]))
        requests.delete('https://my.farmbot.io/api/images/' + str(image["id"]), headers=get_headers())
    else:
        print("Keeping image: " + str(image["id"]))
