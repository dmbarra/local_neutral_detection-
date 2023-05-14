import os
import time
import pyautogui
from playsound import playsound
import multiprocessing

NEUTRAL_PATH = 'imgs\\neutral.png'
ORANGE_PATH = 'imgs\\orange.png'


def should_i_play_alarm():
    # im2 = pyautogui.screenshot('partial.png', region=(0, 0, 500, 1080))
    return get_the_neutral() is not None or get_the_orange() is not None


def get_the_neutral():
    # im2 = pyautogui.screenshot('partial.png', region=(0, 0, 500, 1080))
    return pyautogui.locateOnScreen(NEUTRAL_PATH, confidence=0.8)


def get_the_orange():
    return pyautogui.locateOnScreen(ORANGE_PATH, confidence=0.8)


def play_alarm():
    audio_file = os.path.dirname(__file__) + '\\sound\\alarm1.mp3'
    p = multiprocessing.Process(target=playsound, args=(audio_file,))
    p.start()
    return p


def stop_alarm(play):
    play.terminate()


def start_caos():
    play = play_alarm()
    time.sleep(6)
    stop_alarm(play)


if __name__ == '__main__':
    while True:
        if should_i_play_alarm():
            print("NEUTRO!!!!")
            start_caos()
        time.sleep(1)

        print("waiting!!!!")
