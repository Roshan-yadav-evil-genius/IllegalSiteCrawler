import time
import math
import pyautogui

def move_mouse_in_circle(radius=100, speed=5):
    """
    Move the mouse in a continuous circle.

    :param radius: Radius of the circle.
    :param speed: Time delay between each mouse move in seconds. Smaller values result in faster movement.
    """
    center_x, center_y = pyautogui.position()
    time.sleep(10)
    while True:
        for angle in range(0, 360):
            radians = math.radians(angle)
            x = center_x + radius * math.cos(radians)
            y = center_y + radius * math.sin(radians)
            pyautogui.moveTo(x, y)
            time.sleep(speed)

try:
    move_mouse_in_circle()
except KeyboardInterrupt:
    print("Mouse movement stopped.")
