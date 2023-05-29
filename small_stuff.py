import time
import pyautogui
import random

from local import should_i_play_closer_threat, start_threat, stop_playing, should_i_play_alarm, start_caos
from warp_zero import generate_random_offset

FRIGATE_PATH = 'imgs\\frigate.png'
CRUISER_PATH = 'imgs\\cruiser.png'
LOCK_ICON = 'imgs\\enable_lock.png'
UNLOCK_ICON = 'imgs\\enable_unlock.png'
NONE_LOCKED = 'imgs\\no_object_select.png'


def select_frig_or_cruise():
    if get_the_frigate() is not None:
        return pyautogui.locateCenterOnScreen(FRIGATE_PATH, confidence=0.8)
    if get_the_cruiser() is not None:
        return pyautogui.locateCenterOnScreen(CRUISER_PATH, confidence=0.8)
    return None


def select_to_shoot():
    ship_icon = select_frig_or_cruise()
    if ship_icon is not None:
        ship_icon = generate_random_offset(ship_icon)
        print(ship_icon)
        pyautogui.move(ship_icon)
        pyautogui.click(ship_icon, clicks=random.randint(2, 2), interval=random.uniform(0.2, 0.7))


def lock_target():
    ship_icon = pyautogui.locateCenterOnScreen(LOCK_ICON, confidence=0.9)
    if ship_icon is not None:
        ship_icon = generate_random_offset(ship_icon)
        print(ship_icon)
        pyautogui.move(ship_icon)
        pyautogui.click(ship_icon, clicks=random.randint(2, 3), interval=random.uniform(0.2, 0.7))


def send_drones():
    pyautogui.press("f")


def recovery_drones():
    # pyautogui.press("r")
    print("should")


def get_the_frigate():
    return pyautogui.locateOnScreen(FRIGATE_PATH, confidence=0.8)


def get_the_cruiser():
    return pyautogui.locateOnScreen(CRUISER_PATH, confidence=0.8)


def get_unlock_icon():
    return pyautogui.locateOnScreen(UNLOCK_ICON, confidence=0.9)


def get_none_selected():
    return pyautogui.locateOnScreen(NONE_LOCKED, confidence=0.8)


def choose_to_shoot():
    return get_the_frigate() is not None or get_the_cruiser() is not None


if __name__ == '__main__':
    threat = False
    while True:
        if should_i_play_closer_threat():
            if not threat:
                played, threat = start_threat()
            else:
                stop_playing(played)
                threat = False
        if should_i_play_alarm():
            print("NEUTRO!!!!")
            start_caos()
            recovery_drones()

        if choose_to_shoot():
            print("Nothing to shoot!!!!")
            if get_none_selected() is not None:
                print("Locking!!!!")
                count = 0
                select_to_shoot()
                lock_target()
                while get_unlock_icon() is None and count <= 8:
                    print("Waiting for lock!!!!")
                    print(count)
                    time.sleep(1)
                    count += 1
                if get_unlock_icon() is not None:
                    send_drones()

        time.sleep(1)

        print("waiting!!!!")
