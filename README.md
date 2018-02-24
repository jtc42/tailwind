# tailwind
Subnet monitor for Windows, used on Articuno network

## Requirements
* Flask
### Windows (for system monitoring with OpenHardwareMonitor)
* OpenHardwareMonitor
* pywin32
* wmi

## Usage
* Edit `server.json` with your server info, and choice of cards
* Add .txt files to `cards` folder to add static-content cards
* Run `main.py`, or run through a WSGI server

## server.json
### cards
* **vpnscan** - Info on clients connected to an OpenVPN server located at the specific `ovpn_path`
* **netscan** - Online/offline status of all hosts listed in the `hosts` parameter
* **sysinfo** (Windows only) - CPU, memory, and GPU load and temperature info, obtained from OpenHardwareMonitor
* **platform** - Basic platform info for the host hardware

### hosts
* List of hosts to appear on the `netscan` card
* Each item much have a `url` and `name` specified (see included example `server.json`)
