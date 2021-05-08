from moviepy.editor import ImageSequenceClip
from datetime import datetime, timedelta
import os

TIMELAPSE_FOLDER = "timelapses"
OUTPUT_FOLDER = "video"

if __name__ == "__main__":
    for plant_folder in os.listdir(TIMELAPSE_FOLDER):
        print(plant_folder)
        image_filename_list = []
        last_date = None
        for image_filename in os.listdir(os.path.join(TIMELAPSE_FOLDER, plant_folder)):
            date = datetime.strptime(image_filename[:-4], "%Y-%m-%dT%H:%M:%S.%fZ")
            if last_date is not None:
                dt = date - last_date
                while dt > timedelta(days=1):
                    image_filename_list.append(os.path.join(TIMELAPSE_FOLDER, plant_folder, image_filename))
                    dt -= timedelta(days=1)
            image_filename_list.append(os.path.join(TIMELAPSE_FOLDER, plant_folder, image_filename))
            last_date = date
        print(image_filename_list)
        clip = ImageSequenceClip(image_filename_list, fps=10)
        # clip.write_gif(os.path.join(OUTPUT_FOLDER, plant_folder + ".gif"))
        clip.write_videofile(filename=os.path.join(OUTPUT_FOLDER, plant_folder + ".mp4"),
                             codec="libx264", bitrate="1000000", audio=False)
