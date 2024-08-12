import hashlib
from django.core.mail import send_mail
from api_yamdb.settings import DEFAULT_FROM_EMAIL


def encode_confirmation_code(username, email):
    my_str = str(username) + str(email)
    return hashlib.sha256(my_str.encode()).hexdigest()


def send_email(email, code):
    send_mail(
        subject='Подтверждение регистрации',
        message=f'Код подтверждения:{code}',
        recipient_list=[email],
        from_email=DEFAULT_FROM_EMAIL,
        fail_silently=True,
    )
