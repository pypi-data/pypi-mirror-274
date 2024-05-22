#dataloader for pytorch1.0

import torch
import torchvision
import torchvision.transforms as transforms
from torch.utils.data import DataLoader
from mb_pytorch.utils.yaml_reader import YamlReader
import os
import sys
import numpy as np
from mb_pandas.src.dfload import load_any_df
from mb_utils.src.verify_image import verify_image
from mb_pandas.src.transform import *
from datetime import datetime
import cv2

today = datetime.now()

__all__ = ['data_fetcher','DataLoader']

class data_fetcher:
    """
    dataloader for pytorch1.0
    """
    def __init__(self,yaml,logger=None) -> None:
        self.yaml = yaml
        self.logger = logger
        self._yaml_data = None
        self.data_dict = {}
        self.transforms_final=[]
        self.all = None

    def __repr__(self) -> str:
        return "data_fetcher(yaml={},logger={})".format(self.yaml,self.logger)

    @staticmethod
    def read_yaml(self):
        """
        read yaml file
        """
        self._yaml_data = YamlReader(self.yaml).data(self.logger)
        return self._yaml_data

    @property
    def load_data_params(self):
        """
        get dataloader data from yaml file
        """
        data = YamlReader(self.yaml).data(self.logger)
        self.data_dict['data'] = data['data']
        self.data_dict['train_params'] = data['train_params']
        self.data_dict['test_params'] = data['test_params']
        self.data_dict['transforms_list'] = data['transformation']
        self.data_dict['model'] = data['model']
        return self.data_dict
    
    @property
    def load_data_all(self):
        """
        get dataloader all data dict from yaml file
        """
        data = YamlReader(self.yaml).data(self.logger)
        self.all = data
        return self.all

class JointTransforms:
    def __init__(self,transform_yaml,logger=None):
        """
        get transforms from yaml file
        """

        self.transform_data = transform_yaml
        self.logger = logger

        if self.transform_data['transform']==False:
            return None

    def __call__(self,img,mask=None):
        if self.transform_data['to_tensor']['val']:
            img = transforms.ToTensor()(img)
            if mask is not None:
                mask = transforms.ToTensor()(mask)

        if self.transform_data['normalize']['val']:
            img = transforms.Normalize(self.transform_data['normalize']['args']['mean'],self.transform_data['normalize']['args']['std'])(img)

        if self.transform_data['resize']['val']:
            img = transforms.Resize(self.transform_data['resize']['args']['size'])(img)
            if mask is not None:
                mask = transforms.Resize(self.transform_data['resize']['args']['size'])(mask)

        if self.transform_data['random_crop']['val']:
            img = transforms.RandomCrop(self.transform_data['random_crop']['args']['size'])(img)
            if mask is not None:
                mask = transforms.RandomCrop(self.transform_data['random_crop']['args']['size'])(mask)

        if self.transform_data['random_horizontal_flip']['val']:
            img = transforms.RandomHorizontalFlip(self.transform_data['random_horizontal_flip']['args']['p'])(img)
            if mask is not None:
                mask = transforms.RandomHorizontalFlip(self.transform_data['random_horizontal_flip']['args']['p'])(mask)

        if self.transform_data['random_vertical_flip']['val']:
            img = transforms.RandomVerticalFlip(self.transform_data['random_vertical_flip']['args']['p'])(img)
            if mask is not None:
                mask = transforms.RandomVerticalFlip(self.transform_data['random_vertical_flip']['args']['p'])(mask)

        if self.transform_data['random_rotation']['val']:
            img = transforms.RandomRotation(self.transform_data['random_rotation']['args']['degrees'])(img)
            if mask is not None:
                mask = transforms.RandomRotation(self.transform_data['random_rotation']['args']['degrees'])(mask)

        if self.transform_data['random_color_jitter']['val']:
            img = transforms.ColorJitter(brightness=self.transform_data['random_color_jitter']['args']['brightness'],contrast=self.transform_data['random_color_jitter']['args']['contrast'],saturation=self.transform_data['random_color_jitter']['args']['saturation'],hue=self.transform_data['random_color_jitter']['args']['hue'])(img)
        
        if self.transform_data['random_grayscale']['val']:
            img = transforms.RandomGrayscale(self.transform_data['random_grayscale']['args']['p'])(img)

        if self.logger:
            self.logger.info("transforms: {}".format(self.transform_data))
        
        if mask is not None:
            return img,mask
        else:
            return img
   
