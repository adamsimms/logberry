from bs4 import BeautifulSoup as bs
import datetime
import requests
import pandas as pd

from paths import TIDE_DATA_CSV


def get_tide_data():
    today = datetime.datetime.now()
    url = (
        "https://www.tides.gc.ca/eng/station"
        f"?type=1&date={today.year}%2F{today.month}%2F{today.day}"
        "&sid=990&tz=NDT&pres=1"
    )
    response = requests.get(url, timeout=30)
    response.raise_for_status()

    soup = bs(response.text, "html.parser")
    tide_rows = []

    for row in soup.find_all("tr"):
        entry_data = [cell.text for cell in row.find_all("td")]
        if len(entry_data) == 3:
            tide_rows.append(entry_data)

    tide_df = pd.DataFrame(tide_rows, columns=["Date", "Time", "Height"])
    tide_df[["Date", "Time"]] = tide_df[["Date", "Time"]].astype(str)
    tide_df["date_time"] = tide_df["Date"] + " " + tide_df["Time"] + ":00"
    tide_df["date_time"] = pd.to_datetime(tide_df["date_time"])
    tide_df["Height"] = pd.to_numeric(tide_df["Height"], errors="coerce")

    final_data = tide_df[["date_time", "Height"]]
    TIDE_DATA_CSV.parent.mkdir(parents=True, exist_ok=True)
    final_data.to_csv(TIDE_DATA_CSV, index=False)
