from flask import render_template
from flask_mail import Message
from app import mail
from app.decorators import *
from app.config import *
from app import app

@async
def async_send(msg):
    with app.app_context():
        mail.send(msg)


def send_email(subject, sender, recipients, text_body, html_body):
    msg = Message(subject, sender = sender, recipients = recipients)
    msg.body = text_body
    msg.html = html_body
    async_send(msg)


def send_my_email():
    send_email("test", "aqueti.tester@gmail.com", RLIST, "text", "html")