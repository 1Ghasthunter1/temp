import subprocess

subprocess.run(
    [
        "osascript",
        "-e",
        'set the clipboard to (read (POSIX file "image.png") as «class PNGf»)',
    ]
)
