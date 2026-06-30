import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from config import data_input

import tide_data as tide
import wave_data as wave

REFRESH_INTERVAL = data_input.data_refresh_interval

while True:
    try:
        tide.get_tide_data()
        wave.get_wave_data()
        time.sleep(REFRESH_INTERVAL)
    except KeyboardInterrupt:
        print("Ending script")
        break
    except Exception as error:
        print(f"Error in data refresh: {error}")
        time.sleep(REFRESH_INTERVAL)
