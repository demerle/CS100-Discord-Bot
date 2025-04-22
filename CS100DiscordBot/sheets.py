import gspread
import pandas as pd

def update_csv(some_data: dict) -> None:
    df = pd.DataFrame(some_data)
    df.to_csv("data.csv", index=False)

def upload_csv_to_google_sheets() -> None:
    df = pd.read_csv("data.csv")

    gc = gspread.service_account("moonlit-nature-449922-r0-fa29a54e433c.json")  # Google Cloud API generated key
    sheet = gc.open_by_key("1cijX9eOzK0faRYYlJRa2rWxtku__anecsHGpqIp01QI")
    worksheet = sheet.worksheet("Sheet1")

    if worksheet.col_count < len(df.columns): #If the new file has less columns than the old one, then there is data loss, so don't do anything
        print("Failed to update due to potential data loss")
        return

    worksheet.clear()
    worksheet.update([df.columns.values.tolist()] + df.values.tolist()) #formatting to 2d list
    print("Updated Google Sheet successfully")
