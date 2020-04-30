import time, threading, sys, os
from pynput.mouse import Button, Controller
from pynput.keyboard import Listener, KeyCode, Key

f_keys = ['F1', 'F2', 'F3', 'F4', 'F5', 'F6', 'F7', 'F8', 'F9', 'F10', 'F11', 'F12']
f_triggers = [Key.f1, Key.f2, Key.f3, Key.f4, Key.f5, Key.f6, 
    Key.f7, Key.f8, Key.f9, Key.f10, Key.f11, Key.f12]
found = 0

scroll_chooser = input('\n Do you want to include scrolling into your clicking?\n' 
    + ' Type "yes/no" to include scrolling into clicking,\n' 
    + ' or type "only" for scrolling only then press ENTER\n\n ')

while scroll_chooser.lower() != 'yes' and scroll_chooser.lower() != 'no' and scroll_chooser.lower() != 'only' and scroll_chooser.lower() != 'y' and scroll_chooser.lower() != 'n':
    scroll_chooser = str(input('\n Unknown choice, please choose again and press ENTER\n\n '))

if scroll_chooser.lower() == 'y':
    scroll_chooser = 'yes'
elif scroll_chooser.lower() == 'n':
    scroll_chooser = 'no'

if scroll_chooser.lower() != 'only':
    button = input('\n For left click write 1, for right click write 2 and press ENTER\n\n ')
    while button != '1' and button != '2':
        button = input('\n Unknown choice, please choose again and press ENTER\n\n ')
    if button == '1':
        button = Button.left
    elif button == '2':
        button = Button.right
    
    if button == Button.right:
        middle_click = str(input('\n Do you want to want to alternate between right-clicking and middle-clicking?\n'
        + ' Type "yes/no" then press ENTER\n\n '))
        while middle_click.lower() != 'yes' and middle_click.lower() != 'no' and middle_click.lower() != 'y' and middle_click.lower() != 'n':
            middle_click = str(input('\n Unknown choice, please choose again and press ENTER\n\n '))
        if middle_click.lower() == 'yes' or middle_click.lower() == 'y':
            middle_click = Button.middle

if scroll_chooser.lower() != 'only':
    delay = input('\n Write your delay for clicking in ms,\n (for click-lock type in 0) then press ENTER\n\n ')
    while True:
        try:
            delay = int(delay) / 1000
            break
        except:
            delay = input('\n Wrong input, please try again.\n\n ')

start_stop_key = input('\n Write your start/stop key, then press ENTER\n\n ')
while len(start_stop_key) > 1 and found == 0:
    for i in range(0,12):
        if start_stop_key.upper() == f_keys[i]:
            found = 1
    if found == 1:
        break
    start_stop_key = input('\n Wrong input, please try again.\n\n ')
found = 0

exit_key = input('\n Write your exit key, then press ENTER\n\n ')
while len(exit_key) > 1 and found == 0:
    if exit_key.lower() == start_stop_key.lower():
        exit_key = input('\n Exit key is the same as start/stop key, please choose again.\n\n ')
    else:
        for i in range(0,12):
            if exit_key.upper() == f_keys[i]:
                found = 1
        if found == 1:
            break
        exit_key = input('\n Wrong input, please try again.\n\n ')
found = 0

reset_key = input('\n Write your reset key, then press ENTER\n\n ')
while len(reset_key) > 1 and found == 0:
    if reset_key.lower() == start_stop_key.lower():
        reset_key = input('\n Reset key is the same as start/stop key, please choose again.\n\n ')
    elif reset_key.lower() == exit_key.lower():
        reset_key = input('\n Reset key is the same as exit key, please choose again.\n\n ')
    else:
        for i in range(0,12):
            if reset_key.upper() == f_keys[i]:
                found = 1
        if found == 1:
            break
        reset_key = input('\n Wrong input, please try again.\n\n ')

if scroll_chooser.lower() != 'only' and delay > 0:
    os.system('cls')
    if button == Button.left:
        print('\n You are using "left-click".')
    elif button == Button.right:
        print('\n You are using "right-click".')
        if middle_click == Button.middle:
            print('\n You will be alternating between "right-click" and "middle-click".')
    print('\n Click delay is set to "' + str((delay * 1000)) + '" ms.')
