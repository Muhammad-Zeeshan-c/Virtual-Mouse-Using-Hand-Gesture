import cv2
import time
import threading
from hand_tracker import HandTracker
from gesture_logic import GestureLogic
from mouse_controller import MouseController
from server import server_instance, start_server

def main():
    # 0. Start API Server in background
    threading.Thread(target=start_server, daemon=True).start()

    # 1. Initialize Webcam (search for available camera)
    w_cam, h_cam = 640, 480
    cap = None
    for i in range(5):
        print(f"Trying camera index {i}...")
        cap = cv2.VideoCapture(i, cv2.CAP_DSHOW)
        if cap.isOpened():
            print(f"Successfully opened camera {i}")
            break
    
    if cap is None or not cap.isOpened():
        print("Error: Could not open any webcam (tried indices 0-4).")
        return

    cap.set(cv2.CAP_PROP_FRAME_WIDTH, w_cam)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, h_cam)
    
    # 2. Initialize Core Modules
    tracker = HandTracker(max_hands=1, detection_con=0.5, track_con=0.5)
    logic = GestureLogic()
    mouse = MouseController(w_cam, h_cam, frame_reduction=100, smoothing=5)
    
    prev_time = 0

    # Click debouncing
    last_click_time = 0
    click_delay = 0.4  # seconds between clicks

    # State machine for MOVE vs LEFT_CLICK
    pinch_active = False       # Is index+thumb currently pinched?
    pinch_start_time = 0       # When did the pinch start?
    pinch_moved = False        # Did the cursor move significantly during pinch?
    pinch_start_pos = (0, 0)   # Starting cursor position when pinch began
    MOVE_DISTANCE_THRESHOLD = 30  # Pixels of movement to count as "intentional move"
    TAP_TIME_THRESHOLD = 0.35    # Max duration (seconds) for a tap to count as click

    # Window name constant
    WINDOW_NAME = "Virtual Mouse Feed"

    print("AI Virtual Mouse Started...")
    print("API Server running at http://127.0.0.1:8000")
    print("Press 'q' or close the window to exit.")

    while True:
        # A. Sync Settings from Server
        mouse.smoothing = server_instance.settings["smoothing"]
        mouse.frame_reduction = 150 - (server_instance.settings["sensitivity"] * 10)

        # B. Read frame
        success, img = cap.read()
        if not success:
            break
            
        # C. Find hands and extract landmarks
        img = tracker.find_hands(img, draw=True)
        lm_list = tracker.get_landmarks(img)
        hand_type = tracker.get_hand_type()
        
        server_instance.status["hand_detected"] = len(lm_list) > 0

        # D. Process gestures when hand is detected
        if len(lm_list) != 0:
            gesture = logic.detect_gesture(lm_list, hand_type)
            
            # Extract Index finger tip coordinates (landmark ID: 8)
            x1, y1 = lm_list[8][1], lm_list[8][2]
            settings = server_instance.settings

            # ==============================
            # DRAG: Fist detected
            # ==============================
            if gesture == "DRAG" and settings["enableDrag"]:
                mouse.start_drag()
                mouse.move(x1, y1)
                server_instance.status["gesture"] = "DRAG"
                cv2.putText(img, "DRAG", (20, 50), cv2.FONT_HERSHEY_PLAIN, 3, (255, 255, 0), 3)
                pinch_active = False  # Reset pinch state
            else:
                mouse.end_drag()

            # ==============================
            # RIGHT CLICK: Thumb + Middle
            # ==============================
            if gesture == "RIGHT_CLICK" and settings["enableRightClick"]:
                if (time.time() - last_click_time) > click_delay:
                    mouse.click('right')
                    last_click_time = time.time()
                    server_instance.status["gesture"] = "RIGHT_CLICK"
                    cv2.putText(img, "RIGHT CLICK", (20, 50), cv2.FONT_HERSHEY_PLAIN, 3, (0, 0, 255), 3)
                pinch_active = False

            # ==============================
            # SCROLL: Thumb + Pinky
            # ==============================
            elif gesture == "SCROLL" and settings["enableScroll"]:
                y_pinky = lm_list[20][2]
                y_base = lm_list[0][2]
                if y_pinky < y_base - 100:
                    mouse.scroll('up')
                elif y_pinky > y_base - 60:
                    mouse.scroll('down')
                server_instance.status["gesture"] = "SCROLL"
                cv2.putText(img, "SCROLL", (20, 50), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)
                pinch_active = False

            # ==============================
            # PINCH_INDEX: Thumb + Index → MOVE or LEFT_CLICK
            # State machine differentiates hold (MOVE) vs tap (LEFT_CLICK)
            # ==============================
            elif gesture == "PINCH_INDEX":
                if not pinch_active:
                    # Pinch just started
                    pinch_active = True
                    pinch_start_time = time.time()
                    pinch_moved = False
                    pinch_start_pos = (x1, y1)
                else:
                    # Pinch is being held → check if user moved their hand
                    dx = abs(x1 - pinch_start_pos[0])
                    dy = abs(y1 - pinch_start_pos[1])
                    if dx > MOVE_DISTANCE_THRESHOLD or dy > MOVE_DISTANCE_THRESHOLD:
                        pinch_moved = True

                # Always move the cursor while pinching (smooth experience)
                if settings["enableMove"]:
                    mouse.move(x1, y1)
                
                server_instance.status["gesture"] = "MOVE"
                cv2.putText(img, "MOVE", (20, 50), cv2.FONT_HERSHEY_PLAIN, 3, (0, 255, 0), 3)

            # ==============================
            # NONE / Release: No active gesture
            # ==============================
            else:
                # Check if pinch was just released → potential LEFT_CLICK
                if pinch_active:
                    pinch_duration = time.time() - pinch_start_time
                    pinch_active = False

                    # LEFT_CLICK: short tap AND user didn't move much
                    if pinch_duration < TAP_TIME_THRESHOLD and not pinch_moved:
                        if settings["enableClick"] and (time.time() - last_click_time) > click_delay:
                            mouse.click('left')
                            last_click_time = time.time()
                            server_instance.status["gesture"] = "LEFT_CLICK"
                            cv2.putText(img, "LEFT CLICK", (20, 50), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)
                    else:
                        server_instance.status["gesture"] = "NONE"
                else:
                    server_instance.status["gesture"] = "NONE"
        else:
            # No hand detected → reset all states
            server_instance.status["gesture"] = "NONE"
            server_instance.status["hand_detected"] = False
            pinch_active = False
            mouse.end_drag()

        # E. FPS Calculation
        curr_time = time.time()
        fps = 1 / (curr_time - prev_time) if (curr_time - prev_time) > 0 else 0
        prev_time = curr_time
        server_instance.status["fps"] = int(fps)

        cv2.putText(img, f"FPS: {int(fps)}", (w_cam - 150, 50), cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 255), 2)
        
        # F. Show feed
        cv2.imshow(WINDOW_NAME, img)
        
        # G. Exit: Press 'q' OR close the window via the X button
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            print("Exiting: 'q' key pressed.")
            break
        if cv2.getWindowProperty(WINDOW_NAME, cv2.WND_PROP_VISIBLE) < 1:
            print("Exiting: Window closed.")
            break

    # Cleanup
    mouse.end_drag()
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
