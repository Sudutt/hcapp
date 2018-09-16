from email.mime.text import MIMEText
import smtplib

def send_email(email, height, average_height,count):
    from_email="########################"
    from_password="##########"
    to_email=email

    subject="Height data results"
    message="Hi there!<br>Your height has been recorded as <strong>%s cm</strong>.<br>Average height found by our study is <strong>%s cm</strong>, calculated from <strong>%s</strong> people.<br><br>Thanks!<br>Sudutt Harne" %(height, average_height, count)

    msg=MIMEText(message,'html')
    msg["Subject"]=subject
    msg["To"]=to_email
    msg["From"]=from_email

    gmail=smtplib.SMTP("smtp.gmail.com",587)
    gmail.ehlo()
    gmail.starttls()
    gmail.login(from_email,from_password)
    gmail.send_message(msg)
    #print("Mail sent!")
