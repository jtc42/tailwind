# -*- coding: utf-8 -*-
"""
Created on Wed Aug 16 18:37:16 2017

@author: jtc9242
"""
import os
import datetime
import calendar

# Set up parameters
SVR_IP = '10.151.25.1'
SVR_NAME = 'jtcsvr-articuno'

OVPN_PATH = 'C:\OpenVPN'
LOG_PATH = os.path.join(OVPN_PATH, 'config', 'openvpn-status.log')
IPP_PATH = os.path.join(OVPN_PATH, 'config', 'ipp.txt')

# Set up month name-to-number dictionary
month_dict = {v: k for k,v in enumerate(calendar.month_abbr)}

# Function to read file and return its contents
def read_file(path):
    with open(path) as file:
        return file.read()

# Function to format dattime nicer
def make_dt(raw):
    dts = raw[4:]

    mon = int(month_dict[dts[0:3]])
    day = int(dts[4:6]) # Single digits will include space at end
    tim = [int(i) for i in dts[6:15].split(':')] # Single digit days will cause space at start
    yrs = int(dts[-4:])

    dt = datetime.datetime(yrs, mon, day, *tim)

    # See http://strftime.org/
    # Alt: dt.strftime("%d %b %Y, %I:%m%p")
    return dt.strftime("%d %b %Y, %H:%m")

    
# Update ipp
ipp_dump = read_file(IPP_PATH)
ipp_lines = ipp_dump.split('\n')
ipp_data = [i.split(',') for i in ipp_lines[:-1]]

# Create devices from ipp
blank_status = {'v_add': '', 'r_add': '', 't_con': ''}

devices = { SVR_NAME: {'v_add': SVR_IP, 'r_add': '', 't_con': ''} }

for i in ipp_data:
    # Add new device, and set value to copy of blank_status
    devices[i[0]] = dict(blank_status)

# UPDATE LOG
def update(): # BUG IN HERE SOMEWHERE
    log_dump = read_file(LOG_PATH)
    log_lines = log_dump.split('\n')
    
    t_break = [i for i, v in enumerate(log_lines) if v == 'ROUTING TABLE'][0]
    
    cts_lines = log_lines[3:t_break] # Clients lines
    rtg_lines = log_lines[t_break+2:-4] # Routing lines
    
    cts_data = [i.split(',') for i in cts_lines]
    rtg_data = [i.split(',') for i in rtg_lines]
    
    # Empty logged out devices
    for key, val in devices.items():
        if key not in [c[0] for c in cts_data] and key is not SVR_NAME:
            devices[key] = dict(blank_status)
    
    # Add newly connected devices to dictionary
    for c in cts_data:
        devices[c[0]]['t_con'] = make_dt(c[4])
    
    for r in rtg_data:
        devices[r[1]]['v_add'] = r[0]
        devices[r[1]]['r_add'] = r[2]
    
    return devices

update()