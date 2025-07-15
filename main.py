from fastapi import FastAPI, UploadFile, Form
from fastapi.responses import JSONResponse
from google_drive import upload_to_drive
from google_sheet import write_to_sheet
import os

app = FastAPI()

# Environment-safe paths for OAuth credentials
TOKEN_PATH = "/etc/secrets/token.json"
CREDS_PATH = "/etc/secrets/credentials.json"
CLIENT_SECRET_PATH = "/etc/secrets/client_secrets.json"


@app.post("/add_product")
async def add_product(price: str = Form(...), stock: str = Form(...), image: UploadFile = Form(...)):
    try:
        # Save uploaded image locally
        contents = await image.read()
        local_filename = f"temp_{image.filename}"
        with open(local_filename, "wb") as f:
            f.write(contents)

        # Upload image to Google Drive
        drive_url = upload_to_drive(local_filename, CREDS_PATH, TOKEN_PATH)

        # Write data to Google Sheet
        write_to_sheet(price, stock, drive_url, CREDS_PATH, TOKEN_PATH)

        os.remove(local_filename)
        return JSONResponse(status_code=200, content={"message": "Product added successfully", "image_url": drive_url})

    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})
