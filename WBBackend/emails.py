from decouple import config
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

def send_mail(sender,receiver,subject,html):
    message = Mail(
        from_email=sender,
        to_emails=receiver,
        subject=subject,
        html_content=html
    try:
        sg = SendGridAPIClient(config('SENDGRID_API_KEY'))
        response = sg.send(message)
    except Exception as e:
        print(e.message)
