# -*- coding: utf-8 -*-
"""
Created on Wed Aug 10 09:46:09 2016

@author: jtc9242
"""
import wmi

# Connect to OpenHardwareMonitor
w = wmi.WMI(namespace="root\OpenHardwareMonitor")

# Sensors to use
sensors = [('CPU Total', 'Load'), ('CPU Package', 'Temperature'), ('GPU Core', 'Load'), ('GPU Core', 'Temperature'), ('Memory', 'Load'), ('GPU Memory', 'Load')]

def get_all(s_list):
    data_all = w.Sensor()  # Get sensor data
    
    data = {}
    
    # NOT NECESARRY EVERY TIME
    # BUILD LIST OF USED SENSORS ONCE, UPDATE AS NEEDED
    for d in data_all:
        for s in s_list:
            if d.Name == s[0] and d.SensorType == s[1]:
                data["{0}/{1}".format(d.Name, d.SensorType)] = round(d.Value,2)
    
    return data
