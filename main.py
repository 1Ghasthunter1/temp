svg_output_path = "temp.svg"
intervalMinutes = 30  # in minutes
inkscape_exec = "/Applications/Inkscape.app/Contents/MacOS/inkscape"
targetPhone = "17472347450"
imgPath = "/Users/hunterpruett/Pictures/image.png"

import subprocess
import os
import time
from datetime import datetime, timedelta
import random

imgMap = {
    0: "./templates/leaf.svg",
    1: "./templates/prius-prime.svg",
    2: "./templates/prius-compact.svg",
    3: "./templates/prius-compact-2.svg",
    4: "./templates/prius-v.svg",
    5: "./templates/truck.svg",
}
last_img = 0


def convert_svg_to_png(input_svg, output_png):
    try:
        subprocess.run(
            [inkscape_exec, input_svg, "-o", output_png],
            check=True,
            capture_output=True,
            text=True,
        )
        #print(f"Successfully converted {input_svg} to {output_png}")
    except subprocess.CalledProcessError as e:
        print(f"Error converting SVG to PNG: {e}")
        print(f"Inkscape output: {e.output}")


def genMeme(timeInput: str, path: str):
    with open(path, "r", encoding="utf-8") as file:
        template = file.read()
    template = template.replace("--TIME--", timeInput)
    with open(svg_output_path, "w", encoding="utf-8") as file:
        file.write(template)

    convert_svg_to_png(svg_output_path, imgPath)
    os.remove(svg_output_path)


print("STARTING...")
# time.sleep(3)


def getTimeString(dt: datetime):
    timeStr = dt.strftime("%I:%M %p").lower()
    if timeStr[0] == "0":
        timeStr = timeStr[1:]
    return timeStr

def prep(dt: datetime):
    global last_img
    timeStr = getTimeString(dt)

    while True:
        imgIdxToUse = random.randint(0, len(imgMap) - 1)
        if imgIdxToUse != last_img:
            break
    last_img = imgIdxToUse
    genMeme(timeStr, imgMap[imgIdxToUse])
    print(f'image prepared for {timeStr}')


start_time = datetime.now()
next_run = start_time + timedelta(
    minutes=intervalMinutes - start_time.minute % intervalMinutes,
    seconds=-start_time.second,
)
next_run.replace(second=0)

print(
    f"Started. First send at {next_run.strftime("%I:%M:%S %p")}"
)

prep(next_run)

while True:
    curr_time = datetime.now()

    if curr_time > next_run:
        timeStr = getTimeString(next_run)
        next_run = next_run + timedelta(minutes=intervalMinutes)

        print(f"sending meme for {timeStr}")

        subprocess.run(
            [
                "osascript",
                "scripts/send_imsg_img.applescript",
                targetPhone,
                imgPath,
                f"it is {timeStr}",
            ]
        )

        prep(next_run)

        print(
            f"Sleeping. Next send at {next_run.strftime("%I:%M:%S %p")}"
        )

    
    time.sleep(1)
