svg_output_path = "temp.svg"
intervalMinutes = 2  # in minutes
inkscape_exec = "/Applications/Inkscape.app/Contents/MacOS/inkscape"
targetPhone = "17472347450"
imgPath = "/Users/hunterpruett/Pictures/image.png"

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

    convert_svg_to_png(svg_output_path, imgPath)
    os.remove(svg_output_path)




print("STARTING...")
time.sleep(3)


def getTime():
    timeStr = datetime.datetime.now().strftime("%I:%M %p").lower()
    if timeStr[0] == "0":
        timeStr = timeStr[1:]
    return timeStr


def displayMsg():
    applescript = """
display dialog "30 SECONDS!" ¬
with title "Switch to message" ¬
with icon caution ¬
buttons {"OK"}
"""
    subprocess.call("osascript -e '{}'".format(applescript), shell=True)


def main():
    next_send_time = datetime.datetime.now()

    while True:
        if datetime.datetime.now() > next_send_time:
            next_send_time = datetime.datetime.now() + datetime.timedelta(
                minutes=random.randint(4, 8)
            )
            keyboard.write(f"it is {getTime()}", 0.5)
            keyboard.press_and_release("space")
            time.sleep(0.1)
            keyboard.press_and_release("enter")
        time.sleep(3)
        print(
            f"seconds until next send: {(next_send_time - datetime.datetime.now()).seconds}"
        )


if __name__ == "__main__":
    main()
