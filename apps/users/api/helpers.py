from django.core.mail import BadHeaderError, send_mail
from rest_framework.response import Response

def notify_user(subject, message, to_email, from_email):
    if subject and message and from_email:
        try:
            send_mail(subject, message, from_email, [to_email])
        except BadHeaderError:
            return Response(
                {
                    "success":False,
                    "err":"Invalid Header Found"
                }
            )
        
    else:
        return Response(
            {
                "success":False,
                "err":'Make sure all fields are entered and valid.'
            }
        )