import requests
from cloudinary import uploader as cloudinary_uploader


def format_datetime(value):
    return value.strftime("%Y-%m-%d %H:%M:%S")


def upload_image(image_url, folder_name):
    try:
        response = requests.get(image_url, stream=True)
        response.raw.decode_content = True
        upload_result = cloudinary_uploader.upload(
            response.raw, resource_type="image", folder=folder_name
        )
        return upload_result["secure_url"]
    except Exception as e:
        print(e)
        return None
