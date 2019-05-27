import cv2
import os
import numpy as np

root_file = ""
imgs=[]

fileNames = []
sortKey = lambda x: int(x.split("/")[-1].split("\\")[-1][len("frame"):][:-len("_synthesized_image.jpg")])

for root, _, fnames in sorted(os.walk(dir)):
    for fname in fnames:
        if "synthesized_image" in fname:
            path = os.path.join(root, fname)
            fileNames.append(path)

for fName in sorted(fileNames, key=sortKey):
    imgs.append(cv2.imread(fName))

height,width,layers=imgs[1].shape

video=cv2.VideoWriter('generated_video.avi',-1,1,(width,height))

for img in imgs:
    print(img)
    video.write(img)

cv2.destroyAllWindows()
video.release()