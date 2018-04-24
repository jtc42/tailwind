# tailwind
Subnet monitor for Windows, used on Articuno network

## Requirements
Easy-install using requirements.txt (pip) or environment.yml (conda). Use -win versions if running on Windows
* Flask
### Windows (for system monitoring with OpenHardwareMonitor)
* OpenHardwareMonitor
* pywin32
* wmi
* wfastcgi

## Usage
* Edit `server.json` with your server info, and choice of cards
* Add .txt files to `cards` folder to add static-content cards
* Run `main.py`, or run through a WSGI server
  * **If on IIS:** Within the environment/venv being used, run 'wfastcgi-enable', and use the returned FastCGI script processor under Handler Mappings

## server.json
### cards
* **vpnscan** - Info on clients connected to an OpenVPN server located at the specific `ovpn_path`
* **netscan** - Online/offline status of all hosts listed in the `hosts` parameter
* **vmscan** - Info about Hyper-V VMs hosted on the Tailwind host machine. *Requires your Application Pool user to be part of the Hyper-V Administrators group*
* **sysinfo** (Windows only) - CPU, memory, and GPU load and temperature info, obtained from OpenHardwareMonitor
* **platform** - Basic platform info for the host hardware

### hosts
* List of hosts to appear on the `netscan` card
* Each item much have a `url` and `name` specified (see included example `server.json`)
