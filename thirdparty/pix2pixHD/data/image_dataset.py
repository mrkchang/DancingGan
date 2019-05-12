### Copyright (C) 2017 NVIDIA Corporation. All rights reserved. 
### Licensed under the CC BY-NC-SA 4.0 license (https://creativecommons.org/licenses/by-nc-sa/4.0/legalcode).
import os.path
from data.base_dataset import BaseDataset, get_params, get_transform, normalize
from data.image_folder import make_dataset
from PIL import Image

class ImageDataset(BaseDataset):
    def initialize(self, opt):
        self.opt = opt
        self.root = opt.dataroot

        sortKey = lambda x: int(x.split("/")[-1][len("figure"):][:-len(".jpg")])
        ### input A (real_images)
        dir_A = '_A'
        self.dir_A = os.path.join(opt.dataroot, opt.phase + dir_A)
        self.A_paths = sorted(make_dataset(self.dir_A), key=sortKey)

        ### input B (real images)
        if opt.isTrain:
            dir_B = '_B'
            self.dir_B = os.path.join(opt.dataroot, opt.phase + dir_B)  
            self.B_paths = sorted(make_dataset(self.dir_B), key=sortKey)

        self.dataset_size = len(self.A_paths) 

    def getWithIndex(self, index):
        ### input A (label maps)
        A_path = self.A_paths[index]
        A = Image.open(A_path)
        params = get_params(self.opt, A.size)

        transform_A = get_transform(self.opt, params)
        A_tensor = transform_A(A.convert('RGB'))

        B_tensor = inst_tensor = feat_tensor = 0
        ### input B (real images)
        if self.opt.isTrain or self.opt.use_encoded_image:
            B_path = self.B_paths[index]
            B = Image.open(B_path).convert('RGB')
            transform_B = get_transform(self.opt, params)
            B_tensor = transform_B(B)

        return A_tensor, B_tensor, A_path

    def __getitem__(self, index):
        index = max(1, index) #just to make sure it doesnt try to access index -1
        A_tensor_1, B_tensor_1, A_path = self.getWithIndex(index)
        A_tensor_0, B_tensor_0, _ = self.getWithIndex(index - 1)
        inst_tensor = feat_tensor = 0

        input_dict = {'label': A_tensor_1, 'inst': inst_tensor, 'image': B_tensor_1,
                      'feat': feat_tensor, 'path': A_path, 'label_last': A_tensor_0, 'image_last': B_tensor_0}

        return input_dict

    def __len__(self):
        return len(self.A_paths) // self.opt.batchSize * self.opt.batchSize

    def name(self):
        return 'AlignedDataset'