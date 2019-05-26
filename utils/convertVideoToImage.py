import cv2
import os
print(cv2.__version__)
vidcap = cv2.VideoCapture('../data/poses_dancer.avi')
savefolder = "professionalPoses"

success, image = vidcap.read()
count = 0
success = True

if not os.path.exists("../data/" + savefolder):
    os.makedirs("../data/" + savefolder)

while success:
    cv2.imwrite("../data/" + savefolder +"/frame%d.jpg" % count, image)     # save frame as JPEG file
    success,image = vidcap.read()
    print('Read a new frame', count, ' : ', success)
    count += 1