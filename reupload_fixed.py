import os
import django
import cloudinary
import cloudinary.uploader

# ===== DJANGO SETTINGS =====
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'shopmate.settings')
django.setup()

from store.models import Product

# ===== CLOUDINARY CONFIG =====
cloudinary.config(
    cloud_name="dtoqcatxx",  # palitan kung iba
    api_key="837814249615385",
    api_secret="MhE1R5RoQQqOUOmbndjcKo_s59Q"
)

# ===== LOCAL FOLDER =====
product_images_dir = "media/products"

# Mapping ng Product Name → Local file name
mapping = {
    "T-shirt": "t-shirt.jpg",
    "Shoes": "shoes.jpg",
    "Slipper": "Slipper.jpg",
    "Jacket": "Jacket.webp",
    "Pants": "Pants.jpg",
    "T-shirts": "White-T-shirts.jpg",
    "Bag": "bag.webp",
    "Short": "short.jpg"
}

print("✅ Cloudinary config loaded.")

# Loop sa lahat ng products
for product in Product.objects.all():
    filename = mapping.get(product.name)
    if not filename:
        print(f"❌ No mapping for {product.name}")
        continue

    local_image_path = os.path.join(product_images_dir, filename)

    if not os.path.exists(local_image_path):
        print(f"❌ Image not found for {product.name}: {local_image_path}")
        continue

    print(f"📤 Uploading {filename} to Cloudinary...")
    upload_result = cloudinary.uploader.upload(
        local_image_path,
        folder="products"
    )

    product.image = upload_result["secure_url"]
    product.save()
    print(f"✅ Updated {product.name} with new image URL.")

print("🎉 All done!")
