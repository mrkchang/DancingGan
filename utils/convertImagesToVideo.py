import cv2
import os
import numpy as np

root_file = r"../data/train_original_gen"
outfile = 'train_original_gen.avi'
imgs=[]
fps = 30

fileNames = []
sortKey = lambda x: int(x.split("/")[-1].split("\\")[-1][len("frame"):][:-len("_synthesized_image.jpg")])
# sortKey = lambda x: int(x.split("/")[-1].split("\\")[-1][len("frame"):][:-len(".jpg")])

for root, _, fnames in sorted(os.walk(root_file)):
    for fname in fnames:
        if "synthesized_image" in fname:
        # if "frame" in fname:
            path = os.path.join(root, fname)
            fileNames.append(path)

first = cv2.imread(fileNames[0])
height,width,layers=first.shape

fourcc = cv2.VideoWriter_fourcc(*'DIVX')
video=cv2.VideoWriter(outfile,fourcc,fps,(width,height))

# COUNT = 0
for fName in sorted(fileNames, key=sortKey):
    # imgs.append(cv2.imread(fName))
    
    video.write(cv2.imread(fName))
    print(fName)
    # if COUNT > 100: break
    # COUNT += 1

cv2.destroyAllWindows()
video.release()