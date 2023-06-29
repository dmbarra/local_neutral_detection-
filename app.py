import multiprocessing
from queue import Empty
from tkinter import Tk, Button, Frame, LEFT, Text, BOTH, TOP, BOTTOM, DISABLED, NORMAL


class GuiApp(object):
    def __init__(self, q):
        self.multiprocess = None
        self.pressed = False
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
        self.button4 = Button(self.button_frame, text="carrier", command=self.run_carrier)
        self.button4.pack(side=LEFT, padx=2)

        self.text_frame = Frame(self.window, width=250, height=160)
        self.text_frame.pack(side=TOP, pady=2)
        self.text_wid = Text(self.text_frame, height=50, width=50)
        self.text_wid.pack(expand=0, fill=BOTH)

        self.window.after(100, self.check_queue_poll, q)

    def run_process(self, target, args):
        p = multiprocessing.Process(target=target, args=args)
        p.start()

    def kill_all_process(self):
        for p in multiprocessing.active_children():
            p.terminate()
        # self.multiprocess.terminate()

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
            from local import loop_running_local
            self.run_process(target=loop_running_local, args=(q,))
            self.window.title("Running Local Script")
            self.button1.config(text="STOP")
            self.pressed = True
            self.button2.config(state=DISABLED)
            self.button3.config(state=DISABLED)
            self.button4.config(state=DISABLED)
        else:
            self.button1.config(text="Local")
            self.kill_all_process()
            self.pressed = False
            self.button2.config(state=NORMAL)
            self.button3.config(state=NORMAL)
            self.button4.config(state=NORMAL)
            self.window.title("Wait!!")

    def run_small_script(self):
        if not self.pressed:
            from local import loop_running_local
            self.run_process(target=loop_running_local, args=(q,))
            from small_stuff import loop_running_small_stuff
            self.run_process(target=loop_running_small_stuff, args=(q,))
            self.window.title("Running Small Script")
            self.button2.config(text="STOP")
            self.pressed = True
            self.button1.config(state=DISABLED)
            self.button3.config(state=DISABLED)
            self.button4.config(state=DISABLED)
        else:
            self.button2.config(text="small")
            self.kill_all_process()
            self.pressed = False
            self.button1.config(state=NORMAL)
            self.button3.config(state=NORMAL)
            self.button4.config(state=NORMAL)
            self.window.title("Wait!!")

    def run_warp_script(self):
        if not self.pressed:
            from warp_zero import loop_running_warp
            self.run_process(target=loop_running_warp, args=(q,))
            self.button3.config(text="STOP")
            self.window.title("Running Warp Script")
            self.pressed = True
            self.button1.config(state=DISABLED)
            self.button2.config(state=DISABLED)
            self.button4.config(state=DISABLED)
        else:
            self.button3.config(text="warp")
            self.multiprocess.terminate()
            self.pressed = False
            self.button1.config(state=NORMAL)
            self.button2.config(state=NORMAL)
            self.button4.config(state=NORMAL)
            self.window.title("Wait!!")

    def run_carrier(self):
        if not self.pressed:
            from local import loop_running_local
            self.run_process(target=loop_running_local, args=(q,))
            from bigger_more import loop_running_by_carrier
            self.run_process(target=loop_running_by_carrier, args=(q,))
            from bigger_more import protect_carrier
            self.run_process(target=protect_carrier, args=(q,))
            self.window.title("Running Carrier")
            self.button4.config(text="STOP")
            self.pressed = True
            self.button1.config(state=DISABLED)
            self.button2.config(state=DISABLED)
            self.button3.config(state=DISABLED)
        else:
            self.button4.config(text="carrier")
            self.kill_all_process()
            self.pressed = False
            self.button1.config(state=NORMAL)
            self.button2.config(state=NORMAL)
            self.button3.config(state=NORMAL)
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
