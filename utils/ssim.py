from skimage.measure import compare_ssim
from skimage.io import imread
import matplotlib.pyplot as plt
import pickle
import os

ground_truth_dir =  "thirdparty/pix2pixHD/datasets/poses/train_B" #Put directories here; must have files with same name.
generated_image_dir = "thirdparty/pix2pixHD/results/backgroundWithRandomKeep/test_latest/images"

ssim_scores = []

for i in range(1,33073):
    real_filename = "frame" + str(i) + ".jpg"
    synth_filename = "frame" + str(i) + "_synthesized_image.jpg"
    true_image = imread(os.path.join(ground_truth_dir, real_filename))
    gen_image = imread(os.path.join(generated_image_dir, synth_filename))
    ssim_scores.append(compare_ssim(true_image, gen_image))

print("Max SSIM: ", max(ssim_scores))
print("Min SSIM: ", min(ssim_scores))
print("Mean SSIM: ", sum(ssim_scores)/len(ssim_scores))

with open('list.pkl', 'wb') as f:
    pickle.dump(ssim_scores, f)

