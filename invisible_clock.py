import cv2
import numpy as np
import time

cap = cv2.VideoCapture(0)
#Putting some time to camera wakeup
time.sleep(3)
count = 0
bg = 0
ret,bg = cap.read()

#invert the image/ flip the image
background = np.flip(bg, axis = 1)

while(cap.isOpened()):
    ret, img = cap.read()
    if not ret:
        break
    count += 1
    img = np.flip(img, axis=1)
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    
    #Lower and Upper range for mask1.
    lower_red1 = np.array([100,40,40])
    upper_red1 = np.array([100,255,255])
    mask1 = cv2.inRange(hsv, lower_red1, upper_red1)
    #lower and upper range for mask2.
    lower_red2 = np.array([155,40,40])
    upper_red2 = np.array([180,255,255])
    mask2 = cv2.inRange(hsv, lower_red2, upper_red2)
    #Filter for detecting the red co;or properly.
    mask1 = mask1 + mask2
    mask1 = cv2.morphologyEx(mask1,cv2.MORPH_OPEN, np.ones((3,3),np.uint8))
    mask1 = cv2.dilate(mask1, np.ones((3,3), np.uint8))
    mask2 = cv2.bitwise_not(mask1)

    #final output
    res1 = cv2.bitwise_and(bg, bg, mask = mask1)
    res2 = cv2.bitwise_and(img, img, mask = mask2)
    output = cv2.addWeighted(res1, 1, res2, 1, 0)
    cv2.imshow('Invisible Clock', output)

    if cv2.waitKey(1) == ord('q'):break
cap.release()
cv2.destroyAllWindows()
