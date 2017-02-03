import smtplib
from os.path import basename
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import COMMASPACE, formatdate

def sendAlert():
    fromaddr = 'alertmail760@gmail.com '
    toaddrs  = 'dougfrieders@gmail.com'
    msg = 'Why,Oh why!'
    username = 'alertmail760@gmail.com'
    password = 'cubbieismydog88'
    server = smtplib.SMTP('smtp.gmail.com:587')
    server.ehlo()
    server.starttls()
    server.login(username,password)
    server.sendmail(fromaddr, toaddrs, msg)
    server.quit()

def sendMail(send_from, send_to, subject, text, files=None,
              server="smtp.gmail.com:587"):
    assert isinstance(send_to, list)

    msg = MIMEMultipart()
    msg['From'] = send_from
    msg['To'] = COMMASPACE.join(send_to)
    msg['Date'] = formatdate(localtime=True)
    msg['Subject'] = subject

    msg.attach(MIMEText(text))

    for f in files or []:
        with open(f, "rb") as fil:
            part = MIMEApplication(
                fil.read(),
                Name=basename(f)
            )
            part['Content-Disposition'] = 'attachment; filename="%s"' % basename(f)
            msg.attach(part)

    smtp = smtplib.SMTP(server)
    smtp.ehlo()
    smtp.starttls()
    username = 'alertmail760@gmail.com'
    password = 'cubbieismydog88'
    smtp.login(username, password)
    smtp.sendmail(send_from, send_to, msg.as_string())
    smtp.quit()