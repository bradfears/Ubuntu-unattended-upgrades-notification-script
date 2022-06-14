# python script for Ubuntu unattended-upgrades
# purpose is to capture specific log file entries
# and email them to specific recipients

import socket
import smtplib
from email.mime.text import MIMEText

inputFile = "/var/log/unattended-upgrades/unattended-upgrades.log"
stringToSearchFor = "Packages that will be upgraded"
sender = '<sender email address>' # must be a validated email address in AWS
recipients = ["<recipient email addresses>"] # must be a comma-separated list
smtp = '<smtp server>' # most likely email-smtp.us-east-1.amazonaws.com
smtpPort = 465
smtpUsername = '<smtp username>' # should be something like PKIA5AYO7KA4TPGJZXB
smtpPassword = '<smtp_password>' # similar to the smtp username, but longer

logFile = open(inputFile, "r")
logData = logFile.readlines()

msg = MIMEText(logFile.read())

for line in logData:
	if stringToSearchFor in line:

		serverName = socket.gethostname()
		serverName = format(serverName)

		emailSubject = "Patches available: " + serverName
		emailBody = "Patches are available for server " + serverName + ".\n\n" + line

		message = """Subject: %s\n\n%s """ % (emailSubject, emailBody)

		#print(message)

		smtpServer = smtplib.SMTP_SSL(smtp, port=smtpPort)
		smtpServer.login(smtpUsername, smtpPassword)
		#smtpServer.sendmail(sender, recipients, msg.as_string())
		smtpServer.sendmail(sender, recipients, message)
		smtpServer.quit()
