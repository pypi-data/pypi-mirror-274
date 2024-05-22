from pandas_gsheets import GoogleSheets, setup

setup()

gs = GoogleSheets()
gs.create_spreadsheet("test")
