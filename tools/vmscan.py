import subprocess
import os
import re

# Get formatted string of Hyper-V stats
def ps_str(cmd, error_string = None, debug=False):
    command = 'powershell.exe \"{}\"'.format(cmd)

    # Open subprocess
    # stdin=subprocess.DEVNULL fixes errors when running as a service, with no stdin
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, stdin=subprocess.DEVNULL)
    stdout, err = process.communicate()

    if debug:
        print("Command:")
        print(command)
        print("Output:")
        print(stdout)
        print("User:")
        print(os.getlogin())
    
    if not err:
        # Check for permission error
        if stdout.decode("utf-8").split('.')[0] != error_string:
            return stdout.decode("utf-8")
        else:
            raise Exception(error_string)


def vm_dict():
    cmd_string = "get-vm | select Name, CPUUsage, MemoryAssigned, Uptime, State"
    err_string = "get-vm : You do not have the required permission to complete this task"
    vm_string = ps_str(cmd_string, err_string)
    

    if vm_string:

        n_cols = 5  # Fixed 
        vm_split = vm_string.split()
        vm_split = [s for s in vm_split if s != ":"]

        vm_heads = vm_split[::2][:n_cols]
        vm_datas = vm_split[1:][::2]

        n_vms = int(len(vm_datas)/n_cols)

        # Create array of VM data arrays
        vm_array = []
        for i in range(n_vms):
            vm_array.append(vm_datas[i*n_cols:(i+1)*n_cols])

        # Convert VM array into VM dictionary
        vm_dict_list = []

        # For each VM
        for vm in vm_array:
            _dict = {}  # Make a dictionary
            for col, col_data in enumerate(vm):  # For each column of data
                _dict[vm_heads[col]] = col_data  # Get column header, and add data to dictionary
            vm_dict_list.append(_dict)  # Append completed dictionary to VM list

        # Fix up data formats
        for vm in vm_dict_list:
            # Format uptime
            uptime_d_t_ms = vm['Uptime'].split(".")
            if len(uptime_d_t_ms) > 2:
                uptime_days = uptime_d_t_ms[0]
                uptime_time = uptime_d_t_ms[1]
            else:
                uptime_days = 0
                uptime_time = uptime_d_t_ms[0]
            
            uptime_h_m_s = uptime_time.split(":")
            uptime_d_h_m = [uptime_days, uptime_h_m_s[0], uptime_h_m_s[1]]

            vm['Uptime'] = "{}d{}h{}m".format(*uptime_d_h_m)
            # Format memory assigned
            vm['MemoryAssigned'] = int(int(vm['MemoryAssigned'])/1E6)
            # Convert CPU pct string to int
            vm['CPUUsage'] = int(vm['CPUUsage'])
            # Calculate an online/offline status code
            if vm['State'] == "Running":
                vm['Status'] = "online"
            elif "Off" in vm['State']:
                vm['Status'] = "offline"
            else:
                vm['Status'] = "excline"

        return vm_dict_list

# TODO: Tidy up data and heading formats
# TODO: Integrate with Tailwind, based on netscan
# TODO: Shrink Tailwind font size and tidy up/modernise

if __name__ == "__main__":
    print(vm_dict())