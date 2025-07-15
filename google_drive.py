from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseUpload
import io

def upload_image_to_drive(drive_service, image, folder_id):
    file_metadata = {
        'name': image.filename,
        'parents': [folder_id]
    }
    media = MediaIoBaseUpload(io.BytesIO(image.file.read()), mimetype=image.content_type)
    file = drive_service.files().create(body=file_metadata, media_body=media, fields='id').execute()
    file_id = file.get('id')

    drive_service.permissions().create(
        fileId=file_id,
        body={"role": "reader", "type": "anyone"}
    ).execute()

    return f"https://drive.google.com/uc?id={file_id}"
