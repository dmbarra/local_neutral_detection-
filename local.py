import os
import time
import pyautogui
from playsound import playsound
import multiprocessing

NEUTRAL_PATH = 'imgs\\neutral.png'
ORANGE_PATH = 'imgs\\orange.png'
LOCAL_NEXT = 'imgs\\5BTK-M.png'


def should_i_play_alarm():
    return get_the_neutral() is not None or get_the_orange() is not None


def should_i_play_closer_threat():
    return get_closer_local() is not None


def get_the_neutral():
    return pyautogui.locateOnScreen(NEUTRAL_PATH, confidence=0.8)


def get_the_orange():
    return pyautogui.locateOnScreen(ORANGE_PATH, confidence=0.8)


def get_closer_local():
    return pyautogui.locateOnScreen(LOCAL_NEXT, confidence=0.8)


def play_alarm():
    audio_file = os.path.dirname(__file__) + '\\sound\\alarm1.mp3'
    p = multiprocessing.Process(target=playsound, args=(audio_file,))
    p.start()
    return p


def play_threat():
    audio_file = os.path.dirname(__file__) + '\\sound\\next_system.mp3'
    p = multiprocessing.Process(target=playsound, args=(audio_file,))
    p.start()
    return p


def stop_playing(play):
    play.terminate()


def start_caos():
    play = play_alarm()
    time.sleep(6)
    stop_playing(play)


def start_threat():
    return play_threat(), True


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
        time.sleep(1)

        print("waiting!!!!")
