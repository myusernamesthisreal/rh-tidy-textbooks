import pyautogui
import cv2
import time
import numpy as np
import threading
import win32api, win32con
import mss


PHYSICS_TICK_TIME = 1 / 240  # 4.16ms
FRAME_PROCESSING_LIMIT = 0.04  # 4ms
# Global variables for multi-threading
screenWidth, screenHeight = pyautogui.size()
latest_frame = None
frame_lock = threading.Lock()
count = 0
latest_frame_time = 0

# Define the region of interest (ROI)
startXCoord = int((screenWidth - screenWidth * 0.55) / 2)
gameWidth = int(screenWidth * 0.55)

def fast_click(x, y):
    win32api.SetCursorPos((x, y))
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0)


def capture_screen():
    """
    Continuously captures the screen and updates latest_frame.
    """
    global latest_frame, latest_frame_time

    # Set dynamic ROI for book detection
    with mss.mss() as sct:
        while True:
            start_time = time.perf_counter()
            roi_top = screenHeight - 117 * (count + 1) - 5
            roi_bottom = screenHeight - 117 * count + 5
            region = (startXCoord, roi_top, startXCoord + gameWidth, roi_bottom)
            image = sct.grab(region)
            bgr = np.array(image)
            grayImage = cv2.cvtColor(bgr, cv2.COLOR_BGR2GRAY)
            del image
            with frame_lock:
                latest_frame = grayImage
                latest_frame_time = start_time
            del bgr
            del grayImage
            capture_time = time.perf_counter() - start_time
            if capture_time > FRAME_PROCESSING_LIMIT:
                print(f"Capture took too long: {capture_time:.3f}s, skipping next frame.")
            # time.sleep(0.0005)  # Capture at a fast rate

def detect_books(gray_image):
    """
    Detects book-like objects using contour analysis.
    Returns the x-coordinates of detected books.
    """
    blurred = cv2.GaussianBlur(gray_image, (5, 5), 0)
    edges = cv2.Canny(blurred, 50, 150)
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    book_positions = []
    for cnt in contours:
        x, y, w, h = cv2.boundingRect(cnt)
        aspect_ratio = w / float(h) if h != 0 else 0

        # Filtering based on size and shape
        if 100 < w < 210 and 100 < h < 120 and 1.5 < aspect_ratio < 2.0:
            book_positions.append((x, y, w, h))

    # Sort books from left to right based on x-coordinates
    book_positions.sort(key=lambda b: b[0])

    return book_positions[0] if book_positions else None

def process_game_logic():
    """
    Continuously processes game logic (detect books & click).
    """
    global latest_frame, latest_frame_time
    total = 0
    while True:
        loop_start = time.perf_counter()
        # Get the latest frame (thread-safe)
        with frame_lock:
            frame = latest_frame.copy() if latest_frame is not None else None
            frame_time = latest_frame_time
        loopStartTime = time.time()
        if (loop_start - frame_time) > FRAME_PROCESSING_LIMIT:
            print(f"⏩ Skipped old frame ({loop_start - frame_time:.6f}s delay).")
            continue
        if frame is not None:
            book_positions = detect_books(frame)
            processing_time = time.perf_counter() - loop_start

            if book_positions and processing_time < FRAME_PROCESSING_LIMIT:
                book_x = book_positions[0]

                # If books are aligned, click
                if 400 < book_x < 450:
                    print("Loop Time: {:.3f}s".format(time.time() - loopStartTime))
                    fast_click(1700, 1440)
                    print(total, "Click: Books Aligned", book_positions)
                    global count
                    count += 1
                    total += 1
                    with frame_lock:
                        del latest_frame
                    time.sleep(0.3)

        if count >= 13:
            count = 1
            time.sleep(2)

def main():
    # Activate and maximize the game window
    window = pyautogui.getWindowsWithTitle("Roblox")[0]
    window.activate()
    time.sleep(1)

    # Start screen capture in a separate thread
    capture_thread = threading.Thread(target=capture_screen, daemon=True)
    capture_thread.start()

    # Start game logic processing in the main thread
    process_game_logic()

if __name__ == "__main__":
    main()
