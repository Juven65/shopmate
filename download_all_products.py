import os, django, requests
from urllib.parse import urlparse

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "shopmate.settings")
django.setup()

from store.models import Product

os.makedirs("media/products", exist_ok=True)

for p in Product.objects.all():
    if not p.image:
        print(f"⚠️ No image for {p.name}")
        continue
    url = p.image.url
    fname = os.path.basename(urlparse(url).path)
    path = f"media/products/{fname}"
    r = requests.get(url, stream=True)
    if r.status_code == 200:
        with open(path, "wb") as f:
            for chunk in r.iter_content(1024):
                f.write(chunk)
        print(f"✅ {p.name} saved as {fname}")
    else:
        print(f"❌ Failed for {p.name}")
