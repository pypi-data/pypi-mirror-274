import os.path

from google.auth.external_account_authorized_user import (
    Credentials as ExternalAccountCredentials,
)
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
]

CONFIG_DIR = os.path.expanduser("~/.config/pandas-gsheets")


def setup(
    config_dir: str = CONFIG_DIR,
    credentials_file: str = os.path.join(CONFIG_DIR, "credentials.json"),
    scopes: list[str] = SCOPES,
) -> Credentials | ExternalAccountCredentials:
    os.makedirs(config_dir, exist_ok=True)

    token_file = os.path.join(CONFIG_DIR, "token.json")

    credentials = None
    if os.path.exists(token_file):
        credentials = Credentials.from_authorized_user_file(token_file, SCOPES)

    if not credentials or not credentials.valid:
        if credentials and credentials.expired and credentials.refresh_token:
            credentials.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(credentials_file, SCOPES)
            credentials = flow.run_local_server(port=0)

        with open(token_file, mode="w") as token:
            token.write(credentials.to_json())

    return credentials
