import os
import django
from decouple import config
import cloudinary
import cloudinary.uploader

# Setup Django environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "shopmate.settings")
django.setup()

from store.models import Product

# Cloudinary config
cloudinary.config(
    cloud_name=config("CLOUDINARY_CLOUD_NAME"),
    api_key=config("CLOUDINARY_API_KEY"),
    api_secret=config("CLOUDINARY_API_SECRET")
)

print("✅ Cloudinary config loaded.")

# Path to local image
file_path = "static/images/short.jpg"
if not os.path.exists(file_path):
    print(f"❌ File not found: {file_path}")
    exit()

print(f"📤 Uploading {file_path} to Cloudinary...")

# Upload to Cloudinary
result = cloudinary.uploader.upload(file_path, public_id="products/short")
image_url = result["secure_url"]

print("✅ Uploaded successfully!")
print("🔗 URL:", image_url)

# Update product in DB
try:
    product = Product.objects.get(name__iexact="Short")
    product.image = image_url
    product.save()
    print(f"✅ Updated product 'Short' with new image URL.")
except Product.DoesNotExist:
    print("❌ No product found with name 'Short'. Please check your database.")
