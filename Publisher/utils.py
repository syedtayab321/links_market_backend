from django.core.mail import send_mail


def send_verification_email(email, code):
    subject = "Verify Your Email"
    message = f"Your verification code is: {code}"
    from_email = "no-reply@yourdomain.com"
    send_mail(subject, message, from_email, [email])
