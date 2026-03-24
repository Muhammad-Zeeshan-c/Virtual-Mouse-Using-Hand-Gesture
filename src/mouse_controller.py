import pyautogui
import numpy as np
import time

class MouseController:
    """
    Controls the system mouse cursor with smoothing and boundary mapping.
    """
    def __init__(self, w_cam, h_cam, frame_reduction=100, smoothing=5):
        self.w_cam = w_cam
        self.h_cam = h_cam
        self.frame_reduction = frame_reduction # Padding from camera edges
        self.smoothing = smoothing # High value = smoother but more lag
        
        # Screen resolution
        self.w_screen, self.h_screen = pyautogui.size()
        pyautogui.FAILSAFE = False # Disable failsafe for virtual mouse use
        
        # Previous and current coordinates for smoothing
        self.prev_x, self.prev_y = 0, 0
        self.curr_x, self.curr_y = 0, 0

        # Click state to prevent rapid repetitive clicks
        self.clicked = False

    def move(self, x, y):
        """
        Maps camera coordinates to screen resolution and moves cursor.
        """
        # 1. Coordinate Mapping
        x_mapped = np.interp(x, (self.frame_reduction, self.w_cam - self.frame_reduction), (0, self.w_screen))
        y_mapped = np.interp(y, (self.frame_reduction, self.h_cam - self.frame_reduction), (0, self.h_screen))
        
        # 2. Smoothing
        self.curr_x = self.prev_x + (x_mapped - self.prev_x) / self.smoothing
        self.curr_y = self.prev_y + (y_mapped - self.prev_y) / self.smoothing
        
        # 3. Move Mouse (Flip X)
        pyautogui.moveTo(self.w_screen - self.curr_x, self.curr_y, _pause=False)
        self.prev_x, self.prev_y = self.curr_x, self.curr_y

    def click(self, button='left'):
        pyautogui.click(button=button)

    def start_drag(self):
        """Presses the mouse button down to begin a drag."""
        if not self.clicked:
            pyautogui.mouseDown(button='left')
            self.clicked = True

    def end_drag(self):
        """Releases the mouse button to complete a drag."""
        if self.clicked:
            pyautogui.mouseUp(button='left')
            self.clicked = False

    def scroll(self, direction):
        val = 150 if direction == 'up' else -150
        pyautogui.scroll(val)
