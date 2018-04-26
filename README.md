# Driftwood


# Commands

Start live tide and wave data: 

- `cd ~/logberry/scripts && python3 live_data_stream.py`

Start motors:

- `cd ~/logberry/scripts && python3 project_log_live.py`

Configure log position manually in CM (-10,15):

- `cd ~/logberry/scripts && python3 play_test.py`

# Auto-start on Raspberry Pi Boot
Add the following lines to `sudo nano /etc/rc.local` before `exit 0`
- `(sleep 60
python3 /home/pi/logberry/scripts/live_data_stream.py) &`
- `(sleep 120
python3 /home/pi/logberry/scripts/project_log_live.py) &`

# Reboot Raspberry Pi Remotely
_The log will reset position and restart in approximately 3 minutes._

1. Go to [www.dataplicity.com](http://www.dataplicity.com) 
    - Username: `hello@adamsim.ms`
    - Password: `driftwood`
2. Tap **logberry @concordia**
3. Type `su pi`
4. Password: `10g63rry`
5. Type `sudo reboot` 

# Hardware

- [Raspberry Pi 3 Model B:](https://www.raspberrypi.org/products/raspberry-pi-3-model-b/)
- [Raspberry Pi Power Supply 5V 3A](https://www.robotshop.com/ca/en/raspberry-pi-power-supply-5v-3a-micro-usb.html) *Optional*
- [SlushEngine](https://roboteurs.com/products/slushengine)
- [Nema 23 Stepper Motor](https://www.amazon.ca/Stepper-Motor-Bipolar-340oz-Router/dp/B074X52ZR2/ref=sr_1_1?s=industrial&ie=UTF8&qid=1521390147&sr=8-1&keywords=340oz.in+1.8A+4.95V) Bipolar 340oz.in 1.8A 4.95V 4 Wires CNC Router [[Alternative Source]](https://www.omc-stepperonline.com/hybrid-stepper-motor/nema-23-bipolar-18deg-24nm-340ozin-18a-495v-57x57x104mm-4-wires-23hs41-1804s.html)
- [2.1mm Barrel Jack to terminal](https://www.robotshop.com/ca/en/barrel-jack-terminal-fit0151.html)
- [8mm Aluminum Key Hub w/ Set Screw](https://www.robotshop.com/ca/en/8mm-aluminum-key-hub-set-screw.html)
- [12VDC 3A Wall Adapter Power Supply](https://www.robotshop.com/ca/en/12vdc-3a-wall-adapter-power-supply.html)


