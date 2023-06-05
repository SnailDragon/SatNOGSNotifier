# TEMPLATE
# rename privateSettings.py and fill in your own settings

# your ground station number
GROUND_STATION = 0

# gmail address and login key to send from 
MY_EMAIL = "exammple@gmail.com"
GMAIL_LOGIN_KEY = "some 16 character code"

# emails to send to 
RECIPIENT_EMAILS = ["exampleRecipient@gmail.com", "exampleRecipient2@gmail.com"]

# true to have the program try to fix the system with a reboot before notifying you
# NOTE: it does this by only notifying you if it finds "failed" and it has been rebooted less than the MAX_ALLOWED_TIME_SINCE_REBOOT_S in the past
ENABLE_AUTO_REBOOT = True
MAX_ALLOWED_TIME_SINCE_REBOOT_S = 60 * 60 * 24 # 1 day in seconds