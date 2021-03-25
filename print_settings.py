import json
import requests
from acquire_token import get_headers


def get_firmware_config():
    response = requests.get('https://my.farmbot.io/api/firmware_config', headers=get_headers())
    return response.json()


def get_axis_length(firmware_config, axis="x"):
    return firmware_config["movement_axis_nr_steps_" + axis] / firmware_config["movement_step_per_mm_" + axis]


if __name__ == "__main__":
    firmware_config = get_firmware_config()
    print(json.dumps(firmware_config, indent=2))
    print("Length of the X axis: {:f}".format(get_axis_length(firmware_config, "x")))
    print("Length of the Y axis: {:f}".format(get_axis_length(firmware_config, "y")))
    print("Length of the Z axis: {:f}".format(get_axis_length(firmware_config, "z")))
