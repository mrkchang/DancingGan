import cv2
import os
import numpy as np

root_file = "H:\\DancingGan\\thirdparty\\pix2pixHD\\results\\RandomKeep\\test_latest\\images"
imgs=[]

fileNames = []
sortKey = lambda x: int(x.split("/")[-1].split("\\")[-1][len("frame"):][:-len("_synthesized_image.jpg")])

for root, _, fnames in sorted(os.walk(root_file)):
    for fname in fnames:
        if "synthesized_image" in fname:
            path = os.path.join(root, fname)
            fileNames.append(path)

first = cv2.imread(fileNames[0])
height,width,layers=first.shape

fourcc = cv2.VideoWriter_fourcc(*'DIVX')
video=cv2.VideoWriter('generated_video.avi',fourcc,29,(width,height))

# COUNT = 0
for fName in sorted(fileNames, key=sortKey):
    # imgs.append(cv2.imread(fName))
    
    video.write(cv2.imread(fName))
    print(fName)
    # if COUNT > 100: break
    # COUNT += 1

cv2.destroyAllWindows()
video.release()