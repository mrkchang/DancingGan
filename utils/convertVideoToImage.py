import cv2
import os
print(cv2.__version__)
vidcap = cv2.VideoCapture('../data/posesonly.avi')
success, image = vidcap.read()
count = 0
success = True

if not os.path.exists("../data/posesonly_images"):
    os.makedirs("../data/posesonly_images")

while success:
    cv2.imwrite("../data/posesonly_images/frame%d.jpg" % count, image)     # save frame as JPEG file
    success,image = vidcap.read()
    print('Read a new frame: ', success)
    count += 1