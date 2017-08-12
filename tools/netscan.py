# Import modules
import subprocess
import ipaddress
import socket
from threading import Thread

print("Tailwind 0.1 - Articuno subnet sniffer")

# Network address for VPN subnet
net_addr = "10.151.25.0/24"
net_end = 32 # Cut searching after this number. Avoids scanning full space.

# Dictionary log of all hosts that are online on the network
online_hosts = {"10.151.25.0": "TESTHOST"}

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

# Function to run a scan of all IPs in host_list, and log as dictionary to online_dict
is_scanning = False
def refresh_online(host_list, online_dict):
    global is_scanning
    is_scanning = True
    # For each IP address in the subnet, 
    # run the ping command with subprocess.popen interface
    for host in host_list:
        output = subprocess.Popen(['ping', '-n', '1', '-w', '500', str(host)], stdout=subprocess.PIPE, startupinfo=info).communicate()[0]
        
        if not ("Destination host unreachable" in output.decode('utf-8') or "Request timed out" in output.decode('utf-8')):
            if not str(host) in online_dict:
                online_dict[str(host)] = socket.getfqdn(str(host))
                print(str(host), "is Online")
        else:
            if str(host) in online_dict:
                print(str(host), "is Offline")
                del online_dict[str(host)]
                
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
