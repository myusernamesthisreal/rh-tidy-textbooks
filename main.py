import pyautogui
import cv2
import time
import numpy
import win32api, win32con
import mss

def fast_click(x, y):
    win32api.SetCursorPos((x, y))
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0)


def main():
    startTime = time.time()
    TEMPLATE_PATH = "template.png"
    template = cv2.imread(TEMPLATE_PATH, cv2.IMREAD_GRAYSCALE)
    template_height, template_width = template.shape[:2]
    screenWidth, screenHeight = pyautogui.size()
    print(screenWidth, screenHeight)
    window = pyautogui.getWindowsWithTitle("Roblox")[0]
    window.activate()
    time.sleep(1)
    startXCoord = int((screenWidth - screenWidth * 0.55) / 2)
    gameWidth = int(screenWidth * 0.55)
    centerX = int(gameWidth / 2)
    lBound = 400
    rBound = 450
    print(startXCoord, gameWidth, centerX, lBound, rBound)
    count = 0
    total = 0
    prev_val = 0
    with mss.mss() as sct:
        while True:
            loopStartTime = time.time()
            startHeight = screenHeight - (count + 1) * 117
            image = sct.grab({"top": startHeight, "left": startXCoord, "width": gameWidth, "height": 117})
            bgr = numpy.array(image)
            grayImage = cv2.cvtColor(bgr, cv2.COLOR_BGR2GRAY)
            result = cv2.matchTemplate(grayImage, template, cv2.TM_CCOEFF_NORMED)
            _, _, _, max_loc = cv2.minMaxLoc(result)

            if max_loc[0] > lBound and max_loc[0] < rBound and abs(max_loc[0] - prev_val) > 10:
                print("Time: " + str(time.time() - loopStartTime), max_loc, startHeight, count, total)
                fast_click(1700, 1000)
                print("FOUND")
                count += 1
                total += 1
                # image.save("image" + str(total) + ".png", "PNG")
                # top_left = max_loc
                # bottom_right = (top_left[0] + template_width, top_left[1] + template_height)
                # cv2.rectangle(grayImage, top_left, bottom_right, (0, 255, 0), 2)
                # plt.imsave("result" + str(total) + ".png", grayImage, cmap="gray")
                time.sleep(0.2)
            # time.sleep(0.006)
            prev_val = max_loc[0]
            if count >= 13:
                count = 1
                time.sleep(2.5)

            if total >= 80:
                break
    print("Runtime", time.time() - startTime)

if __name__ == "__main__":
    main()
