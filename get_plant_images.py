import json
import requests
from acquire_token import get_headers
from print_settings import get_firmware_config, get_axis_length
import os


def download_image(url, filename):
    response = requests.get(url, allow_redirects=True)
    open(filename, 'wb').write(response.content)


def get_path(plant_id, name):
    folder_name = "{:s}-{:d}".format(name, plant_id)
    if folder_name not in os.listdir("timelapses"):
        os.mkdir(os.path.join("timelapses", folder_name))
    return os.path.join("timelapses", folder_name)


def save_image(url, plant_id, name, date_str):
    path = get_path(plant_id, name)
    download_image(url, os.path.join(path, date_str + ".jpg"))


response = requests.get('https://my.farmbot.io/api/images', headers=get_headers())
images = response.json()
print(json.dumps(images, indent=2))
response = requests.post('https://my.farmbot.io/api/points/search', headers=get_headers(),
                         data=json.dumps({"pointer_type": "Plant"}))
plants = response.json()
print(json.dumps(plants, indent=2))
y_length = get_axis_length(get_firmware_config(), "y")
for plant in plants:
    for image in images:
        if image["meta"]["x"] == plant["x"] and \
                round(image["meta"]["y"]) == min(round(y_length), round(plant["y"] + 72)):
            print("Image coords: ({:.1f}, {:.1f}) - Plant coords: ({:.1f}, {:.1f})".format(
                image["meta"]["x"], image["meta"]["y"], plant["x"], plant["y"]))
            print("Saving plant {:s} with id {:d}.".format(plant["name"], plant["id"]))
            save_image(image["attachment_url"], plant["id"], plant["name"], image["created_at"])
            print("Deleting: " + str(image["id"]))
            requests.delete('https://my.farmbot.io/api/images/' + str(image["id"]), headers=get_headers())
