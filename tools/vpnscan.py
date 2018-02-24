# -*- coding: utf-8 -*-
"""
Created on Wed Aug 16 18:37:16 2017

@author: jtc9242
"""
import os
import datetime
import calendar

# Function to read file and return its contents
def read_file(path):
    with open(path) as file:
        return file.read()


class VpnSniffer:
    def __init__(self, log_path): 
        self.log_path = log_path
        self.status_path = os.path.join(log_path, 'openvpn-status.log')
        self.ipp_path = os.path.join(log_path, 'ipp.txt')
        
        # Update ipp on initial load
        ipp_dump = read_file(self.ipp_path)
        ipp_lines = ipp_dump.split('\n')
        self.ipp_data = [i.split(',') for i in ipp_lines[:-1]]
        
        # Create devices from ipp
        self.blank_status = {'v_add': '', 'r_add': '', 't_con': ''}
        
        self.devices = {}
        for i in self.ipp_data:
            # Add new device, and set value to copy of blank_status
            self.devices[i[0]] = dict(self.blank_status)

        # Set up month name-to-number dictionary
        self.month_dict = {v: k for k,v in enumerate(calendar.month_abbr)}
        
        # Inisially populate devices
        self.update()

    
    # Function to format dattime nicer
    def make_dt(self, raw):
        dts = raw[4:]
    
        mon = int(self.month_dict[dts[0:3]])
        day = int(dts[4:6]) # Single digits will include space at end
        tim = [int(i) for i in dts[6:15].split(':')] # Single digit days will cause space at start
        yrs = int(dts[-4:])
    
        dt = datetime.datetime(yrs, mon, day, *tim)
    
        # See http://strftime.org/
        return dt.strftime("%d %b %Y, %H:%m")
    
    
    # UPDATE LOG
    def update(self): # BUG IN HERE SOMEWHERE?
        log_dump = read_file(self.status_path)
        log_lines = log_dump.split('\n')
        
        t_break = [i for i, v in enumerate(log_lines) if v == 'ROUTING TABLE'][0]
        
        cts_lines = log_lines[3:t_break] # Clients lines
        rtg_lines = log_lines[t_break+2:-4] # Routing lines
        
        cts_data = [i.split(',') for i in cts_lines]
        rtg_data = [i.split(',') for i in rtg_lines]
        
        # Empty logged out devices
        for key, val in self.devices.items():
            if key not in [c[0] for c in cts_data]:
                self.devices[key] = dict(self.blank_status)
        
        # Add newly connected devices to dictionary
        for c in cts_data:
            if c[0] != 'UNDEF':
                self.devices[c[0]]['t_con'] = self.make_dt(c[4])
        
        for r in rtg_data:
            self.devices[r[1]]['v_add'] = r[0]
            self.devices[r[1]]['r_add'] = r[2]
        
        return self.devices
    
    