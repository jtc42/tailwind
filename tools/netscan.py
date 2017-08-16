# -*- coding: utf-8 -*-
"""
Created on Wed Aug 16 18:37:16 2017

@author: jtc9242
"""
import os

SVR_IP = '10.151.25.1'
SVR_NAME = 'jtcsvr-articuno'

OVPN_PATH = 'C:\OpenVPN'
LOG_PATH = os.path.join(OVPN_PATH, 'config', 'openvpn-status.log')
IPP_PATH = os.path.join(OVPN_PATH, 'config', 'ipp.txt')

def read_file(path):
    with open(path) as file:
        return file.read()

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
def update():
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
            devices[key] = blank_status
    
    for c in cts_data:
        devices[c[0]]['t_con'] = c[4]
    
    for r in rtg_data:
        devices[r[1]]['v_add'] = r[0]
        devices[r[1]]['r_add'] = r[2]

update()