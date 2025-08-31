
#


import os
from django.core.management.base import BaseCommand
from django.conf import settings
from django.core.files import File
from matcher.models import Product
from matcher.similarity import extract_features
from PIL import Image as PILImage

class Command(BaseCommand):
    help = "Populate the database with products from images in media/uploads/."

    def handle(self, *args, **kwargs):
        uploads_dir = os.path.join(settings.MEDIA_ROOT, "uploads")

        if not os.path.exists(uploads_dir):
            self.stdout.write(self.style.ERROR(f"Folder not found: {uploads_dir}"))
            return

        # Clear old products
        Product.objects.all().delete()
        self.stdout.write("Deleted old products.")

        for filename in os.listdir(uploads_dir):
            file_path = os.path.join(uploads_dir, filename)

            if not filename.lower().endswith((".jpg", ".jpeg", ".png")):
                continue

            try:
                pil_image = PILImage.open(file_path).convert("RGB")
                features = extract_features(pil_image)

                product = Product(
                    name=os.path.splitext(filename)[0],
                    category="General",
                )

                with open(file_path, "rb") as f:
                    product.image.save(filename, File(f), save=False)

                if features is not None:
                    product.feature_vector = features.tobytes()

                product.save()
                self.stdout.write(self.style.SUCCESS(f"Added {filename}"))

            except Exception as e:
                self.stdout.write(self.style.ERROR(f"Error processing {filename}: {e}"))


        self.stdout.write(self.style.SUCCESS("Finished populating products."))
