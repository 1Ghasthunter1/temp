on run {targetBuddyPhone, imagePath}
    set image to POSIX file imagePath
    tell application "Messages"
        set targetService to 1st service whose service type = iMessage
        set targetBuddy to buddy targetBuddyPhone of targetService

        send file image to targetBuddy
    end tell
end run