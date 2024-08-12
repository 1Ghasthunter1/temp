import time
import datetime
import keyboard
import random

print("STARTING...")
time.sleep(3)


def getTime():
    timeStr = datetime.datetime.now().strftime("%I:%M %p").lower()
    if timeStr[0] == "0":
        timeStr = timeStr[1:]
    return timeStr


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
        print(f"seconds until next send: {(next_send_time - datetime.datetime.now()).seconds}")


if __name__ == "__main__":
    main()
