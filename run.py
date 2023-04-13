import torch
import argparse
import os, sys, json
from src.data import get_dataloaders
from src.engine import train_model

parser = argparse.ArgumentParser()

# Data Loading Related
parser.add_argument('--no_processed_data', default=False, type=lambda x: (str(x).lower() == 'true'),
                    help='Whether the raw data has been processed into X,y and idx_to_class')
parser.add_argument('--X_path', default='data/processed/X.pt', type=str,
                    help='path of X tensor')
parser.add_argument('--y_path', default='data/processed/y.pickle', type=str,
                    help='path of y list')
parser.add_argument('--idx_to_class_path', default='data/processed/idx_to_class.txt', type=str,
                    help='path of the idx_to_class dictionary')

# Data Tuning Related
parser.add_argument('--path', default='data/train', type=str,
                    help='path of the root data foler')
parser.add_argument('--smote', default=True, type=bool,
                    help='whether using smote for data augmentation')
parser.add_argument('--bz', default=32, type=int,
                    help='batch size')
parser.add_argument('--normalization_mean', default=(0.3272, 0.2874, 0.2038), type=tuple,
                    help='Mean value of z-scoring normalization for each channel in image')
parser.add_argument('--normalization_std', default=(0.0965, 0.1009, 0.1173), type=tuple,
                    help='Mean value of z-scoring standard deviation for each channel in image')
parser.add_argument('--brightness', default=(0.8,2), type=tuple,
                    help='Brightness range for data augmentation')
parser.add_argument('--noise_std', default=0.05, type=float,
                    help='Adding noise with guassian distribution for data augmentation')
parser.add_argument('--shuffle', default=True, type=bool,
                    help='whether to shuffle training data during optimization')

# Hardware Related
parser.add_argument('--device_id', default=0, type=int,
                    help='the id of the gpu to use')   

args = vars(parser.parse_args())

def main(args):

    print(f'CUDA availability: {torch.cuda.is_available()}')
    if torch.cuda.is_available():
        for i in range(torch.cuda.device_count()):
            print(f'GPU name: {torch.cuda.get_device_name(i)}')

    device = torch.device("cuda:{}".format(args['device_id']) if torch.cuda.is_available() else "cpu")

    if torch.cuda.is_available():
        print("using cuda:{}".format(args['device_id']))
    else:
         print("using {}".format(device))
    dataloaders = get_dataloaders(args['path'], args)
    train_model(dataloaders, args)
    
    
if __name__ == '__main__':
    main(args)