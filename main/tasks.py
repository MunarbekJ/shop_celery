from datetime import date, timedelta
from django.core.mail import send_mail
from celery import shared_task
from .models import Product
from django.contrib.auth import get_user_model

User = get_user_model()

@shared_task
def send_new_products():
    day = date.today() - timedelta(days=1)
    products = Product.objects.filter(created_at_gte=day)
    message = "Новые продукты за день"
    for product in products:
        message += f"\n{product.title}  ${product.price}"

    send_mail(
        subject="Новинки",
        message=message,
        from_email="a@mail.com",
        recipient_list=[u.email for u in User.objects.all()]
    )


def send_spam(new_product):
    users_email = [x.email for x in User.objects.all()]
    message = f"""
У нас появился новый продукт

{new_product.title}

{new_product.description}
"""
    send_mail(
        subject="Новинка",
        message=message,
        from_email="a@gmail.com",
        recipient_list=users_email
    )
