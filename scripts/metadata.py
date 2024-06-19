from PIL import Image
from PIL.ExifTags import TAGS

def extract_metadata(image_path):
    image = Image.open(image_path)
    exif_data = image._getexif()
    if exif_data:
        metadata = {TAGS.get(tag): value for tag, value in exif_data.items()}
    else:
        metadata = {}
    return metadata

image_path = "/home/koala/freelance projects/Rekognition project (UpWork)/sample_images/image7.jpg"
metadata = extract_metadata(image_path)
print(metadata)
