import sys
from datetime import datetime, timedelta
from pathlib import Path
from urllib.parse import quote

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from config import data_input
from paths import WAVE_STATUS_CSV


def get_wave_data():
    now = datetime.now()
    start_date = now - timedelta(days=1)
    end_date = now

    user = quote(data_input.SMARTATLANTIC_USER)
    email = quote(data_input.SMARTATLANTIC_EMAIL)
    url = (
        "http://www.smartatlantic.ca/Home/doNewRequest.php"
        "?sel=timestamp%2Clat%2Clon%2Cwave_ht_max%2Cwave_ht_sig%2Cwave_period_max%2C"
        f"&db=smb_mouth_of_placentia&title=Mouth%20of%20Placentia%20Bay"
        f"&user={user}&email={email}"
        f"&start={start_date.strftime('%Y-%m-%d')}&end={end_date.strftime('%Y-%m-%d')}"
    )

    wave_data = pd.read_csv(url)
    wave_data["Date & Time(UTC)"] = pd.to_datetime(wave_data["Date & Time(UTC)"])
    wave_data.columns = [
        "date_time",
        "latitude",
        "longitude",
        "max_wave_height",
        "sig_wave_height",
        "peak_wave_period",
    ]
    WAVE_STATUS_CSV.parent.mkdir(parents=True, exist_ok=True)
    wave_data.tail(1).to_csv(WAVE_STATUS_CSV, index=False)
