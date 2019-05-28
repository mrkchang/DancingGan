# DancingGan - Reimplemention and Improvement from "Everybody Dance Now" by Caroline Chan, et al @ UC Berkeley

Authors: Michael Arruza-Cruz, Mark Chang

Instructions
Using openpose to extract poses and video:
>bin\OpenPoseDemo.exe --video file\Source_052619.mp4 - -hand --face --number_people_max 1 --write_json file --write_video file/poses.avi --disable_blendng

TRAIN
>python train.py --label_nc 0 --no_instance --dataroot datasets/lacoste --name dummy --no_flip --serial_batches --input_nc 6 --output_nc 3 --mark --real_prob 0

>python train.py --label_nc 0 --no_instance --dataroot datasets/lacoste --name background0 --no_flip --serial_batches --input_nc 9 --output_nc 3 --mark --background --real_prob 0


TEST
>python test.py --name RandomKeep --label_nc 0 --no_instance --dataroot datasets/lacoste --no_flip --serial_batches --input_nc 6 --output_nc 3 --mark --how_many 33072




GCLOUD STUFF
gcloud compute scp train_original.mp4 markchang93@dl-vm1-vm:~/DancingGan/file

gcloud compute scp train_original.mp4 mark@dl-vm1-vm:~/DancingGan/file

cat ~/.ssh/id_rsa.pub