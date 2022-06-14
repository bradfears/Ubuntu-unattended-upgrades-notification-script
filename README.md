# Ubuntu unattended-upgrades notification script

Notes:  
- You do NOT need to clone this repo, just download the .py script.
- This is NOT a replacement for unattended-upgrades.

requirements:
1. AWS account
2. ubuntu 18+
3. unattended-upgrades package
4. postfix package
5. uu-notifier.py script (github)
---------------------------

## Instructions
- You must have an AWS account (or, sign up at [AWS](https://aws.amazon.com/account/sign-up))  
You will be using a service known as AWS SES (Simple Email Service)

- To create your SMTP credentials

	1. Sign in to the AWS Management Console and open the Amazon SES console at [https://console.aws.amazon.com/ses/](https://console.aws.amazon.com/ses/).

	2. Choose **Account dashboard** in the left navigation pane.

	3. In the **Simple Mail Transfer Protocol (SMTP) settings** container, choose **Create SMTP Credentials** in the lower-left corner - the IAM console will open.

	4. For **Create User for SMTP**, type a name for your SMTP user in the **IAM User Name field**. Alternatively, you can use the default value that is provided in this field. When you finish, choose **Create** in the bottom-right corner.

	5. Expand **Show User SMTP Security Credentials** - your SMTP credentials are shown on the screen.

	6. Download these credentials by choosing **Download Credentials** or copy them and store them in a safe place, because you can't view or save your credentials after you close this dialog box.

	7. Choose **Close Window**.

	8. Return to the **Account Dashboard** page. This is where you will find the SMTP endpoint and associated ports.

- install unattended-upgrades (if not already installed)  
```sudo apt-get install unattended-upgrades```

- ensure that unattended-upgrades is running properly  
```sudo unattended-upgrades --dry-run```

- restart unattended-upgrades daemon  
```sudo systemctl restart unattended-upgrades```

- install postfix (if not already installed)  
```sudo apt-get install postfix```

- configure postfix by using its config file  
```sudo vi /etc/postfix/main.cf```
- add the following lines to the main.cf file  
```
smtp_sasl_auth_enable = yes  
smtp_sasl_password_maps = hash:/etc/postfix/sasl_passwd  
smtp_sasl_security_options = noanonymous  
smtp_sasl_tls_security_options = noanonymous  
smtp_tls_security_level = encrypt  
header_size_limit = 4096000  
relayhost = [smtp.sendgrid.net]:587
smtp_tls_CAfile = /etc/postfix/cacert.pem
```

- create the /etc/postfix/sasl_passwd file  
```sudo vi /etc/postfix/sasl_passwd```

- add the following line to the sasl_passwd file  
```[email-smtp.us-east-1.amazonaws.com]:465 username:password```  
Note: you will need the SMTP credentials from your AWS account. this is NOT the same as your AWS login identity.

- secure the sasl_passwd file  
```sudo chmod 600 /etc/postfix/sasl_passwd```  
```sudo chmod 600 /etc/postfix/sasl_passwd```

- update postfix's hashtables to use the new file  
```sudo postmap /etc/postfix/sasl_passwd```

- Sign certificate for postfix  
```cat /etc/ssl/certs/Trustwave_Global_Certification_Authority.pem | sudo tee -a /etc/postfix/cacert.pem```

- restart postfix  
```sudo systemctl restart postfix```

- verify that postfix is configured properly by sending a test email  
```echo "Test Email message body" | mail -s "Email test subject" user@localhost```  
Note: if it fails to send a test message, refer to the external links section below

- download a [copy of the script](https://github.com/bradfears/Ubuntu-unattended-upgrades-notification-script/blob/main/uu-notifier.py)
-- this will be the script you run on the server

- configure cron job to run script once per month (unattended-upgrades logs rotate once per month)  
```sudo crontab -e```  
```@monthly /usr/bin/python3 /<location of python script>/uu-notifier.py```

---------------------------
## External links that may be helpful in troubleshooting

[How to configure Postfix to use an External SMTP Server](https://devanswers.co/postfix-external-smtp-server/#:~:text=sudo%20postmap%20%2Fetc%2Fpostfix%2Fsasl_passwd%20There%20should%20now%20be%20a,to%20read%20and%20write%20to%20sasl_passwd%20and%20sasl_passwd.db)

[How can I force unattended-upgrades to run on demand?](https://askubuntu.com/questions/444711/how-can-i-force-unattended-upgrades-to-run-on-demand)
