from pynput.keyboard import Key, Listener, KeyCode

def key_pressed(key):
    print("Pressed {}".format(key))

def key_released(key):
    print("Released {}".format(key))

    if key == Key.esc:
        return False

with Listener(on_press=key_pressed, on_release=key_released) as listener:
    listener.join()