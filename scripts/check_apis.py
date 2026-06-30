#!/usr/bin/env python3
"""Verify Driftwood external data sources."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from config import data_input
import tide_data
import wave_data


def main():
    errors = []

    print(f"Checking tide station: {data_input.TIDE_STATION_NAME}")
    try:
        tide_data.get_tide_data()
        print("  tide: OK")
    except Exception as error:
        errors.append(f"tide: {error}")
        print(f"  tide: FAIL ({error})")

    print(f"Checking wave dataset: {data_input.WAVE_DATASET_NAME}")
    try:
        wave_data.get_wave_data()
        print("  wave: OK")
    except Exception as error:
        errors.append(f"wave: {error}")
        print(f"  wave: FAIL ({error})")

    if errors:
        print("\nAPI check failed.")
        return 1

    print("\nAPI check passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
