import cloudinary
import cloudinary.uploader

def upload_arquivo(file):
    result = cloudinary.uploader.upload(file)
    return result["secure_url"]