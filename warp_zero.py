import time
import pyautogui
import random

GATE_TO_JUMP_PATH = 'imgs\\destination.png'
STATION_TO_DOCK_PATH = 'imgs\\station.png'
STATION_TO_DOCK_HOME_PATH = 'imgs\\station_home.png'
WARPING_ICON_PATH = 'imgs\\warping_icon.png'
STOPPED_ICON_PATH = 'imgs\\stopped_icon.png'
ENABLED_ALIGN_PATH = 'imgs\\enable_align.png'
ENABLED_JUMP_PATH = 'imgs\\enable_jump.png'
ENABLED_DOCK_PATH = 'imgs\\enable_station.png'

MSG_JUMP_PATH = 'imgs\\jumping.png'
MSG_WARP_PATH = 'imgs\\warp.png'

CONTROL_ALIGN = False
CONTROL_JUMP = False


def click_to_jump():
    jump_icon = pyautogui.locateCenterOnScreen(ENABLED_JUMP_PATH, confidence=0.8)
    if jump_icon is not None:
        jump_icon = generate_random_offset(jump_icon)
        print(jump_icon)
        pyautogui.move(jump_icon)
        pyautogui.click(jump_icon, clicks=random.randint(2, 3), interval=random.uniform(0.3, 0.9))
        return True


def click_to_dock():
    dock_icon = pyautogui.locateCenterOnScreen(ENABLED_DOCK_PATH, confidence=0.8)
    if dock_icon is not None:
        dock_icon = generate_random_offset(dock_icon)
        print(dock_icon)
        pyautogui.move(dock_icon)
        pyautogui.click(dock_icon, clicks=random.randint(2, 3), interval=random.uniform(0.3, 0.9))


def click_to_align():
    align_icon = pyautogui.locateCenterOnScreen(ENABLED_ALIGN_PATH, confidence=0.8)
    if align_icon is not None:
        align_icon = generate_random_offset(align_icon)
        print(align_icon)
        pyautogui.move(align_icon)
        pyautogui.click(align_icon, clicks=random.randint(2, 4), interval=random.uniform(0.2, 0.7))
        return True


def generate_random_offset(start):
    print(start)
    return random.randint(start.x - 7, start.x + 7), random.randint(start.y - 7, start.y + 7)


def get_gate_to_jump():
    return pyautogui.locateOnScreen(GATE_TO_JUMP_PATH, confidence=0.8)


def get_station_to_dock():
    if pyautogui.locateOnScreen(STATION_TO_DOCK_PATH, confidence=0.8) is not None:
        return pyautogui.locateOnScreen(STATION_TO_DOCK_PATH, confidence=0.8)
    else:
        return pyautogui.locateOnScreen(STATION_TO_DOCK_HOME_PATH, confidence=0.8)


def get_warping_icon():
    return pyautogui.locateOnScreen(WARPING_ICON_PATH, confidence=0.99, grayscale=False)


def get_msg_warp():
    return pyautogui.locateOnScreen(MSG_WARP_PATH, confidence=0.99)


def get_msg_jump():
    return pyautogui.locateOnScreen(MSG_JUMP_PATH, confidence=0.99)


def get_stopped_icon():
    return pyautogui.locateOnScreen(STOPPED_ICON_PATH, confidence=0.99)


def should_i_jump(control):
    return get_warping_icon() is None and \
        get_gate_to_jump() is not None and \
        get_stopped_icon() is None and \
        get_station_to_dock() is None and \
        get_msg_jump() is None and \
        get_msg_warp() is None and \
        control


def should_i_align(control):
    return get_warping_icon() is None and \
        get_gate_to_jump() is not None and \
        get_stopped_icon() is not None and \
        get_station_to_dock() is None and \
        get_msg_jump() is None and \
        get_msg_warp() is None and \
        control


def should_i_dock():
    return get_warping_icon() is None and get_stopped_icon() is not None and get_station_to_dock() is not None


if __name__ == '__main__':
    CONTROL_ALIGN = True
    while True:
        if should_i_align(CONTROL_ALIGN):
            CONTROL_JUMP = click_to_align()
            print("Align!!!!")
            time.sleep(random.randint(2, 5))

        if should_i_jump(CONTROL_JUMP):
            CONTROL_ALIGN = click_to_jump()
            print("Jumping!!!!")
            time.sleep(random.randint(7, 18))
        else:
            print("CANNOT Jumping!!!!")

        if should_i_dock():
            click_to_dock()
            print("Docking!!!!")
            time.sleep(random.randint(7, 18))
        else:
            print("CANNOT Warp!!!!")

        print("Waiting!!!!")
        time.sleep(5)
