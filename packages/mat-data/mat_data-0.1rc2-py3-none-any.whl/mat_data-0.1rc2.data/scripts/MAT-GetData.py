#!python
# -*- coding: utf-8 -*-
"""
**Multiple Aspect Trajectory Tools Framework**

*MAT-data: Data Preprocessing for Multiple Aspect Trajectory Data Mining*

The present application offers a tool, to support the user in the classification task of multiple aspect trajectories,
specifically for extracting and visualizing the movelets, the parts of the trajectory that better discriminate a class.
It integrates into a unique platform the fragmented approaches available for multiple aspects trajectories and in
general for multidimensional sequence classification into a unique web-based and python library system. Offers both
movelets visualization and classification methods.

Created on May, 2024
Copyright (C) 2024, License GPL Version 3 or superior (see LICENSE file)

@author: Tarlis Portela

----

"""
import os
import argparse
from functools import reduce

from matdata.dataset import *
from matdata.converter import *

def parse_args():
    """[This is a function used to parse command line arguments]

    Returns:
        args ([object]): [Parse parameter object to get parse object]
    """
    parse = argparse.ArgumentParser(description='MAT-data: Downloader')
    parse.add_argument('data-path', type=str, help='path for the datasets')
    parse.add_argument('datasets', type=str, default='mat.FoursquareNYC', help='dataset names (comma separated)')
    parse.add_argument('-k', '--k', type=int, default=0, help='Number of subsets for: a) k-fold cross-validation (k > 1); b) hold-out train test split (k = 1); or c) no split (k = 0).')
    parse.add_argument('-f', '--format', type=str, default='parquet', help='output file format (csv, parquet, zip)')
    
    parse.add_argument('-r', '--random', type=int, default=1, help='random seed for reproducibility')
    parse.add_argument('-ts', '--train-size', type=float, default=0.7, help='proportion of the training set (default 0.7).')
    parse.add_argument('-sample', '--sample-size', type=float, default=1, help='proportion of the dataset to include in the sample (default 1, i.e., use the entire dataset)')

    args = parse.parse_args()
    config = vars(args)
    return config
 
config = parse_args()
#print(config)

data_path  = config["data-path"]
datasets   = config["datasets"].split(',')

k = config["k"]
random      = config["random"]
train_size  = config["train_size"]
sample_size = config["sample_size"]

outformat   = config["format"]

def getData(dataset, k, train_size, sample_size, random):
    name = dataset.split('.')[1]
    if k == 0:
        return {(name, 'data'): load_ds(dataset, sample_size=sample_size, random_num=random)}
    elif k == 1:
        train, test = load_ds_holdout(dataset, sample_size=sample_size, random_num=random)
        return {(name, 'train'): train, (name, 'test'): test}
    else:
        ktrain, ktest = load_ds_kfold(dataset, k, sample_size=sample_size, random_num=random)
        data      = dict(map(lambda i: ((name, f'run{i+1}','train'), ktrain[i]), range(len(ktrain))))
        data.update(dict(map(lambda i: ((name, f'run{i+1}','test'), ktest[i]), range(len(ktest)))))
        return data

def save(path, df):
    if len(path) > 2:
        file = path[2]
        path = os.path.join(data_path, path[0], path[1])
    else:
        file = path[1]
        path = os.path.join(data_path, path[0])
    
    if outformat == 'parquet':
        df2parquet(df, path, file)
    elif outformat == 'csv':
        df2csv(df, path, file)
    elif outformat == 'zip':
        df2zip(df, path, file)
    elif outformat == 'mat':
        df2mat(df, path, file)
        
    return (path, file)

print('[MAT-GetData]: Starting files download ...')

data_dict = list(map(lambda ds: getData(ds, k, train_size, sample_size, random), datasets))
data_dict = reduce(lambda a, b: {**a, **b}, data_dict)

list(map(lambda k: save(k[0], k[1]), data_dict.items()))

print("[MAT-GetData]: All Done.")
print(" --------------------------------------------------------------------------------")