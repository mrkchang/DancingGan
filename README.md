# DancingGan - Reimplemention and Improvement from "Everybody Dance Now" by Caroline Chan, et al @ UC Berkeley

Authors: Michael Arruza-Cruz, Mark Chang

Instructions
Using openpose to extract poses and video:
bin\OpenPoseDemo.exe --video file\Source_052619.mp4 - -hand --face --number_people_max 1 --write_json file --write_video file/poses.avi --disable_blendng



python test.py --name RandomKeep --label_nc 0 --no_instance --dataroot datasets/lacoste --no_flip --serial_batches --input_nc 6 --output_nc 3 --mark

python train.py --label_nc 0 --no_instance --dataroot datasets/lacoste --name dummy --no_flip --serial_batches --input_nc 6 --output_nc 3 --mark --real_prob 0