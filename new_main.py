import subprocess
import os
import time
from datetime import datetime, timedelta
import random
import keyboard
from pynput.keyboard import Key, Controller

svg_output_path = "temp.svg"
intervalMinutes = 30

inkscape_exec = "/Applications/Inkscape.app/Contents/MacOS/inkscape"


pynputKeyboard = Controller()

imgMap = {
    0: "./templates/leaf.svg",
    1: "./templates/prius-prime.svg",
    2: "./templates/prius-compact.svg",
    3: "./templates/prius-compact-2.svg",
    4: "./templates/prius-v.svg",
    5: "./templates/truck.svg",
}


def displayMsg():
    applescript = """
display dialog "30 SECONDS!" ¬
with title "Switch to message" ¬
with icon caution ¬
buttons {"OK"}
"""
    subprocess.call("osascript -e '{}'".format(applescript), shell=True)


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


def getNextTime(lastTime: datetime):
    return (
        lastTime
        + timedelta(minutes=intervalMinutes)
        - timedelta(minutes=(lastTime.minute % intervalMinutes))
    ).replace(second=0, microsecond=0)


# Call the function to delete the SVG file after conversion
# displayMsg()

print("STARTING...")
time.sleep(3)

last_img = 0

timeToSendNextMsg = getNextTime(datetime.now())
timeToSendWarning = timeToSendNextMsg - timedelta(seconds=30)
while True:
    curr_time = datetime.now()

    if timeToSendWarning is not None and timeToSendWarning < curr_time:
        # displayMsg()
        timeToSendWarning = timeToSendWarning + timedelta(minutes=intervalMinutes)

    if timeToSendNextMsg is None or timeToSendNextMsg < curr_time:

        timeToSendNextMsg = getNextTime(curr_time)
        timeToSendWarning = timeToSendNextMsg - timedelta(seconds=30)

        print(timeToSendNextMsg)
        print(timeToSendWarning)

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

    print(
        f"time to next send: {timeToSendNextMsg.strftime('%I:%M:%S:%f %p')} ({round((timeToSendNextMsg - curr_time).total_seconds())}s)"
    )
    print(
        f"time to next warning: {timeToSendWarning.strftime('%I:%M:%S:%f %p')} ({round((timeToSendWarning - curr_time).total_seconds())}s)"
    )
    time.sleep(1)
