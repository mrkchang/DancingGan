from skimage.measure import compare_ssim
from skimage.io import imread
import matplotlib.pyplot as plt

import os

ground_truth_dir =  "" #Put directories here; must have files with same name.
generated_image_dir = ""

ssim_scores = []

for filename in os.listdir(ground_truth_dir):
    true_image = imread(os.path.join(ground_truth_dir, filename))
    gen_image = imread(os.path.join(generated_image_dir, filename))
    ssim_scores.append(compare_ssim(true_image, gen_image))

print("Max SSIM: ", max(ssim_scores))
print("Min SSIM: ", min(ssim_scores))
print("Mean SSIM: ", sum(ssim_scores)/len(ssim_scores))

plt.hist(ssim_scores, 100)
plt.show()
