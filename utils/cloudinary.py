import cloudinary
import cloudinary.uploader
# import cloudinary.api
from fastapi import HTTPException
from dotenv import load_dotenv
import os


# -------------------------
# Configure Cloudinary
# -------------------------

load_dotenv()

class Config:
    CLOUDINARY_CLOUD_NAME = os.getenv("CLOUDINARY_CLOUD_NAME")
    CLOUDINARY_API_KEY = os.getenv("CLOUDINARY_API_KEY")
    CLOUDINARY_API_SECRET = os.getenv("CLOUDINARY_API_SECRET")

# -------------------------
# Upload Image Function
# -------------------------
def upload_image(file):
    try:
        result = cloudinary.uploader.upload(file)
        return result.get("secure_url")
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail="Image upload failed"
        )