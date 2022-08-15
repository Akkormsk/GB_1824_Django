import logging
from celery import shared_task
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.mail import send_mail

logger = logging.getLogger(__name__)


@shared_task
def send_feedback_mail(message: str) -> None:
    logger.info(f"Send message: '{message}'")
    # user_model = get_user_model()
    # user_obj = user_model.objects.get(pk=user_id)
    send_mail(
        'TechSupport Help',
        message,
        'test@mail.ru',
        ['techsupport@braniac.com'],
        fail_silently=False,
    )
    return None
