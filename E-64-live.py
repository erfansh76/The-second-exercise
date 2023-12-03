import os
from ptrace.debugger import PtraceDebugger
import psutil

# Function to get the PID (Process ID) by the process name
def get_pid_by_name(process_name):
    # Iterate over all running processes
    for proc in psutil.process_iter(['pid', 'name']):
        # If the process name matches, return its PID
        if proc.info['name'] == process_name:
            return proc.info['pid']
    # If no process with the given name is found, return None
    return None

# Function to attach to a process and read memory
def read_memory(pid, address, length):
    # Create a ptrace debugger
    debugger = PtraceDebugger()
    # Add the process to the debugger
    process = debugger.addProcess(pid, False)
    # Read bytes from the process memory
    data = process.readBytes(address, length)
    # Quit the debugger
    debugger.quit()
    # Return the read data
    return data

# Function to attach to a process and write memory
def write_memory(pid, address, data):
    # Create a ptrace debugger
    debugger = PtraceDebugger()
    # Add the process to the debugger
    process = debugger.addProcess(pid, False)
    # Write bytes to the process memory
    process.writeBytes(address, data)
    debugger.quit()

# Function to write a specific value to a memory address
def write_value(pid, address, lives_count):
    data = lives_count.to_bytes(4, byteorder='little', signed=True)
    write_memory(pid, address, data)

# Get PID by process name
process_name = "toppler64"  # Replace with your process name
pid = get_pid_by_name(process_name)

# If no process is found with the given name, print an error message
if pid is None:
    print(f"No process named {process_name} found")
else:
    # The memory address of interest
    live_address = 0x42b8f0
    # Set the value at the memory address to 100
    write_value(pid, live_address, 100)