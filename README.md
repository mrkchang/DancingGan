## DancingGan - Reimplemention and Improvement from "Everybody Dance Now" by Caroline Chan, et al @ UC Berkeley

Authors: Michael Arruza-Cruz, Mark Chang

# Instructions for openpose
Using openpose to extract poses and video:
>bin\OpenPoseDemo.exe --video file\Source_052619.mp4 - -hand --face --number_people_max 1 --write_json file --write_video file/poses.avi --disable_blendng

# Instructions for running and training GANs
TRAIN
>python train.py --label_nc 0 --no_instance --dataroot datasets/lacoste --name dummy --no_flip --serial_batches --input_nc 6 --output_nc 3 --mark --real_prob 0

>python train.py --label_nc 0 --no_instance --dataroot datasets/lacoste --name background0 --no_flip --serial_batches --input_nc 9 --output_nc 3 --mark --background --real_prob 0


TEST
>python test.py --name RandomKeep --label_nc 0 --no_instance --dataroot datasets/lacoste --no_flip --serial_batches --input_nc 6 --output_nc 3 --mark --how_many 33072




# GCloud 
git clone https://github.com/cs231n/gcloud.git
cd gcloud/
chmod +x ./setup.sh
./setup.sh

gcloud compute scp train_B.zip --zone "us-central1-c" mark@centralbaby-vm:~/DancingGan/thirdparty/pix2pixHD/datasets/lacoste

gcloud compute ssh --zone "us-west1-b" dl-vm1-vm -- -L 8890:127.0.0.1:8890

# SSH keygen 
cat ~/.ssh/id_rsa.pub
ssh-keygen -t rsa -b 4096 -C "mrkchang@github.com"
eval "$(ssh-agent -s)"
ssh-add ~/.ssh/id_rsa
sudo apt-get install xclip
xclip -sel clip < ~/.ssh/id_rsa.pub

# Server hosting 
gcloud compute ssh --zone "us-west1-b" dl-vm1-vm -- -L 8890:127.0.0.1:8890
python -m http.server 8890
http://127.0.0.1:8890/DancingGan/thirdparty/pix2pixHD/checkpoints/background0/web/index.html

gcloud compute ssh --zone "us-central1-c" centralbaby-vm -- -L 8891:127.0.0.1:8891
python -m http.server 8891
http://127.0.0.1:8891/DancingGan/thirdparty/pix2pixHD/checkpoints/dummy/web/index.html

# tmux
tmux new -s temporal
cntrl + b, d