class customdl(torch.utils.data.Dataset):
    def __init__(self,data,model_type,transform=None,train_file=True,logger=None):
        self.transform=transform
        self.logger=logger
        self.folder_name=os.path.dirname(data['root'])
        self.data_type = model_type
        self.csv_data = load_any_df(data['root'],logger=self.logger)

        if self.logger:
            self.logger.info("Data file: {} loaded with mb_pandas.".format(data))
            self.logger.info("Data columns: {}".format(self.csv_data.columns))
            self.logger.info("Data will be split into train and validation according to train_file input : {}".format(train_file))
            self.logger.info("If unnamed columns are present, they will be removed.")
            self.logger.info("If duplicate rows are present, they will be removed.")
        assert 'image_path' in self.csv_data.columns, "image_path column not found in data"
        assert 'image_type' in self.csv_data.columns, "image_type column not found in data"

        if train_file: ## used this to differentiate between train and validation data in the data file
            self.csv_data = self.csv_data[self.csv_data['image_type'] == 'training']
        else:
            self.csv_data = self.csv_data[self.csv_data['image_type'] == 'validation']

        self.csv_data = check_drop_duplicates(self.csv_data,columns=['image_path'],drop=True,logger=self.logger)
        self.csv_data = remove_unnamed(self.csv_data,logger=self.logger)

        # else:
        #     date_now = today.strftime("%d_%m_%Y_%H_%M")
        #     self.folder_name='data_'+date_now
        # os.mkdir('./data'+str(self.folder_name))

        if data['use_img_dir']:
            img_path = [os.path.join(str(data['img_dir']),self.csv_data['image_path'].iloc[i]) for i in range(len(self.csv_data))]
        else:
            img_path = [self.csv_data['image_path'].iloc[i] for i in range(len(self.csv_data))]
        self.csv_data['image_path_new'] = img_path
        if self.logger:
            self.logger.info("Verifying paths")
            self.logger.info("first path : {}".format(img_path[0]))

        path_check_res= [os.path.exists(img_path[i]) for i in range(len(img_path))]
        self.csv_data['img_path_check'] = path_check_res
        self.csv_data = self.csv_data[self.csv_data['img_path_check'] == True]
        self.csv_data = self.csv_data.reset_index(drop=True)
        if logger:
            self.logger.info("self.data: {}".format(self.csv_data))

        if data['thresholding_pd']>0:
            if len(self.csv_data) <= data['thresholding_pd']:
                self.logger.info("Length of data after removing invalid paths: {}".format(len(self.csv_data)))
                self.logger.info("Less than thresholding_pd data points. Please check the data file.")
                self.logger.info("Exiting")
                sys.exit('Less than thresholding_pd data points. Please check the data file.')

        if self.logger:
            self.logger.info("Length of data after removing invalid paths: {}".format(len(self.csv_data)))

        if data['verify_image']:
            if self.logger:
                self.logger.info("Verifying images")
            verify_image_res = [verify_image(self.csv_data['image_path_new'].iloc[i],logger=self.logger) for i in range(len(self.csv_data))]  
            self.csv_data['img_verify'] = verify_image_res
            self.csv_data = self.csv_data[self.csv_data['img_verify'] == True]
            self.csv_data = self.csv_data.reset_index()

            if data['thresholding_pd']>0:
                if len(self.csv_data) <= data['thresholding_pd']:
                    self.logger.info("Length of data after removing invalid images: {}".format(len(self.csv_data)))
                    self.logger.info("Less than thresholding_pd data points. Please check the data file.")
                    self.logger.info("Exiting")
                    sys.exit('Less than thresholding_pd data points. Please check the data file.')
        else:   
            if self.logger:
                self.logger.info("Skipping image verification")
        
        if self.data_type == 'classification':
            assert 'label' in self.csv_data.columns, "label column not found in data"
            self.label = self.csv_data['label']
    

        if self.data_type == 'segmentation':
            assert 'mask_path' in self.csv_data.columns, "mask_path column not found in data"
            self.masks = self.csv_data['mask_path']

        if self.data_type == 'detection':
            assert 'label' in self.csv_data.columns, "label column not found in data"
            assert 'bbox' in self.csv_data.columns, "bbox column not found in data"
            self.label = self.csv_data['label']
            self.bbox = self.csv_data['bbox']

        ## save wrangled file
        try:
            if os.path.exists(self.folder_name):
                self.csv_data.to_csv(os.path.join(self.folder_name,'wrangled_file.csv'),index=False)
        except:
            if self.logger:
                self.logger.info("Could not save wrangled file. Please check the folder name.")

    def __len__(self):
        return len(self.csv_data)
    
    def __repr__(self) -> str:
        return "self.data: {},self.transform: {},self.label: {}".format(self.csv_data,self.transform,self.label)

    def __getitem__(self,idx):
        
        img = self.csv_data['image_path_new'].iloc[idx]
        #img = Image.open(img)
        img = cv2.imread(img)

        if self.data_type == 'classification':
            if self.transform:
                img = self.transform(img)
            out_dict = {'image':img}
            out_dict['label'] = self.label.iloc[idx]   

            return out_dict
        
        if self.data_type == 'segmentation':
            if self.transform:
                mask = cv2.imread(self.masks.iloc[idx],cv2.IMREAD_GRAYSCALE) ## considering mask is just binary class
                img,mask = self.transform(img,mask)
            out_dict = {'image':img}
            out_dict['mask'] = mask
            out_dict['label'] = self.label.iloc[idx]
            
            return out_dict
        
        if self.data_type == 'detection':
            if self.transform:
                img = self.transform(img)
            out_dict = {'image':img}
            out_dict['bbox'] = torch.tensor([[self.bbox.iloc[idx][0],self.bbox.iloc[idx][1],self.bbox.iloc[idx][2],self.bbox.iloc[idx][3]] 
                                             for x in len(self.bbox.iloc[idx])],dtype=torch.float32)  ## should be list in a list. 
            out_dict['label'] = self.label.iloc[idx]

            return out_dict

