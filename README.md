# SatNOGSNotifier
Scrip used with SatNOGS (https://satnogs.org/) ground stations to notify the owner via email when it is failing to pick up signals. <br>

The main script is checkSignalStatus.py, when run it will output logs to checkSignalStatus.log - currently it writes to SatNOGSNotifier/checkSignalStatus.log on the assumption that you are running it in the home folder. <br>

I suggest regularly running this script using crontab
NOTE: it needs to be run more regularly than MAX_ALLOWED_TIME_SINCE_REBOOT_S or it won't stop trying to reboot and just send you an email
```

```

Rename the file "privateSettingsTEMPLATE.py" to "privateSettings.py" and fill in your information before trying to run the program.

The email code I used was based on this guide:<br> https://towardsdatascience.com/how-to-easily-automate-emails-with-python-8b476045c151 <br>You can follow the beginning of it (Step 1) to learn how to get your GMAIL_LOGIN_KEY value
