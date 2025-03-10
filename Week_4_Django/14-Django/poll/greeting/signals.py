from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Poll
import logging

logger = logging.getLogger("poll_creation")


@receiver(post_save, sender=Poll)
def log_poll_creation(sender, instance, created, **kwargs):
    if created:
        logger.info(f"New poll created: {instance.question_text}")
