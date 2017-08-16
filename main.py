from tools import netscan, sysinfo
from flask import Flask, render_template, request, jsonify

print("Setting up internal server...")
app = Flask(__name__)
app.config['DEBUG'] = True
        
@app.route('/')
def index():
    
    visitor_ip = str(request.remote_addr) # Get visitor IP

    name = "{}".format(visitor_ip)
    
    return render_template("index.html",
                           title='Home',
                           name=name,
                           hosts=netscan.devices)

@app.route('/devlist')
def devlist():
    netscan.update()
    return render_template("dev_table.html",
                           hosts=netscan.devices)

@app.route('/status')
def status():
    print("Getting status data")
    j = sysinfo.get_all(sysinfo.sensors)
    print("Returning status data")
    return jsonify(j)

# Run web app
if __name__=='__main__':
    app.run(host='0.0.0.0', threaded=True)