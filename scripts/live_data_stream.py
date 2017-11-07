import tide_data as tide
import wave_data as wave

while True:
    try:
        tide.get_tide_data()
        wave.get_wave_data()
    except KeyboardInterrupt:
        break
    except:
        print("Error in data refresh")