from google_auth_oauthlib.flow import InstalledAppFlow

SCOPES = ['https://www.googleapis.com/auth/drive.file', 'https://www.googleapis.com/auth/spreadsheets']

def main():
    flow = InstalledAppFlow.from_client_secrets_file("client_secrets.json", SCOPES)
    creds = flow.run_local_server(port=0)
    
    # Save token as JSON
    with open("token.json", "w") as token:
        token.write(creds.to_json())

if __name__ == "__main__":
    main()
