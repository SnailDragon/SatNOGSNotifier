##
# Sends a test email using the preferences you provided
##

from gmailClient import notifyOwners
import privateSettings

notifyOwners(privateSettings.RECIPIENT_EMAILS, "SatNOGS Notifier Test", "This is a test email")