from flask import Flask, render_template, jsonify, Markup
import random
import glob
import os
import platform
import json

# SET UP APP
print("Setting up internal server...")
app = Flask(__name__)
app.config['DEBUG'] = True


# SET UP BASIC FUNCTIONS
def get_static_cards(path_mask):
    # Load static cards
    files = glob.glob(path_mask) #Find all data files
    names = [os.path.basename(f)[:-4] for f in files]
    cdata = [open(file).read() for file in files]
    cards = {}
    
    for c in zip(names, cdata):
        # Read text file data as markup. Be fucking sure it's safe!
        cards[c[0]] = Markup(c[1])
        
    return cards


# SELECT CARDS
STATIC_CARDS = get_static_cards("cards/*.txt")  

# GET SERVER INFO FROM JSON
SERVER_INFO = json.load(open('server.json'))

# GET PLATFORM DATA
PLATFORM_DATA = {
        'node': {'name': 'Node', 'val': platform.node()},
        'os': {'name': 'Operating System', 'val': platform.platform()},
        'arch': {'name': 'Architecture', 'val': platform.machine()},
        'pyver': {'name': 'Python Version', 'val': platform.python_version()}
        }
  
# CREATE ROUTES
@app.route('/')
def index():
    global CARDS
    global STATIC_CARDS
    global PLATFORM_DATA
    
    return render_template("index.html",
                           title=SERVER_INFO['title'],
                           colour=SERVER_INFO['colour'],
                           emblem=SERVER_INFO['emblem'],
                           favicon=SERVER_INFO['favicon'],
                           msg=SERVER_INFO['message'],
                           platform=PLATFORM_DATA,
                           static_cards=STATIC_CARDS,
                           cards=SERVER_INFO['cards']
                           )


if 'netscan' in SERVER_INFO['cards']:
    from tools import netscan
    hosts = SERVER_INFO['hosts']
    hosts = netscan.online_dict(hosts)
    @app.route('/devs')
    def devs():
        global hosts
        return render_template("dev_table.html",
                               hosts=hosts
                               )


if 'vmscan' in SERVER_INFO['cards']:
    from tools import vmscan
    @app.route('/vmdevs')
    def vmdevs():
        hosts = vmscan.vm_dict()
        return render_template("vm_table.html",
                               hosts=hosts
                               )


if 'vpnscan' in SERVER_INFO['cards']:
    from tools import vpnscan
    vpn_sniffer_win = vpnscan.VpnSniffer(SERVER_INFO['ovpn_path'])
    @app.route('/vpndevs')
    def vpndevs():
        vpn_sniffer_win.update()
        return render_template("vpn_table.html",
                               hosts=vpn_sniffer_win.devices
                               )


if 'sysinfo' in SERVER_INFO['cards']:
    from tools import sysinfo
    @app.route('/status')
    def status():
        sensors = ['CPU Total/Load', 
                   'CPU Package/Temperature', 
                   'GPU Core/Load', 
                   'GPU Core/Temperature', 
                   'Memory/Load', 
                   'GPU Memory/Load',
                   ]
        j = sysinfo.get_all(sensors)
        return jsonify(j)


# Run web app
if __name__=='__main__':
    app.run(host='0.0.0.0')
