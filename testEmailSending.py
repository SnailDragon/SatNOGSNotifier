##
# Sends a test email using the preferences you provided
##

from gmailClient import notifyOwners
import privateSettings
from datetime import datetime

notifyOwners(privateSettings.RECIPIENT_EMAILS, "SatNOGS Notifier Test", f"This is a test email sent on {datetime.now()}")