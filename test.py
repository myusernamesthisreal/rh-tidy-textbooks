import pyautogui
import cv2
import time
import numpy as np
from PIL import ImageGrab
import win32api, win32con
import mss

def fast_click(x, y):
    win32api.SetCursorPos((x, y))
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0)
def detect_books(gray_image):
    """
    Detects book-like objects using contour analysis.
    Returns the x-coordinates of detected books.
    """
    blurred = cv2.GaussianBlur(gray_image, (5, 5), 0)
    edges = cv2.Canny(blurred, 50, 150)
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # save debug image
    # cv2.imwrite("debug.png", edges)
    # print(contours)
    book_positions = []
    for cnt in contours:
        x, y, w, h = cv2.boundingRect(cnt)
        aspect_ratio = w / float(h) if h != 0 else 0
        # save a debug image
        # cv2.rectangle(gray_image, (x, y), (x + w, y + h), (0, 255, 0), 2)
        # cv2.imwrite("debug2.png", gray_image)
        # Filtering based on size and shape
        if 100 < w < 210 and 100 < h < 120 and 1.2 < aspect_ratio < 2.0:
            book_positions.append((x, y, w, h))

    # Sort books from left to right based on x-coordinates
    book_positions.sort(key=lambda b: b[0])

    if len(book_positions) > 0:
        # print("First", book_positions[0], "Last", book_positions[-1])
        return book_positions[0]

    return None

def main():
    # startTime = time.time()
    screenWidth, screenHeight = pyautogui.size()

    # Activate and maximize the game window
    window = pyautogui.getWindowsWithTitle("Roblox")[0]
    window.activate()
    time.sleep(1)

    # Define ROI based on image: Focus on the bottom area where the books appear
    startXCoord = int((screenWidth - screenWidth * 0.55) / 2)
    gameWidth = int(screenWidth * 0.55)

    count = 0
    total = 0
    with mss.mss() as sct:
        while True:
            loopStartTime = time.time()
            roi_top = screenHeight - 117 * (count + 1) - 5
            roi_bottom = screenHeight - 117 * count + 5

            # Capture only the region where the books appear
            image = sct.grab({"top": roi_top, "left": startXCoord, "width": gameWidth, "height": roi_bottom - roi_top})
            bgr = np.array(image)
            grayImage = cv2.cvtColor(bgr, cv2.COLOR_BGR2GRAY)

            # convert to opencv2

            # cv2.imwrite("debug" + str(total) + ".png", grayImage)
            book_positions = detect_books(grayImage)
            print(total, book_positions)
            if book_positions:
                book_coords = book_positions

                # If the books have similar x-coordinates, click
                if book_coords[0] > 400 and book_coords[0] < 450:
                    fast_click(1920, 1440)
                    print(total, "Click: Books Aligned", book_coords)
                    # cv2.rectangle(grayImage, (book_coords[0], book_coords[1], book_coords[2], book_coords[3]), (0,0,255), 5)
                    # cv2.imwrite("debugSuccess" + str(total) + ".png", grayImage)
                    count += 1
                    total += 1
                    time.sleep(0.5)

                    print("Loop Time: {:.3f}s".format(time.time() - loopStartTime), total + 1)
            if count >= 13:
                count = 1
                time.sleep(2)


if __name__ == "__main__":
    main()
