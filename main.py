import time

import pyautogui
from time import sleep
from playsound import playsound


def get_the_neutral():
    # im2 = pyautogui.screenshot('partial.png', region=(0, 0, 500, 1080))
    return pyautogui.locateOnScreen('neutral.png', confidence=0.8)


def get_the_orange():
    return pyautogui.locateOnScreen('orange.png', confidence=0.8)


def play_alarm():
    playsound('alarm1.mp3')


if __name__ == '__main__':
    while True:
        if (get_the_neutral() is not None):
            play_alarm()
        if (get_the_orange() is not None):
            play_alarm()
        time.sleep(1/2)
        print("waiting!!!!")
