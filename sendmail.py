import email
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

sender = 'eng18cs0132.keerthikumar@gmail.com'
password = 'viratkeerthi'
receiver = 'keerthikumar1835@gmail.com'


try:
    def send_mail():
        print('Sending E-Mail')
        filename = "static/Risk.mp4"
        msg = MIMEMultipart()
        msg['From'] = sender
        msg['To'] = receiver
        msg['Subject'] = 'Public Risk detection'
    
        body = 'the generated detection video is Attached.'
        msg.attach(MIMEText(body, 'plain'))
        attachment = open(filename, 'rb')
        part = MIMEBase('application', 'octet-stream')
        part.set_payload((attachment).read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', 'attachment; filename= %s' % filename)
        msg.attach(part)
        server = smtplib.SMTP('smtp.gmail.com', 465)
        server.starttls()
        server.login(sender, password)
        text = msg.as_string()
        server.sendmail(sender, receiver, text)
        server.quit()
except:
    print("mail not sent")