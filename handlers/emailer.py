#!/usr/bin/python2.7
import sys, json, os, smtplib

json_args = json.loads(sys.argv[1])
hostname = json_args["hostname"]
ip = json_args["ip"]
time = json_args["time"]
port = json_args["port"]
try:
    mail_from = os.environ["MAIL_FROM"]
    smtp_server = os.environ["SMTP_SERVER"]
    smtp_port = os.environ.get("SMTP_PORT", 25)
    smtp_user = os.environ.get("SMTP_USER")
    smtp_pass = os.environ.get("SMTP_PASS")
    smtp_tls = os.environ.get("SMTP_TLS", "False").lower()
    mail_to = os.environ["MAIL_TO"].split(",")
except:
    print "unable to send mail - missing one of the envvars of the emailer.py handler"
    exit(2)

try:
    smtpObj = smtplib.SMTP(host=smtp_server,port=smtp_port)
    try:
        if smtp_tls == "true":
            smtpObj.starttls()
    except:
        pass
    if smtp_user and smtp_pass:
        smtpObj.login(smtp_user, smtp_pass)
    for mail_address in mail_to:
        data = "there have an attempet to access " + hostname + ":" + str(port) + " at " + time + " from ip address " + ip
        message = """\
From: %s
To: %s
Subject: %s

%s\
        """ % (mail_from, mail_address,"DSHP alert: " + hostname + " access attempt detected", data)
        smtpObj.sendmail(mail_from, mail_to, message)
        smtpObj.quit()
except:
    print "unable to send mail - something went wrong"
