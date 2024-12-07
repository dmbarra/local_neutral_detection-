import multiprocessing
import time
import pyautogui
import random

from app import print_message
from local import should_i_play_closer_threat, start_threat, stop_playing, should_i_play_alarm, start_caos, start_bloop
from warp_zero import generate_random_offset

FRIGATE_PATH = 'imgs\\frigate.png'
CRUISER_PATH = 'imgs\\cruiser.png'
BATTLECRUISER_PATH = 'imgs\\battlecruiser.png'
BATTLESHIP_PATH = 'imgs\\battleship.png'

LOCK_ICON = 'imgs\\enable_lock.png'
UNLOCK_ICON = 'imgs\\enable_unlock.png'
NONE_LOCKED = 'imgs\\no_object_select.png'

LOCKED_CRUISER_PATH = 'imgs\\cruiser_locked.png'
LOCKED_FRIGATE_PATH = 'imgs\\frigate_locked.png'
LOCKED_BATTLECRUISER_PATH = 'imgs\\battlecruiser_locked.png'
LOCKED_BATTLESHIP_PATH = 'imgs\\battleship_locked.png'
LOCKED2_CRUISER_PATH = 'imgs\\cruiser_locked2.png'
LOCKED2_FRIGATE_PATH = 'imgs\\frigate_locked2.png'
LOCKED2_BATTLECRUISER_PATH = 'imgs\\battlecruiser_locked2.png'
LOCKED2_BATTLESHIP_PATH = 'imgs\\battleship_locked2.png'

CONFIDENCE = 0.8


def list_targets():
    if pyautogui.locateOnScreen(FRIGATE_PATH, confidence=CONFIDENCE) is not None:
        return list(pyautogui.locateAllOnScreen(FRIGATE_PATH, confidence=CONFIDENCE))
    if pyautogui.locateOnScreen(CRUISER_PATH, confidence=CONFIDENCE) is not None:
        return list(pyautogui.locateAllOnScreen(CRUISER_PATH, confidence=CONFIDENCE))
    # if pyautogui.locateOnScreen(BATTLECRUISER_PATH, confidence=CONFIDENCE) is not None:
    #     return list(pyautogui.locateAllOnScreen(BATTLECRUISER_PATH, confidence=CONFIDENCE))
    # if pyautogui.locateOnScreen(BATTLESHIP_PATH, confidence=CONFIDENCE) is not None:
    #     return list(pyautogui.locateAllOnScreen(BATTLESHIP_PATH, confidence=CONFIDENCE))
    return []


def list_selected_targets():
    if pyautogui.locateOnScreen(LOCKED_FRIGATE_PATH, confidence=CONFIDENCE, grayscale=True) is not None \
            or pyautogui.locateOnScreen(LOCKED2_FRIGATE_PATH, confidence=CONFIDENCE, grayscale=True) is not None:
        return list(pyautogui.locateAllOnScreen(LOCKED_FRIGATE_PATH, confidence=CONFIDENCE, grayscale=True)) \
            + list(pyautogui.locateAllOnScreen(LOCKED2_FRIGATE_PATH, confidence=CONFIDENCE, grayscale=True))
    if pyautogui.locateOnScreen(LOCKED_CRUISER_PATH, confidence=CONFIDENCE, grayscale=True) is not None \
            or pyautogui.locateOnScreen(LOCKED2_CRUISER_PATH, confidence=CONFIDENCE, grayscale=True) is not None:
        return list(pyautogui.locateAllOnScreen(LOCKED_CRUISER_PATH, confidence=CONFIDENCE, grayscale=True)) \
            + list(pyautogui.locateAllOnScreen(LOCKED2_CRUISER_PATH, confidence=CONFIDENCE, grayscale=True))
    # if pyautogui.locateOnScreen(LOCKED_BATTLECRUISER_PATH, confidence=CONFIDENCE, grayscale=True) is not None \
    #         or pyautogui.locateOnScreen(LOCKED2_BATTLECRUISER_PATH, confidence=CONFIDENCE, grayscale=True) is not None:
    #     return list(pyautogui.locateAllOnScreen(LOCKED_BATTLECRUISER_PATH, confidence=CONFIDENCE, grayscale=True)) \
    #         + list(pyautogui.locateAllOnScreen(LOCKED2_BATTLECRUISER_PATH, confidence=CONFIDENCE, grayscale=True))
    # if pyautogui.locateOnScreen(LOCKED_BATTLESHIP_PATH, confidence=CONFIDENCE, grayscale=True) is not None \
    #         or pyautogui.locateOnScreen(LOCKED2_BATTLESHIP_PATH, confidence=CONFIDENCE, grayscale=True) is not None:
    #     return list(pyautogui.locateAllOnScreen(LOCKED_BATTLESHIP_PATH, confidence=CONFIDENCE, grayscale=True)) \
    #         + list(pyautogui.locateAllOnScreen(LOCKED2_BATTLESHIP_PATH, confidence=CONFIDENCE, grayscale=True))
    return []


def select_to_shoot(target_icon):
    if target_icon is not None:
        target_random = generate_random_offset(pyautogui.center(target_icon))
        with pyautogui.hold('ctrl'):
            pyautogui.sleep(2)
            pyautogui.move(target_random)
            pyautogui.click(target_random, clicks=random.randint(2, 2), interval=random.uniform(0.2, 0.7))


def send_drones():
    pyautogui.press("f")


def get_unlock_icon():
    return pyautogui.locateOnScreen(UNLOCK_ICON, confidence=0.9)


def loop_running_small_stuff(q=None):
    control_locking = False
    pyautogui.FAILSAFE = False
    while True:
        print_message("Loop to check targets", q)
        if list_targets() and not control_locking and not list_selected_targets():
            while list_targets() > list_selected_targets() or not control_locking:
                print_message("There is targets: " + str(len(list_targets())), q)
                print_message("There is already locked: " + str(len(list_selected_targets())), q)
                for target in list_targets():
                    count = 0
                    select_to_shoot(target)
                    while get_unlock_icon() is None and count <= 8:
                        print_message("Waiting for lock!!!!", q)
                        time.sleep(1)
                        count += 1
                time.sleep(1 / 2)
                control_locking = True

        if list_selected_targets():
            print_message("targets to clear", q)
            targets = list_selected_targets()
            press_f = True
            while list_selected_targets() == targets:
                if press_f:
                    send_drones()
                    press_f = False
                time.sleep(2)
                print_message("Waiting target die!", q)
        else:
            print_message("Clear control lock", q)
            control_locking = False
        time.sleep(3)


if __name__ == '__main__':
    from local import loop_running_local
    process = multiprocessing.Process(target=loop_running_local)
    process.start()
    loop_running_small_stuff()
