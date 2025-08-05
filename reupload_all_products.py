import os
from dotenv import load_dotenv

# 1️⃣ Load environment variables mula sa .env
load_dotenv()

# 2️⃣ Ituro muna kung aling settings.py ang gagamitin
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "shopmate.settings")

# 3️⃣ Ngayon saka mag-import ng Django at models
import django
django.setup()

from store.models import Product
import cloudinary
import cloudinary.uploader

# 4️⃣ Configure Cloudinary manually
cloudinary.config(
    cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME"),
    api_key=os.getenv("CLOUDINARY_API_KEY"),
    api_secret=os.getenv("CLOUDINARY_API_SECRET"),
    secure=True
)

print("✅ Cloudinary config loaded.")

# 5️⃣ Path sa local product images
product_images_dir = "media/products"

# 6️⃣ Loop sa lahat ng products
for product in Product.objects.all():
    local_image_path = os.path.join(product_images_dir, os.path.basename(product.image.name))

    if not os.path.exists(local_image_path):
        print(f"❌ Image not found for {product.name}: {local_image_path}")
        continue

    print(f"📤 Uploading {os.path.basename(local_image_path)} to Cloudinary...")
    upload_result = cloudinary.uploader.upload(
        local_image_path,
        folder="products"
    )

    product.image = upload_result["secure_url"]
    product.save()
    print(f"✅ Updated product '{product.name}' with new image URL.")
