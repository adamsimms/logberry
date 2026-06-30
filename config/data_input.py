# Install-specific motor and wave parameters (values are in motor steps unless noted).

lowest_tide = 50
tide_range = 200
multiplier = 6
speed_multiplier = 2.5

# Seconds between successful tide/wave data refreshes in live_data_stream.py
data_refresh_interval = 300

# SmartAtlantic API request identity (override via environment variables on the Pi)
import os

SMARTATLANTIC_USER = os.environ.get("DRIFTWOOD_WAVE_USER", "Driftwood")
SMARTATLANTIC_EMAIL = os.environ.get("DRIFTWOOD_WAVE_EMAIL", "driftwood@example.com")
