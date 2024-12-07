import multiprocessing
import time
import pyautogui
import random

from app import print_message
from actions.local import get_the_neutral, get_the_orange, get_the_red
from actions.small_stuff import get_unlock_icon, list_selected_targets, list_targets, select_to_shoot
from actions.warp_zero import generate_random_offset, get_stopped_icon, get_msg_warp

KEEPSTAR_PATH = 'imgs/kepstar.png'
ENABLED_ALIGN_PATH = 'imgs/enable_align.png'
ENABLED_WARP_PATH = 'imgs/enable_warp.png'

LOAD_ALL_FIGHTERS = '..imgs/load_all_fighters.png'
RECOVERY_ALL_FIGHTERS = 'imgs/recovery_all_fighters.png'

FIGHTERS_WITH_LASER = 'imgs/laser_fighters.png'

MSG_ALIGNING_PATH = 'imgs/aligning.png'
MSG_LOCK_PATH = 'imgs/lock.png'


def get_msg_lock():
    return pyautogui.locateOnScreen(MSG_LOCK_PATH, confidence=0.99)


def get_msg_aligning():
    return pyautogui.locateOnScreen(MSG_ALIGNING_PATH, confidence=0.99)


def move_to_center():
    pyautogui.moveTo(random.randint(1000 / 2, 2000 / 2), random.randint(1000 / 2, 1100 / 2))
    time.sleep(1 / 2)


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


def click_launch_all_drones():
    ship_icon = pyautogui.locateCenterOnScreen(LOAD_ALL_FIGHTERS, confidence=0.9)
    if ship_icon is not None:
        ship_icon = generate_random_offset(ship_icon)
        pyautogui.move(ship_icon)
        pyautogui.click(ship_icon, clicks=random.randint(2, 2), interval=random.uniform(0.2, 0.7))
        move_to_center()


def click_recovery_all_drones():
    ship_icon = pyautogui.locateCenterOnScreen(RECOVERY_ALL_FIGHTERS, confidence=0.9)
    if ship_icon is not None:
        ship_icon = generate_random_offset(ship_icon)
        pyautogui.move(ship_icon)
        pyautogui.click(ship_icon, clicks=random.randint(2, 2), interval=random.uniform(0.2, 0.7))


def click_to_send_fighters():
    laser_icons = pyautogui.locateAllOnScreen(FIGHTERS_WITH_LASER, confidence=0.9)
    for laser_icon in laser_icons:
        time.sleep(1 / 2)
        if laser_icon is not None:
            random_icon = generate_random_offset(pyautogui.center(laser_icon))
            pyautogui.move(random_icon)
            pyautogui.click(random_icon, clicks=random.randint(2, 2), interval=random.uniform(0.2, 0.7))
            move_to_center()


def should_i_align():
    return get_msg_aligning() is None and get_msg_warp() is None and get_msg_lock() is None


def should_i_warp(control_warp):
    return (get_the_neutral() is not None or get_the_orange() is not None or get_the_red() is not None) and \
        get_msg_warp() is None and not control_warp


def loop_running_by_carrier(q=None):
    control_locking = False
    pyautogui.FAILSAFE = False
    fighters_out = False
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
            if not fighters_out:
                print_message("launch drones", q)
                click_launch_all_drones()
                time.sleep(2)
                fighters_out = True
            print_message("targets to clear", q)
            targets = list_selected_targets()
            press_f = True
            while list_selected_targets() == targets:
                if press_f:
                    click_to_send_fighters()
                    press_f = False
                time.sleep(2)
                print_message("Waiting target die!", q)
        else:
            print_message("Clear control lock", q)
            control_locking = False
            if fighters_out:
                print_message("Recovery drones", q)
                click_recovery_all_drones()
                fighters_out = False
        time.sleep(3)


def protect_carrier(q=None):
    control_warp = False
    while True:
        print_message("PROTECT CARRIER", q)
        if should_i_warp(control_warp):
            print_message("WARP!!", q)
            click_to_keepstar()
            click_to_warp()
            click_recovery_all_drones()
            control_warp = True
        if should_i_align():
            print_message("I STOP", q)
            click_to_keepstar()
            click_to_align()
            time.sleep(5)
        time.sleep(1)


if __name__ == '__main__':
    from local import loop_running_local

    process = multiprocessing.Process(target=loop_running_local)
    process.start()

    process2 = multiprocessing.Process(target=protect_carrier)
    process2.start()

    loop_running_by_carrier()
