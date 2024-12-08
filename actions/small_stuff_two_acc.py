import multiprocessing
import time
import pyautogui
import random

from actions.screen_manager import ScreenAreaSelector
from app import print_message
from actions.warp_zero import generate_random_offset

FRIGATE_PATH = 'imgs/frigate.png'
CRUISER_PATH = 'imgs/cruiser.png'
BATTLECRUISER_PATH = 'imgs/battlecruiser.png'
BATTLESHIP_PATH = 'imgs/battleship.png'

LOCK_ICON = 'imgs/enable_lock.png'
UNLOCK_ICON = 'imgs/enable_unlock.png'
NONE_LOCKED = 'imgs/no_object_select.png'

LOCKED_CRUISER_PATH = 'imgs/cruiser_locked.png'
LOCKED_FRIGATE_PATH = 'imgs/frigate_locked.png'
LOCKED_BATTLECRUISER_PATH = 'imgs/battlecruiser_locked.png'
LOCKED_BATTLESHIP_PATH = 'imgs/battleship_locked.png'
LOCKED2_CRUISER_PATH = 'imgs/cruiser_locked2.png'
LOCKED2_FRIGATE_PATH = 'imgs/frigate_locked2.png'
LOCKED2_BATTLECRUISER_PATH = 'imgs/battlecruiser_locked2.png'
LOCKED2_BATTLESHIP_PATH = 'imgs/battleship_locked2.png'

CONFIDENCE = 0.8


def area_has_frigates(region):
    if pyautogui.locateOnScreen(FRIGATE_PATH, confidence=CONFIDENCE, region=region) is not None:
        return list(pyautogui.locateAllOnScreen(FRIGATE_PATH, confidence=CONFIDENCE, region=region))


def area_has_cruisers(region):
    if pyautogui.locateOnScreen(CRUISER_PATH, confidence=CONFIDENCE, region=region) is not None:
        return list(pyautogui.locateAllOnScreen(CRUISER_PATH, confidence=CONFIDENCE, region=region))


def list_targets(region):
    # Search for images in the defined region
    if pyautogui.locateOnScreen(FRIGATE_PATH, confidence=CONFIDENCE, region=region) is not None:
        return list(pyautogui.locateAllOnScreen(FRIGATE_PATH, confidence=CONFIDENCE, region=region))
    if pyautogui.locateOnScreen(CRUISER_PATH, confidence=CONFIDENCE, region=region) is not None:
        return list(pyautogui.locateAllOnScreen(CRUISER_PATH, confidence=CONFIDENCE, region=region))

    return []


def list_selected_targets(region):
    # Locate LOCKED_FRIGATE_PATH or LOCKED2_FRIGATE_PATH
    if pyautogui.locateOnScreen(LOCKED_FRIGATE_PATH, confidence=CONFIDENCE, grayscale=True, region=region) is not None \
            or pyautogui.locateOnScreen(LOCKED2_FRIGATE_PATH, confidence=CONFIDENCE, grayscale=True,
                                        region=region) is not None:
        return list(
            pyautogui.locateAllOnScreen(LOCKED_FRIGATE_PATH, confidence=CONFIDENCE, grayscale=True, region=region)) \
            + list(
                pyautogui.locateAllOnScreen(LOCKED2_FRIGATE_PATH, confidence=CONFIDENCE, grayscale=True, region=region))

    # Locate LOCKED_CRUISER_PATH or LOCKED2_CRUISER_PATH
    # if pyautogui.locateOnScreen(LOCKED_CRUISER_PATH, confidence=CONFIDENCE, grayscale=True, region=region) is not None \
    #         or pyautogui.locateOnScreen(LOCKED2_CRUISER_PATH, confidence=CONFIDENCE, grayscale=True,
    #                                     region=region) is not None:
    #     return list(
    #         pyautogui.locateAllOnScreen(LOCKED_CRUISER_PATH, confidence=CONFIDENCE, grayscale=True, region=region)) \
    #         + list(
    #             pyautogui.locateAllOnScreen(LOCKED2_CRUISER_PATH, confidence=CONFIDENCE, grayscale=True, region=region))

    return []


def select_to_shoot(target_icon, region):
    x, y, width, height = region
    if target_icon is not None:
        # Center of the target relative to the region
        target_center = pyautogui.center(target_icon)
        target_random = generate_random_offset(target_center)

        # Perform the action within the defined region
        if (
                x <= target_center[0] <= x + width
                and y <= target_center[1] <= y + height
        ):  # Check if the target is within the specified region
            with pyautogui.hold('ctrl'):
                pyautogui.sleep(2)  # Wait for a specified time
                pyautogui.move(target_random)  # Move to the target with offset
                pyautogui.click(
                    target_random,
                    clicks=random.randint(2, 2),
                    interval=random.uniform(0.2, 0.7),
                )


def click_center_of_region(region):
    """
    Click the center of a given region.

    :param region: Tuple (x, y, width, height) representing the region.
    """
    x, y, width, height = region
    center_x = random.randint((x + width // 2)-10, (x + width // 2)+10)
    center_y = random.randint((y + height // 2)-10, (y + height // 2)+10)

    # Perform the click at the center
    random.randint(2, 2),
    pyautogui.click(center_x, center_y, interval=random.uniform(0.2, 0.7))


def send_drones(region):
    click_center_of_region(region)
    print("Sending drones without target check.")
    pyautogui.press("f")


def get_unlock_icon(region):
    return pyautogui.locateOnScreen(UNLOCK_ICON, confidence=0.9, region=region)


def loop_running_two_acc_small_stuff(q=None, areas=None):
    pyautogui.FAILSAFE = False

    region_1 = tuple(map(int, areas[0]))
    region_2 = tuple(map(int, areas[1]))

    while True:
        print_message("Checking Frigs 1", q)
        if area_has_frigates(region_1):
            print_message("Found Frigs area 1", q)
            clear_targets(region_1, q)
        print_message("Checking Frigs 2", q)
        if area_has_frigates(region_2):
            print_message("Found Frigs area 2", q)
            clear_targets(region_2, q)
        print_message("Checking Cruisers 1", q)
        if area_has_cruisers(region_1):
            print_message("Found Cruisers area 1", q)
            clear_targets(region_1, q)
        print_message("Checking Cruisers 2", q)
        if area_has_cruisers(region_2):
            print_message("Found Cruisers area 2", q)
            clear_targets(region_2, q)
        time.sleep(3)


def clear_targets(region, q):
    control_locking = False
    if list_targets(region) and not control_locking and not list_selected_targets(region):
        while list_targets(region) > list_selected_targets(region) or not control_locking:
            print_message("There is targets: " + str(len(list_targets(region))), q)
            print_message("There is already locked: " + str(len(list_selected_targets(region))), q)
            for target in list_targets(region):
                count = 0
                select_to_shoot(target, region)
                while get_unlock_icon(region) is None and count <= 8:
                    print_message("Waiting for lock!!!!", q)
                    time.sleep(1)
                    count += 1
            time.sleep(1 / 2)
            control_locking = True
    if list_selected_targets(region):
        print_message("targets to clear", q)
        targets = list_selected_targets(region)
        press_f = True
        while list_selected_targets(region) == targets:
            if press_f:
                send_drones(region)
                press_f = False
            time.sleep(2)
            print_message("Waiting target die!", q)
