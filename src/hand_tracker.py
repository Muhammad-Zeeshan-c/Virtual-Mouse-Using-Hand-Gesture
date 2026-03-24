import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
import cv2
import os

class HandTracker:
    """
    A class used to track hand landmarks using MediaPipe Tasks API.
    """
    def __init__(self, mode=False, max_hands=1, detection_con=0.5, track_con=0.5):
        """
        Initializes the MediaPipe HandLandmarker module.
        """
        model_path = os.path.join(os.path.dirname(__file__), 'hand_landmarker.task')
        
        base_options = python.BaseOptions(model_asset_path=model_path)
        options = vision.HandLandmarkerOptions(
            base_options=base_options,
            running_mode=vision.RunningMode.IMAGE,
            num_hands=max_hands,
            min_hand_detection_confidence=detection_con,
            min_hand_presence_confidence=detection_con,
            min_tracking_confidence=track_con
        )
        self.detector = vision.HandLandmarker.create_from_options(options)
        self.results = None

    def find_hands(self, img, draw=True):
        """
        Detects hands in an image and provides results.
        """
        # Convert BGR image to RGB for MediaPipe
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=img_rgb)
        
        # Perform detection
        self.results = self.detector.detect(mp_image)

        if draw and self.results.hand_landmarks:
            # Drawing landmarks manually since solutions.drawing_utils is missing in this env
            for hand_landmarks in self.results.hand_landmarks:
                for lm in hand_landmarks:
                    h, w, c = img.shape
                    cx, cy = int(lm.x * w), int(lm.y * h)
                    cv2.circle(img, (cx, cy), 3, (0, 255, 0), cv2.FILLED)
            
        return img

    def get_landmarks(self, img, hand_no=0):
        """
        Extracts landmark coordinates (x, y) for a specific hand.
        """
        lm_list = []
        if self.results and self.results.hand_landmarks:
            if len(self.results.hand_landmarks) > hand_no:
                hand_lms = self.results.hand_landmarks[hand_no]
                h, w, c = img.shape
                for id, lm in enumerate(hand_lms):
                    # Convert normalized coordinates to pixel coordinates
                    cx, cy = int(lm.x * w), int(lm.y * h)
                    lm_list.append([id, cx, cy])
        return lm_list

    def get_hand_type(self, hand_no=0):
        """
        Returns whether the detected hand is Left or Right.
        """
        if self.results and self.results.handedness:
            if len(self.results.handedness) > hand_no:
                # New API returns handedness as a list of lists
                return self.results.handedness[hand_no][0].category_name
        return None
