import cv2
import os
print(cv2.__version__)
vidcap = cv2.VideoCapture('../data/original.mp4')
success, image = vidcap.read()
count = 0
success = True

if not os.path.exists("../data/original_images"):
    os.makedirs("../data/original_images")

while success:
    cv2.imwrite("../data/original_images/frame%d.jpg" % count, image)     # save frame as JPEG file
    success,image = vidcap.read()
    print('Read a new frame', count, ' : ', success)
    count += 1