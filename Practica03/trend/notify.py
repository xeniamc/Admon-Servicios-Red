import smtplib
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart

COMMASPACE = ', '
# Define params
rrdpath = 'RRD/'
imgpath = 'img/'


mailsender = "dummycuenta3@gmail.com"
mailreceip = "xeniaamc23@gmail.com"
mailserver = 'smtp.gmail.com: 587'
password = 'dvduuffmlhspbmjj' #contraseña de aplicacion

def send_alert_attached(subject, hostname, datasource):

    """ Envía un correo electrónico adjuntando la imagen en img
    """

    msg = MIMEMultipart()
    msg['Subject'] = subject
    msg['From'] = mailsender
    msg['To'] = mailreceip
    fp = open(f'{imgpath}deteccion-{datasource}.png', 'rb')
    img = MIMEImage(fp.read())
    fp.close()
    body = f'El agente {hostname} {subject}, revisar su rendimiento.'
    body = MIMEText(body)
    msg.attach(body)
    msg.attach(img)
    s = smtplib.SMTP(mailserver)

    s.starttls()
    # Login Credentials for sending the mail
    s.login(mailsender, password)

    s.sendmail(mailsender, mailreceip, msg.as_string())
    s.quit()