from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.files.storage import default_storage
from PIL import Image
from .models import Menu
import os


@receiver(post_save, sender=Menu)
def resize_menu_item_image(sender, instance, created, **kwargs):
    """Resize image after saving a Menu object."""
    if created:
        image = instance.item_image

        if image:
            try:
                img = Image.open(image)
                img.thumbnail((600, 600))
                img.save(image.path)
                print(f"Image for {instance.item_name} resized successfully.")

            except Exception as e:
                print(f"Error resizing image for {instance.item_name}: {e}")


@receiver(post_delete, sender=Menu)
def delete_item_image(sender, instance, **kwargs):
    """Delete the image file when the Menu instance is deleted."""
    image = instance.item_image
    if image:
        try:
            if os.path.isfile(image.path):
                os.remove(image.path)
                print(f"Image {image.name} deleted successfully.")
        except Exception as e:
            print(f"Error deleting image {image.name}: {e}")
