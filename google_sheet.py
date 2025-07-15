from googleapiclient.discovery import build

def append_to_sheet(sheet_service, sheet_id, price, stock, image_url):
    sheet_range = "Sheet1!A1"  # Adjust if your sheet/tab name is different
    values = [[image_url, price, stock]]  # Correct order: ImageURL, Price, Stock

    body = {
        "values": values
    }

    result = sheet_service.spreadsheets().values().append(
        spreadsheetId=sheet_id,
        range=sheet_range,
        valueInputOption="USER_ENTERED",
        body=body
    ).execute()

    print(f"{result.get('updates').get('updatedCells')} cells appended.")
