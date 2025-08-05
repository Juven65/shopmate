import cloudinary
import cloudinary.uploader
import os
from decouple import config

# Load Cloudinary config from .env
cloudinary.config(
    cloud_name=config("CLOUDINARY_CLOUD_NAME"),
    api_key=config("CLOUDINARY_API_KEY"),
    api_secret=config("CLOUDINARY_API_SECRET")
)

print("✅ Cloudinary Config Loaded!")

# Test image file path (siguraduhin may image ka dito)
test_image_path = os.path.join("static", "images", "short.jpg")

if not os.path.exists(test_image_path):
    print(f"❌ Test image not found at: {test_image_path}")
else:
    print("📤 Uploading test image to Cloudinary...")
    result = cloudinary.uploader.upload(test_image_path)
    print("✅ Uploaded successfully!")
    print("🔗 Image URL:", result.get("secure_url"))
