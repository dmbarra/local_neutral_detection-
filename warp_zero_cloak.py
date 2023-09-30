import multiprocessing
import time
import pyautogui
import random

from app import print_message

GATE_TO_JUMP_PATH = 'imgs\\destination.png'
STATION_TO_DOCK_PATH = 'imgs\\station.png'
STATION_TO_DOCK_HOME_PATH = 'imgs\\station_home.png'
WARPING_ICON_PATH = 'imgs\\warping_icon.png'
STOPPED_ICON_PATH = 'imgs\\stopped_icon.png'
ENABLED_ALIGN_PATH = 'imgs\\enable_align2.png'
ENABLED_JUMP_PATH = 'imgs\\enable_jump.png'
ENABLED_DOCK_PATH = 'imgs\\enable_station.png'

MSG_ALIGN_PATH = 'imgs\\aligning.png'
MSG_JUMP_PATH = 'imgs\\jumping.png'
MSG_WARP_PATH = 'imgs\\warp.png'

NO_OBJECT_SELECTED = 'imgs\\no_object_select.png'
CLOAK_ICON_PATH = 'imgs\\cloak_icon.png'


def click_to_jump():
    jump_icon = pyautogui.locateCenterOnScreen(ENABLED_JUMP_PATH, confidence=0.8)
    if jump_icon is not None:
        jump_icon = generate_random_offset(jump_icon)
        pyautogui.move(jump_icon)
        pyautogui.click(jump_icon, clicks=random.randint(2, 3), interval=random.uniform(0.3, 0.9))


def click_to_dock():
    dock_icon = pyautogui.locateCenterOnScreen(ENABLED_DOCK_PATH, confidence=0.8)
    if dock_icon is not None:
        dock_icon = generate_random_offset(dock_icon)
        pyautogui.move(dock_icon)
        pyautogui.click(dock_icon, clicks=random.randint(2, 3), interval=random.uniform(0.3, 0.9))


def click_to_align():
    align_icon = pyautogui.locateCenterOnScreen(ENABLED_ALIGN_PATH, confidence=0.8)
    if align_icon is not None:
        align_icon = generate_random_offset(align_icon)
        pyautogui.move(align_icon)
        pyautogui.click(align_icon, clicks=random.randint(2, 4), interval=random.uniform(0.2, 0.7))


def click_to_cloak():
    cloak_icon = pyautogui.locateCenterOnScreen(CLOAK_ICON_PATH, confidence=0.8)
    if cloak_icon is not None:
        align_icon = generate_random_offset(cloak_icon)
        pyautogui.move(align_icon)
        pyautogui.click(align_icon, clicks=random.randint(2, 3), interval=random.uniform(0.2, 0.7))


def generate_random_offset(start):
    return random.randint(start.x - 7, start.x + 7), random.randint(start.y - 7, start.y + 7)


def get_gate_to_jump():
    return pyautogui.locateOnScreen(GATE_TO_JUMP_PATH, confidence=0.8)


def get_station_to_dock():
    if pyautogui.locateOnScreen(ENABLED_DOCK_PATH, confidence=0.8) is not None:
        return pyautogui.locateOnScreen(STATION_TO_DOCK_PATH, confidence=0.8)
    else:
        return pyautogui.locateOnScreen(STATION_TO_DOCK_HOME_PATH, confidence=0.8)


def get_warping_icon():
    return pyautogui.locateOnScreen(WARPING_ICON_PATH, confidence=0.99, grayscale=False)


def get_msg_warp():
    return pyautogui.locateOnScreen(MSG_WARP_PATH, confidence=0.99)


def get_msg_jump():
    return pyautogui.locateOnScreen(MSG_JUMP_PATH, confidence=0.99)


def get_msg_align():
    return pyautogui.locateOnScreen(MSG_ALIGN_PATH, confidence=0.99)


def get_stopped_icon():
    return pyautogui.locateOnScreen(STOPPED_ICON_PATH, confidence=0.99)


def get_no_object_selected():
    return pyautogui.locateOnScreen(NO_OBJECT_SELECTED, confidence=0.99)


def should_i_jump(control):
    return get_warping_icon() is None and \
        get_gate_to_jump() is not None and \
        get_stopped_icon() is None and \
        get_station_to_dock() is None and \
        get_msg_jump() is None and \
        get_msg_warp() is None and \
        control and \
        get_no_object_selected() is None


def should_i_align(control):
    return get_warping_icon() is None and \
        get_gate_to_jump() is not None and \
        get_stopped_icon() is not None and \
        get_station_to_dock() is None and \
        get_msg_jump() is None and \
        get_msg_warp() is None and \
        control and \
        get_no_object_selected() is None


def should_i_dock():
    return get_warping_icon() is None and get_stopped_icon() is not None and get_station_to_dock() is not None


def move_to_center():
    pyautogui.moveTo(random.randint(1000 / 2, 2000 / 2), random.randint(1000 / 2, 1100 / 2))
    time.sleep(1 / 2)


def loop_stucked(q=None):
    count: int = 0
    while True:
        print_message("Checking Stucked", q)
        if (get_stopped_icon() is not None and get_msg_warp() is None) \
                or get_msg_align() is not None:
            print_message("Count Stucked", q)
            count += 1
            time.sleep(2)
        else:
            count = 0

        if count >= 7:
            click_to_jump()
            print_message("Jumping STUCK", q)
            time.sleep(random.randint(3, 10))
            count = 0
        time.sleep(1)


def loop_running_warp_cloak(q=None):
    control_align: bool = True
    control_jump: bool = False
    while True:
        print_message("Should I align?: " + str(should_i_align(control_align)), q)
        if should_i_align(control_align):
            click_to_align()
            time.sleep(random.randint(0, 1))
            click_to_cloak()
            move_to_center()
            time.sleep(random.randint(1, 2))
            control_jump = True
            control_align = False
            print_message("Align!!!!", q)
            time.sleep(random.randint(1, 4))

        print_message("Should I jump?: " + str(should_i_jump(control_jump)), q)
        if should_i_jump(control_jump):
            click_to_jump()
            control_jump = False
            control_align = True
            print_message("Jumping!!!!", q)
            time.sleep(random.randint(7, 18))

        if should_i_dock():
            click_to_dock()
            print_message("Docking!!!!", q)
            control_jump = False
            control_align = True
            time.sleep(random.randint(7, 18))

        print_message("Waiting!!!!", q)
        time.sleep(5)


if __name__ == '__main__':
    process = multiprocessing.Process(target=loop_stucked)
    process.start()
    loop_running_warp_cloak()
