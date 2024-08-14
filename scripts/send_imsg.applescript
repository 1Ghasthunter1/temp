on run {targetBuddyPhone, targetMessage}
    tell application "Messages"
        send "${message}" to buddy "${targetBuddyPhone}"
    end tell
end run