class DataLoader(data_fetcher):
    """
    Basic dataloader for pytorch1.0
    """
    def __init__(self,yaml,logger=None) -> None:
        super().__init__(yaml, logger=logger)
        self.yaml = yaml
        self.logger = logger
        self._yaml_data = None
        self.data_dict = self.load_data_params
        self.trainloader = None
        self.testloader = None
        self.model_type = self.data_dict['model']['model_type']
        self.dataset_params_train = self.data_dict['data']['datasets_params_train']
        self.transformations = self.data_dict['transformation']
        self.dataset_params_train['transform'] = JointTransforms(self.transformations,logger=self.logger) 
        self.dataset_params_test = self.data_dict['data']['datasets_params_test']
        self.dataset_params_test['transform'] = JointTransforms(self.transformations,logger=self.logger)
        self.data_params_file = self.data_dict['data']['from_file']

        self.data_file= self.data_dict['data']['from_datasets']

        if os.path.exists(self.dataset_params_train['root']):
            if self.logger:
                self.logger.info("Data folder already exists. Using existing data folder :  {}".format(self.dataset_params_train['root']))
        else:
            os.mkdir(self.dataset_params_train['root'])
            if self.logger:
                self.logger.info("Data folder created : {}".format(self.dataset_params_train['root']))
    
    def data_load(self):
        """
        return all data loaders
        """

        if self.data_dict['data']['from_file']==False:
            if self.data_file in dir(torchvision.datasets):
                if self.logger:
                    self.logger.info("Data file: {} loading from torchvision.datasets.".format(self.data_file))
                self.trainset = getattr(torchvision.datasets,self.data_file)(**self.dataset_params_train)
                self.testset = getattr(torchvision.datasets,self.data_file)(**self.dataset_params_test)
                if self.data_dict['data']['thresholding_pd']>0:
                    subset_indices = range(self.data_dict['data']['thresholding_pd'])
                    self.trainset = torch.utils.data.Subset(self.trainset, subset_indices)
                    self.testset = torch.utils.data.Subset(self.testset, subset_indices)
            else:
                if self.logger:
                    self.logger.info("Data file: {} could not be loaded from torchvision.datasets.".format(self.data_file))
                    self.logger.info("Exiting")
                sys.exit("Data file: {} could not be loaded from torchvision.datasets.".format(self.data_file))
        else:
            self.trainset = self.data_train(self.data_params_file,self.model_type, 
                                            transform=JointTransforms(self.transformations),train_file=True,logger=self.logger)
            self.testset = self.data_train(self.data_params_file,self.model_type,
                                           transform=JointTransforms(self.transformations),train_file=False,logger=self.logger)

        self.trainloader = torch.utils.data.DataLoader(self.trainset, batch_size=self.data_dict['train_params']['batch_size'], shuffle=self.data_dict['train_params']['shuffle'], num_workers=self.data_dict['train_params']['num_workers'],worker_init_fn = lambda id: np.array(self.data_dict['train_params']['seed']))
        self.testloader = torch.utils.data.DataLoader(self.testset, batch_size=self.data_dict['test_params']['batch_size'], shuffle=self.data_dict['test_params']['shuffle'], num_workers=self.data_dict['test_params']['num_workers'],worker_init_fn = lambda id: np.array(self.data_dict['test_params']['seed']))
        return self.trainloader,self.testloader,self.trainset,self.testset

    def data_train(self,data,model_type,transform=None,train_file=True,**kwargs):
        """
        get train data from yaml file
        """
        data_t = customdl(data,model_type,transform=transform,train_file=train_file,**kwargs)
        return data_t