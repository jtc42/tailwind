from tools import netscan, sysinfo
from flask import Flask, render_template, request, jsonify, Markup
import random
import glob
import os

print("Setting up internal server...")
app = Flask(__name__)
app.config['DEBUG'] = True

# Load static cards
files = glob.glob("cards/*.txt") #Find all data files
names = [os.path.basename(f)[:-4] for f in files]
cdata = [open(file).read() for file in files]
cards = {}
for c in zip(names, cdata):
    # Read text file data as markup. Be fucking sure it's safe!
    cards[c[0]] = Markup(c[1])

# Set up routes

@app.route('/')
def index():

    # Get server message from file
    try:
        with open("svrmsg.txt") as f:
            msgs = f.readlines()
            svrmsg = random.choice(msgs)
    except:
        svrmsg = ""
    
    # Get visitor IP
    visitor_ip = str(request.remote_addr) # Get visitor IP

    # Create visitor name
    name = "{}".format(visitor_ip)
    
    return render_template("index.html",
                           title='Home',
                           name=name,
                           msg = svrmsg,
                           cards = cards,
                           hosts=netscan.devices)

                           
@app.route('/devlist')
def devlist():
    netscan.update()
    return render_template("dev_table.html",
                           hosts=netscan.devices)

                           
@app.route('/devraw')
def devraw():
    netscan.update()
    j = netscan.devices
    print("Returning status data")
    return jsonify(j)
         
         
@app.route('/status')
def status():
    print("Getting status data")
    j = sysinfo.get_all(sysinfo.sensors)
    print("Returning status data")
    return jsonify(j)

    
# Run web app
if __name__=='__main__':
    app.run(host='0.0.0.0', threaded=True)