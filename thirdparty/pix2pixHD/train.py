### Copyright (C) 2017 NVIDIA Corporation. All rights reserved. 
### Licensed under the CC BY-NC-SA 4.0 license (https://creativecommons.org/licenses/by-nc-sa/4.0/legalcode).
import time
import os
import numpy as np
import torch
from torch.autograd import Variable
from collections import OrderedDict
from subprocess import call
# from apex import amp
import fractions
def lcm(a,b): return abs(a * b)/fractions.gcd(a,b) if a and b else 0

from options.train_options import TrainOptions
from data.data_loader import CreateDataLoader
import util.util as util
from util.visualizer import Visualizer

def main():
    opt = TrainOptions().parse()
    iter_path = os.path.join(opt.checkpoints_dir, opt.name, 'iter.txt')

    if not opt.mark:
        from models.models import create_model
    else:
        if opt.background:

            from models.mb_models import create_model # m_flag
        else:
            from models.m_models import create_model # m_flag

    if opt.continue_train:
        try:
            start_epoch, epoch_iter = np.loadtxt(iter_path , delimiter=',', dtype=int)
        except:
            start_epoch, epoch_iter = 1, 0
        print('Resuming from epoch %d at iteration %d' % (start_epoch, epoch_iter))        
    else:    
        start_epoch, epoch_iter = 1, 0

    opt.print_freq = lcm(opt.print_freq, opt.batchSize)    
    if opt.debug:
        opt.display_freq = 1
        opt.print_freq = 1
        opt.niter = 1
        opt.niter_decay = 0
        opt.max_dataset_size = 10

    data_loader = CreateDataLoader(opt)
    dataset = data_loader.load_data()
    dataset_size = len(data_loader)
    print('#training images = %d' % dataset_size)

    model = create_model(opt)
    visualizer = Visualizer(opt)
    # if opt.fp16:    
    #     model, [optimizer_G, optimizer_D] = amp.initialize(model, [model.optimizer_G, model.optimizer_D], opt_level='O1')             
    #     model = torch.nn.DataParallel(model, device_ids=opt.gpu_ids)
    # else:
    optimizer_G, optimizer_D = model.module.optimizer_G, model.module.optimizer_D

    total_steps = (start_epoch-1) * dataset_size + epoch_iter

    display_delta = total_steps % opt.display_freq
    print_delta = total_steps % opt.print_freq
    save_delta = total_steps % opt.save_latest_freq

    # fake_last = torch.zeros(1, 3, 576, 1024) # m_flag
    # background = dataset.dataset.getZeroImage("H:\\DancingGan\\thirdparty\\pix2pixHD\\datasets\\lacoste\\train_B\\frame0.jpg")
    # background = dataset.dataset.getZeroImage("datasets\\lacoste\\train_B\\frame0.jpg")
    background = dataset.dataset.getZeroImage(os.path.join("datasets","lacoste","train_B","frame0.jpg"))
    background = torch.unsqueeze(background,dim=0).cuda()#torch.zeros(1, 3, 576, 1024).cuda() # m_flag
    fake_last = background.clone()


    for epoch in range(start_epoch, opt.niter + opt.niter_decay + 1):
        epoch_start_time = time.time()
        if epoch != start_epoch:
            epoch_iter = epoch_iter % dataset_size
        for i, data in enumerate(dataset, start=epoch_iter):
            if total_steps % opt.print_freq == print_delta:
                iter_start_time = time.time()
            total_steps += opt.batchSize
            epoch_iter += opt.batchSize

            # whether to collect output images
            if not opt.mark:
                save_fake = total_steps % opt.display_freq == display_delta
            else:
                save_fake = True
        
            ############## Forward Pass ######################

            if not opt.mark:
                losses, generated = model(Variable(data['label']), Variable(data['inst']), 
                    Variable(data['image']), Variable(data['feat']), infer=save_fake)
            else:
                if opt.background:
                    losses, generated = model(Variable(data['label']), Variable(data['inst']), 
                        Variable(data['image']), Variable(data['feat']), 
                        label_last = Variable(data['label_last']), 
                        image_last = Variable(data['image_last']), 
                        fake_last = fake_last, background = background, infer=save_fake)
                    fake_last = generated.detach()

                else:
                    losses, generated = model(Variable(data['label']), Variable(data['inst']), 
                        Variable(data['image']), Variable(data['feat']), 
                        label_last = Variable(data['label_last']), 
                        image_last = Variable(data['image_last']), 
                        fake_last = fake_last, infer=save_fake)
                    fake_last = generated.detach()

            # from model: forward(self, label, inst, image, feat, infer=False)
            # from pdb, label and image have true sizes
            # fake_image = self.netG.forward(input_concat) <- input_concat = input_label <- label
            # pred_fake = self.discriminate(input_label, real_image)

            # sum per device losses
            losses = [ torch.mean(x) if not isinstance(x, int) else x for x in losses ]
            loss_dict = dict(zip(model.module.loss_names, losses))

            # calculate final loss scalar
            loss_D = (loss_dict['D_fake'] + loss_dict['D_real']) * 0.5
            loss_G = loss_dict['G_GAN'] + loss_dict.get('G_GAN_Feat',0) + loss_dict.get('G_VGG',0)

            ############### Backward Pass ####################
            # update generator weights
            optimizer_G.zero_grad()
            # if opt.fp16:                                
            #     with amp.scale_loss(loss_G, optimizer_G) as scaled_loss: scaled_loss.backward()                
            # else:
            loss_G.backward()          
            optimizer_G.step()

            # update discriminator weights
            optimizer_D.zero_grad()
            # if opt.fp16:                                
            #     with amp.scale_loss(loss_D, optimizer_D) as scaled_loss: scaled_loss.backward()                
            # else:
            loss_D.backward()        
            optimizer_D.step()        

            ############## Display results and errors ##########
            ### print out errors
            if total_steps % opt.print_freq == print_delta:
                errors = {k: v.data.item() if not isinstance(v, int) else v for k, v in loss_dict.items()}            
                t = (time.time() - iter_start_time) / opt.print_freq
                visualizer.print_current_errors(epoch, epoch_iter, errors, t)
                visualizer.plot_current_errors(errors, total_steps)
                #call(["nvidia-smi", "--format=csv", "--query-gpu=memory.used,memory.free"]) 

            ### display output images
            # if save_fake: # m_flag
            if total_steps % opt.display_freq == display_delta: # m_flag
                visuals = OrderedDict([('input_label', util.tensor2label(data['label'][0], opt.label_nc)),
                                    ('synthesized_image', util.tensor2im(generated.data[0])),
                                    ('real_image', util.tensor2im(data['image'][0]))])
                visualizer.display_current_results(visuals, epoch, total_steps)

            ### save latest model
            if total_steps % opt.save_latest_freq == save_delta:
                print('saving the latest model (epoch %d, total_steps %d)' % (epoch, total_steps))
                model.module.save('latest')            
                np.savetxt(iter_path, (epoch, epoch_iter), delimiter=',', fmt='%d')

            if epoch_iter >= dataset_size:
                break
        
        # end of epoch 
        iter_end_time = time.time()
        print('End of epoch %d / %d \t Time Taken: %d sec' %
            (epoch, opt.niter + opt.niter_decay, time.time() - epoch_start_time))

        ### save model for this epoch
        if epoch % opt.save_epoch_freq == 0:
            print('saving the model at the end of epoch %d, iters %d' % (epoch, total_steps))        
            model.module.save('latest')
            model.module.save(epoch)
            np.savetxt(iter_path, (epoch+1, 0), delimiter=',', fmt='%d')

        ### instead of only training the local enhancer, train the entire network after certain iterations
        if (opt.niter_fix_global != 0) and (epoch == opt.niter_fix_global):
            model.module.update_fixed_params()

        ### linearly decay learning rate after certain iterations
        if epoch > opt.niter:
            model.module.update_learning_rate()

if __name__ == '__main__':
    main()
