'''
Process sinograms in 2D
'''

from skimage.transform import radon as radon_scikit 
from skimage.transform import iradon as iradon_scikit


import torch
from .modl import ToMoDL
from .unet import UNet
try:
    from torch_radon import Radon as radon_thrad
    use_cuda = True

except:
    use_cuda = False
    print('Torch-Radon not available!')


from .alternating import TwIST, TVdenoise, TVnorm


import numpy as np
from napari.layers import Image
import scipy.ndimage as ndi
import os
import matplotlib.pyplot as plt 
import cv2
from enum  import Enum
import tqdm
import os, sys

for k, v in os.environ.items():
    if k.startswith("QT_") and "cv2" in v:
        del os.environ[k]

try:
    device = torch.device("cuda:0" if use_cuda == True else "cpu")
except:
    print('Torch not available!')

class Rec_Modes(Enum):
    FBP_CPU = 0
    FBP_GPU = 1
    TWIST_CPU = 2
    UNET_GPU = 3
    MODL_GPU = 4
    MODL_CPU = 5

class Order_Modes(Enum):
    Vertical = 0
    Horizontal = 1

def my_filtering_function(pair):
    unwanted_key = 'num_batches'
    key, value = pair
    if unwanted_key in key:
        return False  # filter pair out of the dictionary
    else:
        return True  # keep pair in the filtered dictionary

