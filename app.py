import multiprocessing
from datetime import datetime
from queue import Empty, Full
import time
from tkinter import Tk, Button, Frame, LEFT, Text, BOTH, TOP, BOTTOM, Scrollbar, DISABLED, NORMAL


class GuiApp(object):
    def __init__(self, q):
        self.window = Tk()
        self.window.geometry("250x200")
        self.window.title("Waiting!!")

        self.button_frame = Frame(self.window, width=250, height=160)
        self.button_frame.pack(side=BOTTOM, pady=2)
        self.button1 = Button(self.button_frame, text="Local", command=self.run_local_script)
        self.button1.pack(side=LEFT, padx=2)
        self.button2 = Button(self.button_frame, text="small", command=self.run_small_script)
        self.button2.pack(side=LEFT, padx=2)
        self.button3 = Button(self.button_frame, text="warp", command=self.run_warp_script)
        self.button3.pack(side=LEFT, padx=2)

        self.pressed = False
        from local import loop_running_local
        self.run_local = multiprocessing.Process(target=loop_running_local, args=(q,))
        from small_stuff import loop_running_small_stuff
        self.run_small = multiprocessing.Process(target=loop_running_small_stuff, args=(q,))
        from warp_zero import loop_running_warp
        self.run_warp = multiprocessing.Process(target=loop_running_warp, args=(q,))

        self.text_frame = Frame(self.window, width=250, height=160)
        self.text_frame.pack(side=TOP, pady=2)
        self.text_wid = Text(self.text_frame, height=50, width=50)
        self.text_wid.pack(expand=0, fill=BOTH)

        self.scroll = Scrollbar(self.window, orient="vertical", command=self.text_wid.yview)
        self.text_wid.configure(yscrollcommand=self.scroll.set)
        self.scroll.pack(side="right", fill="y")

        self.window.after(100, self.check_queue_poll, q)

    def check_queue_poll(self, c_queue):
        try:
            str = c_queue.get(0)
            self.text_wid.insert('end', " ---> " + str + "\n")
            self.text_wid.see("end")
        except Empty:
            pass
        finally:
            self.window.after(100, self.check_queue_poll, c_queue)

    def run_local_script(self):
        if not self.pressed:
            self.run_local.start()
            self.window.title("Running Local Script")
            self.button1.config(text="STOP")
            self.pressed = True
            self.button2.config(state=DISABLED)
            self.button3.config(state=DISABLED)
        else:
            self.button1.config(text="Local")
            self.run_local.terminate()
            self.pressed = False
            self.button2.config(state=NORMAL)
            self.button3.config(state=NORMAL)
            self.window.title("Wait!!")

    def run_small_script(self):
        if not self.pressed:
            self.run_small.start()
            self.window.title("Running Small Script")
            self.button2.config(text="STOP")
            self.pressed = True
            self.button1.config(state=DISABLED)
            self.button3.config(state=DISABLED)
        else:
            self.button2.config(text="small")
            self.run_small.terminate()
            self.pressed = False
            self.button1.config(state=NORMAL)
            self.button3.config(state=NORMAL)
            self.window.title("Wait!!")

    def run_warp_script(self):
        if not self.pressed:
            self.run_warp.start()
            self.button3.config(text="STOP")
            self.window.title("Running Warp Script")
            self.pressed = True
            self.button1.config(state=DISABLED)
            self.button2.config(state=DISABLED)
        else:
            self.button3.config(text="warp")
            self.run_warp.terminate()
            self.pressed = False
            self.button1.config(state=NORMAL)
            self.button2.config(state=NORMAL)
            self.window.title("Wait!!")


def print_message(message, q):
    if q is not None:
        q.put(message)
    print(message)


if __name__ == '__main__':
    q = multiprocessing.Queue()
    q.cancel_join_thread()
    gui = GuiApp(q)
    gui.window.mainloop()
