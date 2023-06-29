import multiprocessing
import time
import pyautogui
import random

from app import print_message
from local import get_the_neutral, get_the_orange, get_the_red
from small_stuff import get_unlock_icon
from warp_zero import generate_random_offset, get_stopped_icon, get_msg_warp

FRIGATE_PATH = 'imgs\\frigate.png'
CRUISER_PATH = 'imgs\\cruiser.png'
BATTLESHIP_PATH = 'imgs\\battleship.png'
KEEPSTAR_PATH = 'imgs\\kepstar.png'
ENABLED_ALIGN_PATH = 'imgs\\enable_align.png'
ENABLED_WARP_PATH = 'imgs\\enable_warp.png'

LOAD_ALL_FIGHTERS = 'imgs\\load_all_fighters.png'
RECOVERY_ALL_FIGHTERS = 'imgs\\recovery_all_fighters.png'

FIGHTERS_WITH_LASER = 'imgs\\laser_fighters.png'

MSG_ALIGNING_PATH = 'imgs\\aligning.png'


def get_the_frigate():
    return pyautogui.locateOnScreen(FRIGATE_PATH, confidence=0.8)


def get_the_cruiser():
    return pyautogui.locateOnScreen(CRUISER_PATH, confidence=0.8)


def get_the_battleship():
    return pyautogui.locateOnScreen(BATTLESHIP_PATH, confidence=0.8)


def get_msg_aligning():
    return pyautogui.locateOnScreen(MSG_ALIGNING_PATH, confidence=0.99)


def click_to_align():
    align_icon = pyautogui.locateCenterOnScreen(ENABLED_ALIGN_PATH, confidence=0.8)
    if align_icon is not None:
        align_icon = generate_random_offset(align_icon)
        pyautogui.move(align_icon)
        pyautogui.click(align_icon, clicks=random.randint(2, 4), interval=random.uniform(0.2, 0.7))


def click_to_warp():
    align_icon = pyautogui.locateCenterOnScreen(ENABLED_WARP_PATH, confidence=0.8)
    if align_icon is not None:
        align_icon = generate_random_offset(align_icon)
        pyautogui.move(align_icon)
        pyautogui.click(align_icon, clicks=random.randint(2, 4), interval=random.uniform(0.2, 0.7))


def click_to_keepstar():
    ship_icon = pyautogui.locateCenterOnScreen(KEEPSTAR_PATH, confidence=0.9)
    if ship_icon is not None:
        ship_icon = generate_random_offset(ship_icon)
        pyautogui.move(ship_icon)
        pyautogui.click(ship_icon, clicks=random.randint(2, 3), interval=random.uniform(0.2, 0.7))


def select_target():
    if get_the_frigate() is not None:
        return pyautogui.locateCenterOnScreen(FRIGATE_PATH, confidence=0.8)
    if get_the_cruiser() is not None:
        return pyautogui.locateCenterOnScreen(CRUISER_PATH, confidence=0.8)
    if get_the_battleship() is not None:
        return pyautogui.locateCenterOnScreen(BATTLESHIP_PATH, confidence=0.8)
    return None


def click_select_to_shoot():
    ship_icon = select_target()
    if ship_icon is not None:
        ship_icon = generate_random_offset(ship_icon)
        pyautogui.move(ship_icon)
        pyautogui.click(ship_icon, clicks=random.randint(2, 2), interval=random.uniform(0.2, 0.7))


def click_launch_all_drones():
    ship_icon = pyautogui.locateCenterOnScreen(LOAD_ALL_FIGHTERS, confidence=0.9)
    if ship_icon is not None:
        ship_icon = generate_random_offset(ship_icon)
        pyautogui.move(ship_icon)
        pyautogui.click(ship_icon, clicks=random.randint(2, 2), interval=random.uniform(0.2, 0.7))


def click_recovery_all_drones():
    ship_icon = pyautogui.locateCenterOnScreen(RECOVERY_ALL_FIGHTERS, confidence=0.9)
    if ship_icon is not None:
        ship_icon = generate_random_offset(ship_icon)
        pyautogui.move(ship_icon)
        pyautogui.click(ship_icon, clicks=random.randint(2, 2), interval=random.uniform(0.2, 0.7))


def click_to_send_fighters():
    laser_icons = pyautogui.locateAllOnScreen(FIGHTERS_WITH_LASER, confidence=0.9)
    for laser_icon in laser_icons:
        if laser_icon is not None:
            laser_icon = generate_random_offset(laser_icon)
            pyautogui.move(laser_icon)
            pyautogui.click(laser_icon, clicks=random.randint(2, 2), interval=random.uniform(0.2, 0.7))


def should_i_align():
    return get_msg_aligning() is None and get_msg_warp() is None


def should_i_warp():
    return (get_the_neutral() is not None or get_the_orange() is not None or get_the_red() is not None) and \
        get_msg_warp() is None


def select_to_shoot():
    return get_the_frigate() is not None or \
        get_the_cruiser() is not None or \
        get_the_battleship() is not None


def loop_running_by_carrier(q=None):
    temp = 0
    while True:
        if select_to_shoot():
            print_message("Nothing to shoot!!!!", q)
            if select_target() is not None:
                print_message("Locking!!!!", q)
                count = 0
                click_select_to_shoot()
                while get_unlock_icon() is None and count <= 8:
                    print_message("Waiting for lock!!!!", q)
                    time.sleep(1)
                    count += 1
                if get_unlock_icon() is not None:
                    click_to_send_fighters()
        time.sleep(2)
        print_message("Try Again!!!!", q)
        temp += 1


def protect_carrier(q=None):
    while True:
        print_message("PROTECT CARRIER", q)
        if should_i_warp():
            print_message("WARP!!", q)
            click_to_keepstar()
            click_to_warp()
            click_recovery_all_drones()
        if should_i_align():
            print_message("I STOP", q)
            click_to_keepstar()
            click_to_align()
            time.sleep(2)
        time.sleep(1)


if __name__ == '__main__':
    from local import loop_running_local

    process = multiprocessing.Process(target=loop_running_local)
    process.start()

    process2 = multiprocessing.Process(target=protect_carrier)
    process2.start()

    # loop_running_by_carrier()
