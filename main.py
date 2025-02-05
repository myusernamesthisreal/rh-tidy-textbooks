import pyautogui
import cv2
import time
import numpy
import matplotlib.pyplot as plt
from PIL import ImageGrab

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
    window.maximize()
    time.sleep(1)
    startXCoord = int((screenWidth - screenWidth * 0.55) / 2)
    gameWidth = int(screenWidth * 0.55)
    centerX = int(gameWidth / 2)
    lBound = centerX - 300
    rBound = centerX - 265
    print(startXCoord, gameWidth, centerX, lBound, rBound)
    count = 0
    total = 0
    prev_val = 0
    while True:
        loopStartTime = time.time()
        startHeight = screenHeight - (count + 1) * 117
        image = ImageGrab.grab((startXCoord, startHeight, startXCoord +gameWidth, startHeight + 117))
        grayImage = grayImage = numpy.array(image.convert('L'))
        result = cv2.matchTemplate(grayImage, template, cv2.TM_CCOEFF_NORMED)
        _, _, _, max_loc = cv2.minMaxLoc(result)
        print("Time: " + str(time.time() - loopStartTime), max_loc, startHeight, count, total)
        if max_loc[0] > lBound and max_loc[0] < rBound and abs(max_loc[0] - prev_val) > 10:
            pyautogui.click(1700, 1000)
            print("FOUND")
            count += 1
            total += 1
            # image.save("image" + str(total) + ".png", "PNG")
            # top_left = max_loc
            # bottom_right = (top_left[0] + template_width, top_left[1] + template_height)
            # cv2.rectangle(grayImage, top_left, bottom_right, (0, 255, 0), 2)
            # plt.imsave("result" + str(total) + ".png", grayImage, cmap="gray")
            time.sleep(1)
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