elif scroll_chooser.lower() != 'only' and delay == 0:
    os.system('cls')
    if button == Button.left:
        print('\n You are using "left-click".')
    elif button == Button.right:
        print('\n You are using "right-click".')
        if middle_click == Button.middle:
            print('\n You will be alternating between "right-click" and "middle-click".')
    print('\n Click delay is set to "0.0" ms(click-lock).')
    
if scroll_chooser.lower() != 'no':
    if scroll_chooser.lower() != 'only':
        print('\n Scroll delay is set to "100.0" ms.')
    else:
        os.system('cls')
        print('\n Scroll delay is set to "100.0" ms.')

if len(start_stop_key) > 1:
    for i in range(0, 12):
        if start_stop_key.upper() == f_keys[i]:
            print('\n Your start/stop key is "' + f_keys[i] + '" key.')
            start_stop_key = f_triggers[i]
            break
else:
    print('\n Your start/stop key is "' + start_stop_key + '" key.')
    start_stop_key = KeyCode(char = start_stop_key.lower())

if len(exit_key) > 1:
    for i in range(0, 12):
        if exit_key.upper() == f_keys[i]:
            print('\n Your exit key is "' + f_keys[i] + '" key.')
            exit_key = f_triggers[i]
            break
else:
    print('\n Your exit key is "' + exit_key + '" key.')
    exit_key = KeyCode(char = exit_key.lower())
    
if len(reset_key) > 1:
    for i in range(0, 12):
        if reset_key.upper() == f_keys[i]:
            print('\n Your reset key is "' + f_keys[i] + '" key.')
            reset_key = f_triggers[i]
            break
else:
    print('\n Your reset key is "' + reset_key + '" key.')
    reset_key = KeyCode(char = reset_key.lower())

print('\n Now press key for your desired action.')

class MouseControl(threading.Thread):
    if scroll_chooser.lower() == 'only':
        def __init__(self):
            super().__init__()
            self.running = False
            self.program_running = True
    else:
        def __init__(self, delay, button):
            super().__init__()
            self.delay = delay
            self.button = button
            self.running = False
            self.program_running = True

    def start_clicking(self):
        self.running = True
        if scroll_chooser.lower() != 'only':
            if self.delay == 0:
                mouse.release(self.button)
            if self.button == Button.right:
                if middle_click == Button.middle:
                    mouse.release(Button.middle)

    def stop_clicking(self):
        self.running = False
        if scroll_chooser.lower() != 'only':
            if self.delay == 0:
                mouse.release(self.button)
            if self.button == Button.right:
                if middle_click == Button.middle:
                    mouse.release(Button.middle)

    def exit(self):
        self.stop_clicking()
        self.program_running = False
        if scroll_chooser.lower() != 'only':
            if self.delay == 0:
                mouse.release(self.button)

    def run(self):
        while self.program_running:
            while self.running:
                if scroll_chooser.lower() == 'no':
                    if self.delay == 0:
                        mouse.press(self.button)
                        time.sleep(0.1)
                    else:
                        mouse.click(self.button)
                        time.sleep(self.delay)
                        if self.button == Button.right:
                            if middle_click == Button.middle:
                                mouse.click(Button.middle)
                                time.sleep(self.delay)
                elif scroll_chooser.lower() == 'only':
                    mouse.scroll(0, 1)
                    time.sleep(0.1)
                elif scroll_chooser.lower() == 'yes':
                    if self.delay == 0:
                        mouse.press(self.button)
                        mouse.scroll(0, 1)
                        time.sleep(0.1)
                    else:
                        mouse.click(self.button)
                        time.sleep(self.delay)
                        mouse.scroll(0, 1)
                        time.sleep(0.1)
                        if self.button == Button.right:
                            if middle_click == Button.middle:
                                mouse.click(Button.middle)
                                time.sleep(self.delay)

mouse = Controller()
if scroll_chooser.lower() == 'only':
    mouse_thread = MouseControl()
    mouse_thread.start()
else:
    mouse_thread = MouseControl(delay, button)
    mouse_thread.start()

def on_press(key):
    if key == start_stop_key:
        if mouse_thread.running:
            mouse_thread.stop_clicking()
        else:
            mouse_thread.start_clicking()
    elif key == exit_key:
        mouse_thread.exit()
        listener.stop()
    elif key == reset_key:
        mouse_thread.exit()
        listener.stop()
        os.system('cls')
        os.execl(sys.executable, sys.executable, * sys.argv)

with Listener(on_press = on_press) as listener:
    listener.join()