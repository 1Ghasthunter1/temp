svg_output_path = "temp.svg"
intervalMinutes = 1  # in minutes
inkscape_exec = "/Applications/Inkscape.app/Contents/MacOS/inkscape"
targetPhone = "17472737161"
imgPath = "/Users/hunterpruett/Pictures/image.png"

import subprocess
import os
import time
from datetime import datetime, timedelta
import random

start_time = datetime.now()
next_run = start_time + timedelta(
    minutes=intervalMinutes - start_time.minute % intervalMinutes,
    seconds=-start_time.second,
)
next_run.replace(second=0)

print(f"Started. First send at {next_run.strftime('%I:%M:%S %p')}")

i = 1
while True:
    curr_time = datetime.now()

    if curr_time > next_run:
        next_run = next_run + timedelta(minutes=intervalMinutes)

        subprocess.run(
            [
                "osascript",
                "scripts/send_imsg.applescript",
                targetPhone,
                f"cup noodles {i} - noro :3",
            ]
        )
        i += 1

        print(f"Sleeping. Next send at {next_run.strftime('%I:%M:%S %p')}")

    time.sleep(1)
