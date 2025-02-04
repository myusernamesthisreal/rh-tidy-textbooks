import pyautogui
import cv2
import time
import numpy
import matplotlib.pyplot as plt

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
    startXCoord = int((screenWidth - screenWidth * 0.56) / 2)
    gameWidth = int(screenWidth * 0.55)
    centerX = int(gameWidth / 2)
    lBound = centerX - 290
    rBound = centerX - 258
    print(startXCoord, gameWidth, centerX, lBound, rBound)
    count = 0
    total = 0
    prev_val = 0
    while True:
        loopStartTime = time.time()
        startHeight = screenHeight - (count + 1) * 121
        image = pyautogui.screenshot(region=(startXCoord, startHeight, gameWidth, 155))
        grayImage = cv2.cvtColor(numpy.array(image), cv2.COLOR_BGR2GRAY)
        result = cv2.matchTemplate(grayImage, template, cv2.TM_CCOEFF_NORMED)
        _, max_val, _, max_loc = cv2.minMaxLoc(result)
        print("Time: " + str(time.time() - loopStartTime), max_val, max_loc, startHeight, count)
        if max_loc[0] > lBound and max_loc[0] < rBound and abs(max_loc[0] - prev_val) > 10:
            print("FOUND")
            count += 1
            total += 1
            pyautogui.click(int(gameWidth + startXCoord - 200), int(screenHeight / 2))
            image.save("image" + str(total) + ".png", "PNG")
            top_left = max_loc
            bottom_right = (top_left[0] + template_width, top_left[1] + template_height)
            cv2.rectangle(grayImage, top_left, bottom_right, (0, 255, 0), 2)
            plt.imsave("result" + str(total) + ".png", grayImage)
            time.sleep(0.15)
        time.sleep(0.006)
        prev_val = max_loc[0]
        if count >= 13:
            count = 1
            time.sleep(2.5)

        if total >= 80:
            break
        # frame = cv2.GaussianBlur(frame, (5,5), sigmaX=0)
        # gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
        # plt.imsave("gray" + str(i) + ".png", frame)
        # edges = cv2.Canny(gray, 20, 100)
        # print(edges)
        # plt.imsave("CHART" + str(i) + ".png", edges)

        # for x_coord in range(centerX - 325, centerX - 315):
        #     if edges[:, x_coord].any():
        #         print(x_coord)
        #         pyautogui.click(int(screenWidth / 2), int(screenHeight / 2))
        #         break
        # time.sleep(0.2)
    print("Runtime", time.time() - startTime)

if __name__ == "__main__":
    main()
