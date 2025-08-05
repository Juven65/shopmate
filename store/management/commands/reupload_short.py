from django.core.management.base import BaseCommand
from store.models import Product
from django.core.files import File
import os

class Command(BaseCommand):
    help = "Re-upload the original short.jpg image to Cloudinary"

    def handle(self, *args, **kwargs):
        # Hanapin yung product na may name na "Short"
        try:
            product = Product.objects.get(name__iexact="Short")
        except Product.DoesNotExist:
            self.stdout.write(self.style.ERROR("❌ Product 'Short' not found"))
            return

        # Path ng original short.jpg sa local static/media
        image_path = os.path.join("media", "products", "short.jpg")  # adjust kung nasa ibang folder

        if not os.path.exists(image_path):
            self.stdout.write(self.style.ERROR(f"❌ Image not found at {image_path}"))
            return

        # Buksan at i-save ulit sa ImageField ng product
        with open(image_path, "rb") as f:
            product.image.save("short.jpg", File(f), save=True)

        self.stdout.write(self.style.SUCCESS("✅ Successfully re-uploaded short.jpg to Cloudinary"))
