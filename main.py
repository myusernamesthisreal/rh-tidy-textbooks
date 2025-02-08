import pyautogui
import cv2
import time
import numpy
import win32api, win32con, win32gui
import mss


TEMPLATE_X_RES = 2560
TEMPLATE_Y_RES = 1600
def fast_click(x, y):
    win32api.SetCursorPos((x, y))
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0)

def main():
    TEMPLATE_PATH = "template.png"
    template = cv2.imread(TEMPLATE_PATH, cv2.IMREAD_GRAYSCALE)
    window = None
    if template is None:
        print("Error: Template image not found.")
        return
    try:
        window = pyautogui.getWindowsWithTitle("Roblox")[0]
        win32gui.SetForegroundWindow(window._hWnd)
    except IndexError:
        print("Roblox window not found.")
        return
    baseW, baseH, screenWidth, screenHeight = win32gui.GetWindowRect(window._hWnd)
    screenWidth = screenWidth - baseW
    screenHeight = screenHeight - baseH
    print(f"Detected screen resolution: {screenWidth}x{screenHeight}")
    print(f"Starting root: {baseW}x{baseH}")
    scaleX = screenWidth / TEMPLATE_X_RES
    scaleY = screenHeight / TEMPLATE_Y_RES
    template = cv2.resize(template, None, fx=scaleX, fy=scaleY)
    template_height, template_width = template.shape[:2]
    startXCoord = baseW + int((screenWidth - screenWidth * 0.55) / 2)
    gameWidth = int(screenWidth * 0.55)
    centerX = int(gameWidth / 2)
    lBound = gameWidth * 0.3 - 25
    rBound = gameWidth * 0.3 + 25
    bookHeight = round(screenHeight * 0.07)
    print(startXCoord, gameWidth, centerX, lBound, rBound, bookHeight)
    count = 0
    total = 0
    prev_val = 0
    click_x = round(baseW + screenWidth * 0.55)
    click_y = round(baseH + screenHeight / 2)
    win32api.SetCursorPos((click_x, click_y))
    time.sleep(1)
    win32api.SetCursorPos((click_x, click_y))
    print(f"Clicking at: {click_x}x{click_y}")
    inactive_timer = time.time()
    print("Starting...")
    time.sleep(1)
    with mss.mss() as sct:
        while True:
            loopStartTime = time.time()
            startHeight = baseH + (screenHeight - (count + 1) * bookHeight) - 3
            image = sct.grab({"top": startHeight, "left": startXCoord, "width": gameWidth, "height": bookHeight + 7})
            bgr = numpy.array(image)
            grayImage = cv2.cvtColor(bgr, cv2.COLOR_BGR2GRAY)
            result = cv2.matchTemplate(grayImage, template, cv2.TM_CCOEFF_NORMED)
            _, _, _, max_loc = cv2.minMaxLoc(result)
            # cv2.rectangle(grayImage, max_loc, (max_loc[0] + template_width, max_loc[1] + template_height), (0, 255, 0), 2)
            # cv2.imwrite("result" + str(total) + ".png", grayImage)
            if max_loc[0] > lBound and max_loc[0] < rBound and abs(max_loc[0] - prev_val) > 10:
                print("Time: " + str(time.time() - loopStartTime), max_loc, startHeight, count, total)
                fast_click(click_x, click_y)
                print("FOUND")
                count += 1
                total += 1
                inactive_timer = time.time()
                # top_left = max_loc
                # bottom_right = (top_left[0] + template_width, top_left[1] + template_height)
                # cv2.rectangle(grayImage, top_left, bottom_right, (0, 255, 0), 2)
                # plt.imsave("result" + str(total) + ".png", grayImage, cmap="gray")
                time.sleep(0.2)
            # cv2.imwrite("result" + str(total) + ".png", grayImage)
            # time.sleep(0.006)
            prev_val = max_loc[0]
            if count >= 13:
                count = 1
                time.sleep(2.5)

            if time.time() - inactive_timer > 10:
                break

if __name__ == "__main__":
    main()
