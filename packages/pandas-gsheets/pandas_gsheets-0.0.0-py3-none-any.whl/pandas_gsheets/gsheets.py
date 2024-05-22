from googleapiclient.discovery import Resource, build

from pandas_gsheets.setup import CONFIG_DIR, setup


class GoogleSheets:
    def __init__(self, config_dir: str = CONFIG_DIR) -> None:
        self.credentials = setup(config_dir)

    def sheets(self) -> Resource:
        return build("sheets", "v4", credentials=self.credentials)

    def create_spreadsheet(self, title: str) -> str:
        service = self.sheets()
        spreadsheet = (
            service.spreadsheets()  # type: ignore
            .create(
                body={
                    "properties": {
                        "title": title,
                    },
                },
            )
            .execute()
        )

        return spreadsheet["spreadsheetId"]
