from pynput.keyboard import Key, Listener, KeyCode
import win32api

MY_HOT_KEYS = [
    {"function1": {Key.ctrl_l, Key.alt_l, KeyCode(char="n")}},
    {"function2": {Key.shift, Key.ctrl_l, KeyCode(char="b")}},
    {"function3": {Key.alt_l, Key.ctrl_l, KeyCode(char="g")}},
]

current_keys = set()

def function1():
    print("함수1 호출")
    win32api.WinExec("calc.exe")

def function2():
    print("함수2 호출")
    win32api.WinExec("notepad.exe")

def function3():
    print("함수3 호출")
    win32api.WinExec("C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe")

def key_pressed(key):
    print("Pressed {}".format(key))
    for data in MY_HOT_KEYS:
        FUNCTION = list(data.keys())[0]
        KEYS = list(data.values())[0]

        if key in KEYS:
            current_keys.add(key)

            if all(k in current_keys for k in KEYS):
                function = eval(FUNCTION)
                function()

def key_released(key):
    print("Released {}".format(key))

    if key in current_keys:
        current_keys.remove(key)

    if key == Key.esc:
        return False

with Listener(on_press=key_pressed, on_release=key_released) as listener:
    listener.join()