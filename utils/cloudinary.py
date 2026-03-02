import cloudinary
import cloudinary.uploader
from fastapi import HTTPException
from dotenv import load_dotenv
import os

load_dotenv()

# ✅ VERY IMPORTANT — configure cloudinary properly
cloudinary.config(
    cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME"),
    api_key=os.getenv("CLOUDINARY_API_KEY"),
    api_secret=os.getenv("CLOUDINARY_API_SECRET"),
)
# print("Cloud name:", os.getenv("CLOUDINARY_CLOUD_NAME"))
def upload_image(file):
    try:
        # 🔥 pass file.file NOT file
        result = cloudinary.uploader.upload(file.file)
        return result.get("secure_url")

    except Exception as e:
        print("CLOUDINARY ERROR:", e)  # print real error in terminal
        raise HTTPException(
            status_code=500,
            detail="Image upload failed"
        )