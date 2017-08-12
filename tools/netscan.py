# Import modules
import numpy as np
import subprocess
import ipaddress
import socket
from threading import Thread

print("Tailwind 0.1 - Articuno subnet sniffer")

# Network address for VPN subnet
net_addr = "10.151.25.0/24"
net_end = 64 # Cut searching after this number. Avoids scanning full space.

# Dictionary log of all hosts that are online on the network
online_hosts = {}

# Load list of pre-defined hostnames
predef_hostnames = {}
try: # If a file exists
    f = np.loadtxt("hostname_override.csv", delimiter=",", dtype='bytes').astype('str')
    for ip, name in f:
        predef_hostnames[ip] = name
except:
    print("No hostname override file found.")
    pass

# Create the network
ip_net = ipaddress.ip_network(net_addr)

# Get all hosts on that network
all_hosts = list(ip_net.hosts())
# Cut out unused regions of the network
scan_hosts = all_hosts[:net_end]

# Configure subprocess to hide the console window
info = subprocess.STARTUPINFO()
info.dwFlags |= subprocess.STARTF_USESHOWWINDOW
info.wShowWindow = subprocess.SW_HIDE

# Function to return string of hostname from IP address
def get_hostname(ip_add):
    return socket.getfqdn(str(ip_add))

def async_hostname(ip_add, online_dict):
    global predef_hostnames
    print("Getting hostname for {}\n".format(ip_add))
    if ip_add in predef_hostnames: # If hostname has been manually defined
        online_dict[ip_add][0] = predef_hostnames[ip_add] # Use manually defined version
    else:
        online_dict[ip_add][0] = get_hostname(ip_add) # Update hostname record without changing online status
    print("Found hostname for {} / {}\n".format(ip_add, online_dict[ip_add]))

def is_online(ip_add, mode=0):
    
    output = subprocess.Popen(['ping', '-n', '1', '-w', '500', ip_add], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, startupinfo=info).communicate()[0]

    if ("Destination host unreachable" in output.decode('utf-8') or "Request timed out" in output.decode('utf-8')):
        return False
    else:
        return True

# Create new host entry
def insert_host(ip_add, hostname, is_online, online_dict):
    if is_online:
        status = "Online"
    else:
        status = "Offline"
    online_dict[ip_add] = [hostname, status]

# Update online status of host entry (merge with above?)
def update_host(ip_add, is_online, online_dict):
    if is_online:
        status = "Online"
    else:
        status = "Offline"
    online_dict[ip_add][1] = status

# Function to run a scan of all IPs in host_list, and log as dictionary to online_dict
is_scanning = False
def refresh_online(host_list, online_dict):
    global is_scanning
    is_scanning = True
    # For each IP address in the subnet, 
    # run the ping command with subprocess.popen interface
    for host in host_list:
        host=str(host) # Ensure string type for IP address
        print("Scanning {}".format(host))

        if is_online(host):
            if not host in online_dict: # If this is a new host
                insert_host(host, "Unknown", True, online_dict) # Insert entry
                
                # Start getting hostname in the background
                t = Thread(target=async_hostname, args=(host, online_dict))
                t.start()
                
                print("{} / {} is Online".format(host, online_dict[host]))
                
            else: # If this is not a new host
                update_host(host, True, online_dict) # Update online status only
                
        else: # If host is not online
            if host in online_dict: # If host is in list
                print("{} fell offline.".format(host))
                update_host(host, False, online_dict) # Update online status only
                print(host, "is Offline")
                
    is_scanning = False
    print("Scan finished.")

# Refresh all IPs on the allowed subnet
def refresh_full():
    print("Refreshing subnet")
    t = Thread(target=refresh_online, args=(scan_hosts, online_hosts))
    t.start()

# Refresh only the connections previously marked as online
def refresh_active():
    print("Checking connections")
    t = Thread(target=refresh_online, args=(online_hosts.keys(), online_hosts))
    t.start()
