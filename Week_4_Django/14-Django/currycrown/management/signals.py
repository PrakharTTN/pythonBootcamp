from django.db.models.signals import pre_delete, pre_save, post_delete, post_save
from django.dispatch import receiver
from .models import Menu


@receiver(pre_save, sender=Menu)
def pre_save_menu(sender, instance, **kwargs):
    print(f"Pre-save triggered for: {instance.title}")


@receiver(post_save, sender=Menu)
def post_save_menu(sender, instance, **kwargs):
    print(f"Post-save triggered for {instance.title}")
