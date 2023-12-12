import time
from pynput.mouse import Button, Controller


class Mouse:
    def __init__(self, controller=None, primary_mouse="left", interaction="press"):
        self.mouse = Controller() if not controller else controller
        self.button = Button.right if primary_mouse == "right" else Button.left
        self.hold_click = 0.15 if interaction == "press" else 0.5

    def click(self, wait_start=0, wait_end=0, times=1, hold_time=0.15):
        try:
            time.sleep(wait_start)
            for i in range(times):
                self.mouse.press(self.button)
                sleep_time = self.hold_click + hold_time
                time.sleep(sleep_time)
                self.mouse.release(self.button)
            time.sleep(wait_end)
        except Exception as err:
            print(f"click error: {err}")

    def move_to(self, x=0, y=0, wait_end=0):
        try:
            self.mouse.position = (x, y)
            time.sleep(wait_end)
        except Exception as err:
            print(f"move_to error: {err}")

    def wait_level_cleared(self):
        self.click(wait_start=1, wait_end=2, times=3)

    def click_prestige(self):
        self.move_to()
        self.click(wait_end=4, hold_time=1.5)
        self.click(times=2)
        self.move_to(wait_end=0)

    def click_origin(self, num_nodes):
        wait_end = 2 + num_nodes / 13
        self.click(wait_end=wait_end)
        self.click(times=2, hold_time=0.5)
        self.click()
        self.move_to(wait_end=2)
