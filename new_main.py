svg_output_path = "temp.svg"
intervalMinutes = 30  # in minutes
inkscape_exec = "/Applications/Inkscape.app/Contents/MacOS/inkscape"

import subprocess
import os
import time
from datetime import datetime, timedelta
import random
import keyboard
from pynput.keyboard import Key, Controller

pynputKeyboard = Controller()

imgMap = {
    0: "./templates/leaf.svg",
    1: "./templates/prius-prime.svg",
    2: "./templates/prius-compact.svg",
    3: "./templates/prius-compact-2.svg",
    4: "./templates/prius-v.svg",
    5: "./templates/truck.svg",
}


def convert_svg_to_png(input_svg, output_png):
    try:
        subprocess.run(
            [inkscape_exec, input_svg, "-o", output_png],
            check=True,
            capture_output=True,
            text=True,
        )
        print(f"Successfully converted {input_svg} to {output_png}")
    except subprocess.CalledProcessError as e:
        print(f"Error converting SVG to PNG: {e}")
        print(f"Inkscape output: {e.output}")


def genMeme(timeInput: str, path: str):
    with open(path, "r", encoding="utf-8") as file:
        template = file.read()
    template = template.replace("--TIME--", timeInput)
    with open(svg_output_path, "w", encoding="utf-8") as file:
        file.write(template)

    convert_svg_to_png(svg_output_path, "image.png")
    os.remove(svg_output_path)


def copyMemeToClipBoard():
    subprocess.run(
        [
            "osascript",
            "-e",
            'set the clipboard to (read (POSIX file "image.png") as «class PNGf»)',
        ]
    )


# Call the function to delete the SVG file after conversion


print("STARTING...")
time.sleep(3)

last_img = 0
last_time_ran = datetime.now()
while True:
    curr_time = datetime.now()

    if (
        curr_time.minute % intervalMinutes == 0
        and last_time_ran.minute != curr_time.minute
    ):
        last_time_ran = curr_time

        while True:
            imgIdxToUse = random.randint(0, len(imgMap) - 1)
            if imgIdxToUse != last_img:
                break

        last_img = imgIdxToUse
        timeStr = curr_time.strftime("%I:%M %p").lower()
        print("sending meme of " + imgMap[imgIdxToUse] + " at " + timeStr)
        genMeme(timeStr, imgMap[imgIdxToUse])
        copyMemeToClipBoard()
        keyboard.write(f"it is {timeStr}", 0.2)
        keyboard.press_and_release("space")
        time.sleep(0.1)
        keyboard.press_and_release("backspace")
        time.sleep(0.1)
        pynputKeyboard.press(Key.cmd.value)
        pynputKeyboard.press("v")
        time.sleep(1)
        pynputKeyboard.release("v")
        pynputKeyboard.release(Key.cmd.value)
        time.sleep(0.2)
        keyboard.press_and_release("enter")

    nextSendTime = last_time_ran + timedelta(minutes=intervalMinutes) - datetime.now()
    print(
        f"sleeping. next meme in {nextSendTime.seconds // 60} mins and {nextSendTime.seconds % 60} secs"
    )
    time.sleep(1)
