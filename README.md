# SatNOGSNotifier
Scrip used with SatNOGS (https://satnogs.org/) ground stations to notify the owner when it is failing to pick up signals. 


Create a file called "privateSettings.py" and include this information in it:
```
# your ground station number
GROUND_STATION = 0

# gmail address and login key to send from 
MY_EMAIL = "exammple@gmail.com"
GMAIL_LOGIN_KEY = "some 16 character code"

# emails to send to 
RECIPIENT_EMAILS = ["exampleRecipient@gmail.com", "exampleRecipient2@gmail.com"]

# true to have the program try to fix the system with a reboot before notifying you
# NOTE: it does this by only notifying you if it finds "failed" and it has been rebooted 
# less than the MAX_ALLOWED_TIME_SINCE_REBOOT_S in the past
ENABLE_AUTO_REBOOT = True
MAX_ALLOWED_TIME_SINCE_REBOOT_S = 60 * 60 * 24 # 1 day in seconds
```

The email code I used was based on this guide:<br> https://towardsdatascience.com/how-to-easily-automate-emails-with-python-8b476045c151 <br>You can follow the beginning of it (Step 1) to learn how to get your GMAIL_LOGIN_KEY value
