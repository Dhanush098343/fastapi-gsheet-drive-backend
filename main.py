from fastapi import FastAPI, File, UploadFile, Form
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
import pickle

from google_drive import upload_image_to_drive
from google_sheet import append_to_sheet

app = FastAPI()

DRIVE_FOLDER_ID = "1elPfJCyNAO7APwiboqGuOkKVx3U85K_6"
SHEET_ID = '161yriujUrXgFJDYbryAuOlcV2apTBT8lYOiGMs52240'


from google.oauth2.credentials import Credentials
import json

def get_credentials():
    with open("/etc/secrets/token.json", "r") as token_file:
        token_info = json.load(token_file)
    creds = Credentials.from_authorized_user_info(token_info)
    return creds


@app.post("/add_product")
async def add_product(
    price: str = Form(...),
    stock: str = Form(...),
    image: UploadFile = File(...)
):
    creds = get_credentials()

    # Build services
    drive_service = build('drive', 'v3', credentials=creds)
    sheet_service = build('sheets', 'v4', credentials=creds)

    # Upload image and get shareable link
    image_url = upload_image_to_drive(drive_service, image, DRIVE_FOLDER_ID)

    # Write to Google Sheet
    append_to_sheet(sheet_service, SHEET_ID, price, stock, image_url)

    return {"message": "Product uploaded", "image_url": image_url}
