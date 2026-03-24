import math

class GestureLogic:
    """
    Gesture recognition engine using a 'closest-finger-wins' approach.
    Each gesture is mapped to a unique thumb-to-finger pairing,
    so only ONE gesture can fire at a time.
    """
    def __init__(self):
        # Landmark IDs
        self.THUMB_TIP = 4
        self.INDEX_TIP = 8
        self.MIDDLE_TIP = 12
        self.RING_TIP = 16
        self.PINKY_TIP = 20
        # MCP (knuckle) joints for fist detection
        self.tip_ids = [4, 8, 12, 16, 20]
        self.mcp_ids = [2, 5, 9, 13, 17]

    def _distance(self, p1, p2, lm_list):
        """Euclidean distance between two landmarks."""
        x1, y1 = lm_list[p1][1], lm_list[p1][2]
        x2, y2 = lm_list[p2][1], lm_list[p2][2]
        return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)

    def _all_fingers_down(self, lm_list):
        """Returns True if ALL five fingers are folded into a fist."""
        for i in range(5):
            tip_y = lm_list[self.tip_ids[i]][2]
            mcp_y = lm_list[self.mcp_ids[i]][2]
            if i == 0:
                # Thumb: horizontal closeness to palm
                if abs(lm_list[self.tip_ids[i]][1] - lm_list[self.mcp_ids[i]][1]) > 40:
                    return False
            else:
                # Other fingers: tip must be at or below knuckle
                if tip_y < mcp_y - 10:
                    return False
        return True

    def detect_gesture(self, lm_list, hand_type="Right"):
        """
        Detects the active gesture. Returns one of:
          'PINCH_INDEX'  → Thumb + Index are closest (used for MOVE / LEFT_CLICK)
          'RIGHT_CLICK'  → Thumb + Middle touching
          'SCROLL'       → Thumb + Pinky touching
          'DRAG'         → Full fist
          'NONE'         → No recognized gesture

        The 'closest-finger-wins' rule ensures only ONE gesture fires.
        """
        if not lm_list:
            return "NONE"

        # --- 1. DRAG: Full fist (highest priority) ---
        if self._all_fingers_down(lm_list):
            return "DRAG"

        # --- 2. Calculate thumb-to-finger distances ---
        dist_index = self._distance(self.THUMB_TIP, self.INDEX_TIP, lm_list)
        dist_middle = self._distance(self.THUMB_TIP, self.MIDDLE_TIP, lm_list)
        dist_pinky = self._distance(self.THUMB_TIP, self.PINKY_TIP, lm_list)

        TOUCH_THRESHOLD = 50  # Max distance to count as "touching"

        # --- 3. Find the closest finger to the thumb ---
        # Only consider fingers that are within the touch threshold
        candidates = {}
        if dist_index < TOUCH_THRESHOLD:
            candidates['PINCH_INDEX'] = dist_index
        if dist_middle < TOUCH_THRESHOLD:
            candidates['RIGHT_CLICK'] = dist_middle
        if dist_pinky < TOUCH_THRESHOLD:
            candidates['SCROLL'] = dist_pinky

        # No finger is touching the thumb
        if not candidates:
            return "NONE"

        # The gesture with the SMALLEST distance wins
        winner = min(candidates, key=candidates.get)
        return winner
