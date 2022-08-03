from django.core.mail import EmailMessage, send_mail
from django.template.loader import render_to_string
# from django.utils.html import strip_tags


def invite_mail(
    to, login_url, from_email, subject="Invitation to join workspace"
):
    # import pdb; pdb.set_trace()
    mail_template = 'mail.html'
    context = {
        "login_url": login_url
    }
    html_message = render_to_string(mail_template, context)
    # plain_message = strip_tags(html_message)

    mail = EmailMessage(
        subject=subject,
        body=html_message,
        to=[to],
        from_email="sahil.alam@ekank.com",
    )
    mail.content_subtype = "html"
    mail.send()