import tools
from flask import Flask, render_template, request, redirect, url_for

print("Running initial extended scan...")
tools.netscan.refresh_full()

internal_ips = ["::1", "0.0.0.0", "127.0.0.1"]

print("Setting up internal server...")
app = Flask(__name__)
app.config['DEBUG'] = True
        
@app.route('/')
def index():
    
    visitor_ip = str(request.remote_addr) # Get visitor IP
    flag = None
    
    # If visitor IP is already recognised on the subnet
    if visitor_ip in tools.netscan.online_hosts: 
        print("Visitor already recognised") # Do nothing
        
    # If IP is not recognised, but is on the VPN subnet
    elif (tools.netscan.ipaddress.ip_address(visitor_ip) in tools.netscan.all_hosts): 
        flag = "FORCED"
        
    else: # If not known AND not on the VPN
        if visitor_ip in internal_ips: # Exclude IIS servers internal IP
            flag = None
        else:
            flag = "EXTERNAL"
   
    visitor_hostname = tools.netscan.get_hostname(visitor_ip)
    
    if flag: # If host should be added to the table
        tools.netscan.insert_host(visitor_ip, flag + ':' + visitor_hostname, True, tools.netscan.online_hosts)

    name = "{} / {}".format(visitor_ip, visitor_hostname)
    
    return render_template("index.html",
                           title='Home',
                           name=name,
                           hosts=tools.netscan.online_hosts)

@app.route('/devlist')
def devlist():
    tools.netscan.refresh_active()
    return render_template("dev_table.html",
                           hosts=tools.netscan.online_hosts)

@app.route('/reload')
def reload():
    if tools.netscan.is_scanning == True:
        print("Full scan already running.")
    else:
        # Start a complete rescan when page is first accessed
        print("Starting full rescan")
        tools.netscan.refresh_full()
        
    return redirect(url_for('index'))

# Run web app
if __name__=='__main__':
    app.run(host='0.0.0.0', threaded=True)