class OPTProcessor:

    def __init__(self):
        '''
        Variables for OPT processor
        '''

        self.resize_val = 100
        self.rec_process = Rec_Modes.FBP_CPU.value
        self.order_mode = Order_Modes.Vertical.value
        self.clip_to_circle = False
        self.use_filter = False

        self.resize_bool = True
        self.register_bool = True
        self.max_shift = 200
        self.shift_step = 10
        self.center_shift = 0

        self.set_reconstruction_process()
    
    def set_reconstruction_process(self):

        self.init_volume_rec = False
        self.iradon_functor = None
        # This should change depending on the method
        if (self.rec_process == Rec_Modes.FBP_CPU.value) or (self.rec_process == Rec_Modes.MODL_GPU.value):
            
            self.angles_gen = lambda num_angles: np.linspace(0, 2*180, num_angles, endpoint = False)
            self.iradon_function = lambda sino, num_angles: iradon_scikit(sino.T, self.angles_gen(num_angles), circle = False)
        
        elif (self.rec_process == Rec_Modes.FBP_GPU.value):
            
            assert(torch.cuda.is_available() == True)
            self.angles_gen = lambda num_angles: np.linspace(0, 2*np.pi, num_angles, endpoint = False)
        

    def correct_and_reconstruct(self, sinogram: np.ndarray):
        '''
        Corrects rotation axis by finding optimal registration via maximising reconstructed image's intensity variance.

        Based on 'Walls, J. R., Sled, J. G., Sharpe, J., & Henkelman, R. M. (2005). Correction of artefacts in optical projection tomography. Physics in Medicine & Biology, 50(19), 4645.'

        Params:
        - sinogram
        '''

        if self.shift_step < 1:
            
            if self.order_mode == Order_Modes.Vertical.value:
                shift_tuple = (0, np.copy(self.center_shift))
            elif self.order_mode == Order_Modes.Horizontal.value:
                shift_tuple = (np.copy(self.center_shift), 0)

            # Restart shifts
            self.max_shift = 200
            self.shift_step = 10
            self.center_shift = 0
            
            return self.reconstruct(ndi.shift(sinogram, shift_tuple, mode = 'nearest'))
        
        shifts = np.arange(-self.max_shift, self.max_shift, self.shift_step)+self.center_shift
        image_std = []

        for i, shift in enumerate(shifts):
            
            
            if self.order_mode == Order_Modes.Vertical.value:
                shift_tuple = (0, shift)
                
            if self.order_mode == Order_Modes.Horizontal.value:
                shift_tuple = (shift, 0)

            sino_shift = ndi.shift(sinogram, shift_tuple, mode = 'nearest')

            # Get image reconstruction
            shift_iradon = self.reconstruct(sino_shift)
            
            # Calculate variance
            image_std.append(np.std(shift_iradon))

        # To-Do: Change shifts
        self.center_shift = shifts[np.argmax(image_std)]
        self.max_shift /= 5
        self.shift_step /= 2.5

        return self.correct_and_reconstruct(sinogram)

    def resize(self, sinogram_volume: np.ndarray):
        '''
        Resizes sinogram prior to reconstruction.
        Args:
            -sinogram_volume (np.ndarray): array to resize in any mode specified.
        '''
        
        if self.order_mode == Order_Modes.Vertical.value:
            self.theta, self.Q, self.Z = sinogram_volume.shape
        if self.order_mode == Order_Modes.Horizontal.value:
            self.Q, self.theta, self.Z = sinogram_volume.shape

        if self.resize_bool == True:
            
            if self.order_mode == Order_Modes.Vertical.value:
                
                sinogram_resize = np.zeros((self.theta, int(np.ceil(self.resize_val*np.sqrt(2))),
                                        self.Z),
                                        dtype = np.float32)
                
            if self.order_mode == Order_Modes.Horizontal.value:
                
                sinogram_resize = np.zeros((int(np.ceil(self.resize_val*np.sqrt(2))), self.theta,
                                        self.Z),
                                        dtype = np.float32)
                
            for idx in tqdm.tqdm(range(self.Z)):
                
                if self.order_mode == Order_Modes.Vertical.value:

                    sinogram_resize[:,:,idx] = cv2.resize(sinogram_volume[:,:,idx], 
                                                      (int(np.ceil(self.resize_val*np.sqrt(2))), self.theta),
                                                      interpolation = cv2.INTER_NEAREST)
                    

                elif self.order_mode == Order_Modes.Horizontal.value:
                    
                    sinogram_resize[:,:,idx] = cv2.resize(sinogram_volume[:,:,idx], 
                                                      (self.theta, int(np.ceil(self.resize_val*np.sqrt(2)))),
                                                      interpolation = cv2.INTER_NEAREST)
                    

        return sinogram_resize
    
    def reconstruct(self, sinogram: np.ndarray):
        '''
        Reconstruct with specific method
        TODO: 
            * Include methods ToMODL
            * Optimize GPU usage with tensors

        '''
        ## Es un enriedo, pero inicializa los generadores de ángulos. Poco claro
        if self.init_volume_rec == False:
            
            self.angles = self.angles_gen(self.theta)   
        
        if self.iradon_functor == None:
            try:
                self.angles_torch = np.linspace(0, 2*np.pi, self.theta, endpoint = False)
                self.iradon_functor = radon_thrad(self.resize_val, 
                                              self.angles_torch, 
                                              clip_to_circle = self.clip_to_circle,
                                              det_count = np.ceil(np.sqrt(2)*self.resize_val).astype(int))         
            except:
                self.iradon_functor = None
                self.angles_torch = None
                
        if self.rec_process == Rec_Modes.FBP_GPU.value:
           
            self.angles_torch = np.linspace(0, 2*np.pi, self.theta, endpoint = False)
            
            self.iradon_functor = radon_thrad(self.resize_val, 
                                              self.angles_torch, 
                                              clip_to_circle = self.clip_to_circle,
                                              det_count = np.ceil(np.sqrt(2)*self.resize_val).astype(int))   
            
            if self.use_filter == False:
                self.iradon_function = lambda sino: self.iradon_functor.backprojection((torch.Tensor(sino.T).to(device))).cpu().numpy()
            else:
                self.iradon_function = lambda sino: self.iradon_functor.backprojection(self.iradon_functor.filter_sinogram(torch.Tensor(sino.T).to(device))).cpu().numpy()

        elif self.rec_process == Rec_Modes.FBP_CPU.value:
            
            self.iradon_function = lambda sino: iradon_scikit(sino, 
                                                              self.angles, 
                                                              circle = self.clip_to_circle,
                                                              filter_name= None if self.use_filter == False else 'ramp')
        
        elif self.rec_process == Rec_Modes.MODL_GPU.value:
            
            resnet_options_dict = {'number_layers': 8,
                                    'kernel_size':3,
                                    'features':64,
                                    'in_channels':1,
                                    'out_channels':1,
                                    'stride':1, 
                                    'use_batch_norm': True,
                                    'init_method': 'xavier'}
            
            self.tomodl_dictionary = {'use_torch_radon': True,
                                    'metric': 'psnr',
                                    'K_iterations' : 8,
                                    'number_projections_total' : sinogram.shape[0],
                                    'acceleration_factor': 10,
                                    'image_size': 100,
                                    'lambda': 0.01,
                                    'use_shared_weights': True,
                                    'denoiser_method': 'resnet',
                                    'resnet_options': resnet_options_dict,
                                    'in_channels': 1,
                                    'out_channels': 1}
                            
            self.iradon_functor = ToMoDL(self.tomodl_dictionary)
            
            __location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
            artifact_path = os.path.join(__location__, 'model.ckpt')
            tomodl_checkpoint = torch.load(artifact_path, map_location = torch.device("cuda:0"))

            tomodl_checkpoint['state_dict'] = {k.replace("model.", ""): v for (k,v) in tomodl_checkpoint['state_dict'].items()}

            self.iradon_functor.load_state_dict(dict(filter(my_filtering_function, tomodl_checkpoint['state_dict'].items())))
            self.iradon_function = lambda sino: self.iradon_functor(
                                                    torch.Tensor(
                                                        iradon_scikit(sino, 
                                                                      self.angles, 
                                                                      circle = self.clip_to_circle, filter_name = None)).to(device).unsqueeze(0).unsqueeze(1))['dc'+str(self.tomodl_dictionary['K_iterations'])].detach().cpu().numpy()

        elif self.rec_process == Rec_Modes.MODL_CPU.value:
            
            resnet_options_dict = {'number_layers': 8,
                                    'kernel_size':3,
                                    'features':64,
                                    'in_channels':1,
                                    'out_channels':1,
                                    'stride':1, 
                                    'use_batch_norm': True,
                                    'init_method': 'xavier'}
            
            self.tomodl_dictionary = {'use_torch_radon': True,
                                    'metric': 'psnr',
                                    'K_iterations' : 8,
                                    'number_projections_total' : sinogram.shape[0],
                                    'acceleration_factor': 32,
                                    'image_size': 100,
                                    'lambda': 0.025,
                                    'use_shared_weights': True,
                                    'denoiser_method': 'resnet',
                                    'resnet_options': resnet_options_dict,
                                    'in_channels': 1,
                                    'out_channels': 1}
                            
            self.iradon_functor = ToMoDL(self.tomodl_dictionary)
            
            __location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
            artifact_path = os.path.join(__location__, 'model.ckpt')
            tomodl_checkpoint = torch.load(artifact_path, map_location = torch.device("cpu"))

            tomodl_checkpoint['state_dict'] = {k.replace("model.", ""): v for (k,v) in tomodl_checkpoint['state_dict'].items()}

            self.iradon_functor.load_state_dict(dict(filter(my_filtering_function, tomodl_checkpoint['state_dict'].items())))
            self.iradon_function = lambda sino: self.iradon_functor(
                                                    torch.Tensor(
                                                        iradon_scikit(sino, 
                                                                      self.angles, 
                                                                      circle = self.clip_to_circle, filter_name = None)).to(device).unsqueeze(0).unsqueeze(1))['dc'+str(self.tomodl_dictionary['K_iterations'])].detach().cpu().numpy()

        elif self.rec_process == Rec_Modes.TWIST_CPU.value:

            Psi = lambda x,th: TVdenoise(x,2/th, 3)
            #  set the penalty function, to compute the objective
            Phi = lambda x: TVnorm(x)

            twist_dictionary = {'LAMBDA': 1e-4, 
                                'TOLERANCEA':1e-4,
                                'STOPCRITERION':1, 
                                'VERBOSE':1,
                                'INITIALIZATION':0,
                                'MAXITERA':10000, 
                                'GPU':0,
                                'PSI': Psi,
                                'PHI': Phi,

                                }
            
            A = lambda x: radon_scikit(x, self.angles, circle = self.clip_to_circle)
            AT = lambda sino: iradon_scikit(sino, self.angles, circle = self.clip_to_circle)
            self.iradon_function = lambda sino: TwIST(sino, A, AT, 0.01, twist_dictionary, true_img = AT(sino))[0]
            
        elif self.rec_process == Rec_Modes.UNET_GPU.value:    

            self.iradon_functor = UNet(n_channels = 1, n_classes= 1, residual = True, up_conv = True, batch_norm = True, batch_norm_inconv = True).to(device)
            AT_tensor = lambda sino: torch.Tensor(iradon_scikit(sino, self.angles, circle = self.clip_to_circle, filter_name = None)).to(device).unsqueeze(0).unsqueeze(1)
            
            self.iradon_function = lambda sino: self.iradon_functor(AT_tensor(sino)).detach().cpu().numpy()

        
        reconstruction = self.iradon_function(sinogram) 

        return reconstruction
        
    
