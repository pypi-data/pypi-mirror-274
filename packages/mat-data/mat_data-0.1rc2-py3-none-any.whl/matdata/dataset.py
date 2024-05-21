# -*- coding: utf-8 -*-
"""
**Multiple Aspect Trajectory Tools Framework**

*MAT-data: Data Preprocessing for Multiple Aspect Trajectory Data Mining*

The present application offers a tool, to support the user in the classification task of multiple aspect trajectories,
specifically for extracting and visualizing the movelets, the parts of the trajectory that better discriminate a class.
It integrates into a unique platform the fragmented approaches available for multiple aspects trajectories and in
general for multidimensional sequence classification into a unique web-based and python library system. Offers both
movelets visualization and classification methods.

Created on Dec, 2023
Copyright (C) 2023, License GPL Version 3 or superior (see LICENSE file)

@author: Tarlis Portela

----

"""
import os
import pandas as pd
import numpy as np
import requests
import subprocess
import tempfile, py7zr

from tqdm.auto import tqdm

from matdata.preprocess import organizeFrame, splitTIDs, readDataset, trainTestSplit, kfold_trainTestSplit

# Repository data on GitHub
USER = "mat-analysis"
REPOSITORY = "datasets"

# The 2 URLs are a workaround of GH delay in accessing raw files
REPO_URL_API = 'https://api.github.com/repos/{}/{}/contents/{}/{}/'
REPO_URL_RAW = 'https://raw.githubusercontent.com/{}/{}/main/{}/{}/'

DATASET_TYPES = {
    'mat':           'Multiple Aspect Trajectories', 
    'raw':           'Raw Trajectories', 
    'sequential':    'Sequential Semantics', 
    'log':           'Event Logs',
    'mts':           'Multivariate Time Series', 
    'uts':           'Univariate Time Series',
}

SUBSET_TYPES = {
   '*.specific':                     'Multiple',
   'mat.specific':                   'Multiple Aspect',
   'raw.specific':                   'Raw',
   'sequential.*':                   'Semantic',
   'mts.specific':                   'Multivariate',
   'uts.specific':                   'Univariate',
   'log.specific':                   'Event Log',
   'log.process':                    'Event Log', #Deprecated?
   'log.*':                          'Semantic',
    
   '*.raw':      'Spatio-Temporal',
    
   '*.spatial':  'Spatial',
   '*.geo_only': 'Spatial',
   '*.generic':  'Generic',
   '*.category': 'Category',
   '*.poi':      'POI',
   '*.5dims':    '5-Dimensions',
   '*.genes':    'Genetic Sequence',
}

###############################################################################
#   LOAD DATASETs - From https://github.com/mat-analysis/datasets/
###############################################################################
def prepare_ds(df, tid_col='tid', class_col=None, sample_size=1, random_num=1):
    """
    Prepare dataset for training or testing (helper function).

    Parameters:
    -----------
    df : pandas.DataFrame
        The DataFrame containing the dataset.
    tid_col : str, optional
        The name of the column representing trajectory IDs (default 'tid').
    class_col : str or None, optional
        The name of the column representing class labels. If None, no class column is used for ordering data (default None).
    sample_size : float, optional
        The proportion of the dataset to include in the sample (default 1, i.e., use the entire dataset).
    random_num : int, optional
        Random seed for reproducibility (default 1).

    Returns:
    --------
    pandas.DataFrame
        The prepared dataset with optional sampling.
    """
    
    if class_col:
        df.rename(columns={tid_col: 'tid', class_col: 'label'}, inplace=True)
        class_col = 'label'
        df.sort_values(['label', 'tid'])
    else:
        df.rename(columns={tid_col: 'tid'}, inplace=True)
        df.sort_values(['tid'])
    
    if sample_size < 1: # Stratify the data
        df_index, _, _ = splitTIDs(df, sample_size, random_num, 'tid', class_col, min_elements=2)

        df = df.loc[df['tid'].isin(df_index)]
        
    df, _, columns_order_csv = organizeFrame(df, None, 'tid', class_col)
        
    return df[columns_order_csv]

# ------------------------------------------------------------
## TODO: For now, all datasets on repository have tid and label columns. This can change in the future.
def load_ds(dataset='mat.FoursquareNYC', prefix='', missing='-999', sample_size=1, random_num=1):
    """
    Load a dataset for training or testing from a GitHub repository.

    Parameters:
    -----------
    dataset : str, optional
        The name of the dataset to load (default 'mat.FoursquareNYC').
    prefix : str, optional
        The prefix to be added to the dataset file name (default '').
    missing : str, optional
        The placeholder value used to denote missing data (default '-999').
    sample_size : float, optional
        The proportion of the dataset to include in the sample (default 1, i.e., use the entire dataset).
    random_num : int, optional
        Random seed for reproducibility (default 1).

    Returns:
    --------
    pandas.DataFrame
        The loaded dataset with optional sampling.
    """
    
    def is_file(dsc, dsn, file):
        url = REPO_URL_API.format(USER, REPOSITORY, dsc, dsn) + file
        try:
            resp = requests.head(url)
#            return resp.status_code == requests.codes.found
            return resp.status_code == requests.codes.ok
        except Exception as e:
            return False
        
    def url_is_file(url):
        try:
            resp = requests.head(url)
            return resp.status_code == requests.codes.found
#            return resp.status_code == requests.codes.ok
        except Exception as e:
            return False
        
    def download(url, tmpdir):
        file = os.path.join(tmpdir, os.path.basename(url))
        subprocess.run('curl -o {} {}'.format(file, url), shell=True, check=True)
#        response = requests.get(url, stream=True)
#        with open(os.path.join(tmpdir, os.path.basename(url)), 'wb') as out:
#            out.write(response.content)
#            #content = response.json()['content']
#            #out.write(base64.b64decode(content))
#            return True
        return True #False
    
    def read(url):
        df = pd.read_parquet(url)
        df.fillna(missing, inplace=True)

        return prepare_ds(df, tid_col='tid', class_col='label', sample_size=sample_size, random_num=random_num)
    
    # ------
    file = 'data.parquet'
    if prefix and prefix != '':
        file = prefix+'_data.parquet'
        
    dsc = dataset.split('.')[0]
    dsn = dataset.split('.')[1]
    
    base = REPO_URL_RAW.format(USER, REPOSITORY, dsc, dsn)
    
    # Try to load: 'data.parquet'
    url = base + file
    if is_file(dsc, dsn, file): # url_is_file(url):
        print("Loading dataset file: " + base)
#        return read(url)
        with tempfile.TemporaryDirectory() as tmpdir:
            download(url, tmpdir)
            return read(os.path.join(tmpdir, file))
    
    # Try to load compressed: 'data.parquet.7z'
    url = base + file +'.7z'
    if is_file(dsc, dsn, file+'.7z'): #url_is_file(url):
        print("Loading dataset compressed file: " + base)
        with tempfile.TemporaryDirectory() as tmpdir:
            download(url, tmpdir)
            filename = os.path.join(tmpdir, file +'.7z')

            with py7zr.SevenZipFile(filename, 'r') as archive:
                archive.extractall(path=tmpdir)
            
            print("Done.")
            print(" --------------------------------------------------------------------------------")
            return read(os.path.join(tmpdir, file))
        
    # Try to load compressed and splitted: 'data.parquet.7z.001-N'
    if is_file(dsc, dsn, file+'.001'): #url_is_file(url+'.001'):
        print("Loading dataset multi-volume files: " + base)
        with tempfile.TemporaryDirectory() as tmpdir:
            with open(os.path.join(tmpdir, file +'.7z'), 'ab') as outfile:  # append in binary mode
                i = 1
                while is_file(dsc, dsn, file+'.{:03d}'.format(i)) and download(url+'.{:03d}'.format(i), tmpdir):
                    with open(os.path.join(tmpdir, file+'.7z.{:03d}'.format(i)) , 'rb') as infile: # open in binary mode also
                        outfile.write(infile.read())
                    i += 1

            filename = os.path.join(tmpdir, file +'.7z')
            with py7zr.SevenZipFile(filename, 'r') as archive:
                archive.extractall(path=tmpdir)

            print("Done.")
            print(" --------------------------------------------------------------------------------")
            return read(os.path.join(tmpdir, file))
        
    raise Exception('Unable to load file, check the repository: ' + base)  
    
def load_ds_holdout(dataset='mat.FoursquareNYC', train_size=0.7, prefix='', missing='-999', sample_size=1, random_num=1):
    """
    Load a dataset for training and testing with a holdout method from a GitHub repository.

    Parameters:
    -----------
    dataset : str, optional
        The name of the dataset file to load from the GitHub repository (default 'mat.FoursquareNYC'). Format as `category.DatasetName`
    train_size : float, optional
        The proportion of the dataset to include in the training set (default 0.7).
    prefix : str, optional
        The prefix to be added to the dataset file name (default '').
    missing : str, optional
        The placeholder value used to denote missing data (default '-999').
    sample_size : float, optional
        The proportion of the dataset to include in the sample (default 1, i.e., use the entire dataset).
    random_num : int, optional
        Random seed for reproducibility (default 1).

    Returns:
    --------
    train : pandas.DataFrame
        The training dataset.
    test : pandas.DataFrame
        The testing dataset.
    """
    
    df = load_ds(dataset, prefix, missing, sample_size, random_num)
    
    # Class balanced train/ test split:
    train, test = trainTestSplit(df, train_size, random_num)
    
    return train, test
    
def load_ds_kfold(dataset='mat.FoursquareNYC', k=5, prefix='', missing='-999', sample_size=1, random_num=1):
    """
    Load a dataset for k-fold cross-validation from a GitHub repository.

    Parameters:
    -----------
    dataset : str, optional
        The name of the dataset file to load from the GitHub repository (default 'mat.FoursquareNYC').
    k : int, optional
        The number of folds for cross-validation (default 5).
    prefix : str, optional
        The prefix to be added to the dataset file name (default '').
    missing : str, optional
        The placeholder value used to denote missing data (default '-999').
    sample_size : float, optional
        The proportion of the dataset to include in the sample (default 1, i.e., use the entire dataset).
    random_num : int, optional
        Random seed for reproducibility (default 1).

    Returns:
    --------
    ktrain : list ofpandas.DataFrame
        The training datasets for each fold.
    ktest : list of pandas.DataFrame
        The testing datasets for each fold.
    """
    
    df = load_ds(dataset, prefix, missing, sample_size, random_num)
    
    # Class balanced f-fold train/ test split:
    ktrain, ktest = kfold_trainTestSplit(df, k, random_num)
    
    return ktrain, ktest

# ------------------------------------------------------------
def repository_datasets():
    """
    Read the datasets available in the repository and organize them by category.

    Returns:
    --------
    dict
        A dictionary containing lists of datasets, where each category is a key.
    """
    
    import requests
    
    url = "https://api.github.com/repos/{}/{}/git/trees/main?recursive=1".format(USER, REPOSITORY)
    r = requests.get(url)
    res = r.json()
    
    files = list(map(lambda file: file["path"], res["tree"]))
    datasets_dict = {}
    
    def create_dict(file):
        if file[-3:] == '.md' and '-stats.md' not in file and 'README' not in file and 'TODO' not in file:
            file = file.split(os.path.sep)
            category = file[0]
            if category not in datasets_dict.keys():
                datasets_dict[category] = []
                
            name = file[-1].split('.')[0]
            datasets_dict[category].append(name)
                
        return file
    
    file = list(map(lambda file: create_dict(file), files))
        
    return datasets_dict

###############################################################################
#   READ DATASETs - From local files
###############################################################################
def read_ds(data_file, tid_col='tid', class_col=None, missing='-999', sample_size=1, random_num=1):
    """
    Read a dataset from a file.

    Parameters:
    -----------
    data_file : str
        The path to the dataset file.
    tid_col : str, optional
        The name of the column representing trajectory IDs (default 'tid').
    class_col : str or None, optional
        The name of the column representing class labels. If None, no class column is used (default None).
    missing : str, optional
        The placeholder value used to denote missing data (default '-999').
    sample_size : float, optional
        The proportion of the dataset to include in the sample (default 1, i.e., use the entire dataset).
    random_num : int, optional
        Random seed for reproducibility (default 1).

    Returns:
    --------
    pandas.DataFrame
        The read dataset.
    """
    
    df = readDataset(data_file, class_col=class_col, tid_col=tid_col, missing=missing)
    
    return prepare_ds(df, tid_col, class_col, sample_size, random_num) 

def read_ds_5fold(data_path, prefix='specific', suffix='.csv', tid_col='tid', class_col=None, missing='-999'):
    """
    Read datasets for k-fold cross-validation from files in a directory.
    
    See Also
    --------
    read_ds_kfold : Read datasets for k-fold cross-validation.
    
    Parameters:
    -----------
    data_path : str
        The path to the directory containing the dataset files.
    prefix : str, optional
        The prefix of the dataset file names (default 'specific').
    suffix : str, optional
        The suffix of the dataset file names (default '.csv').
    tid_col : str, optional
        The name of the column representing trajectory IDs (default 'tid').
    class_col : str or None, optional
        The name of the column representing class labels. If None, no class column is used (default None).
    missing : str, optional
        The placeholder value used to denote missing data (default '-999').

    Returns:
    --------
    5_train : list ofpandas.DataFrame
        The training datasets for each fold.
    5_test : list of pandas.DataFrame
        The testing datasets for each fold.
    """

    return read_ds_kfold(data_path, 5, prefix, suffix, tid_col, class_col, missing)
    
def read_ds_kfold(data_path, k=5, prefix='specific', suffix='.csv', tid_col='tid', class_col=None, missing='-999'):
    """
    Read datasets for k-fold cross-validation from files in a directory.

    Parameters:
    -----------
    data_path : str
        The path to the directory containing the dataset files.
    k : int, optional
        The number of folds for cross-validation (default 5).
    prefix : str, optional
        The prefix of the dataset file names (default 'specific').
    suffix : str, optional
        The suffix of the dataset file names (default '.csv').
    tid_col : str, optional
        The name of the column representing trajectory IDs (default 'tid').
    class_col : str or None, optional
        The name of the column representing class labels. If None, no class column is used (default None).
    missing : str, optional
        The placeholder value used to denote missing data (default '-999').

    Returns:
    --------
    ktrain : list ofpandas.DataFrame
        The training datasets for each fold.
    ktest : list of pandas.DataFrame
        The testing datasets for each fold.
    """
    
    dsc = data_path.split(os.path.sep)[-2]
    dsn = data_path.split(os.path.sep)[-1]
    
    k_train = []
    k_test  = []
    
    for fold in tqdm(range(1, k+1), desc='Reading '+str(k)+'-fold dataset '+ dsn + ' of ' + translateCategory(dsn, dsc)):
        df_train, df_test = read_ds_holdout(data_path, prefix, suffix, tid_col, class_col, missing, fold)
        
        k_train.append(df_train)
        k_test.append(df_test)
        
    return k_train, k_test

def read_ds_holdout(data_path, prefix='specific', suffix='.csv', tid_col='tid', class_col=None, missing='-999', fold=None):
    """
    Read datasets for holdout validation from files in a directory.

    Parameters:
    -----------
    data_path : str
        The path to the directory containing the dataset files.
    prefix : str, optional
        The prefix of the dataset file names (default 'specific').
    suffix : str, optional
        The suffix of the dataset file names (default '.csv').
    tid_col : str, optional
        The name of the column representing trajectory IDs (default 'tid').
    class_col : str or None, optional
        The name of the column representing class labels. If None, no class column is used (default None).
    missing : str, optional
        The placeholder value used to denote missing data (default '-999').
    fold : int or None, optional
        The fold number to load for holdout validation, including subdirectory (ex. run1). If None, read files in `data_path`.

    Returns:
    --------
    train : pandas.DataFrame
        The training dataset.
    test : pandas.DataFrame
        The testing dataset.
    """
    
    dsc = data_path.split(os.path.sep)[-2]
    dsn = data_path.split(os.path.sep)[-1]

    if prefix and prefix != '':
        files = [prefix+'_train.csv', prefix+'_test'+suffix]
    else:
        files = ['train'+suffix, 'test'+suffix]
        
    if fold:
        files = [os.path.join('run'+str(fold), files[0]), os.path.join('run'+str(fold), files[1])]
    else:
        print('Reading dataset', dsn, 'of', translateCategory(dsn, dsc))
    
    dataset = []
    for file in tqdm(files, desc=dsn + ' (' + translateCategory(dsn, dsc) + \
                     ('), fold: '+str(fold) if fold else ')')):
#        url = BASE_URL + dsc+'/'+dsn+'/' + file
        url = os.path.join(data_path, file)
        df = read_ds(url, tid_col, class_col, missing)
        dataset.append(df)
    
    return dataset

# ------------------------------------------------------------
def translateDesc(dataset, category, descName):
    dst, dsn = descName.split('.')[0].split('_')[0:2]
    if dsn in ['allfeat', '5dims']:
        return False

    if getDescName(category, dataset) == dst:
        return dsn
    elif dataset in dst:
        return dsn
    return False

def translateCategory(dataset, category, descName=None):
    if descName:        
        if (category+'.'+descName) in SUBSET_TYPES.keys():
            return SUBSET_TYPES[category+'.'+descName]
        elif ('*.'+descName) in SUBSET_TYPES.keys():
            return SUBSET_TYPES['*.'+descName]
        elif (category+'.*') in SUBSET_TYPES.keys():
            return SUBSET_TYPES[category+'.*']
        else:
            return descName.capitalize()
        
    elif category in DATASET_TYPES.keys():
        return DATASET_TYPES[category]
    
    else:
        return category.split('_')[0].title()
    
# ------------------------------------------------------------
#def getName(dic, dst=None, dsn=None):
#    dst = (dst if dst else '*')
#    dsn = (dsn if dsn else '*')
#    if dst +'.'+ dsn in dic.keys():
#        name = dic[dst +'.'+ dsn]
#    elif dst +'.*' in dic.keys():
#        name = dic[dst +'.*']
#    elif '*.*' in dic.keys():
#        name = dic['*.*']
#        
#    if not name:
#        name = dsn 
#    return name
#
#def getDescName(dst, dsn):
#    name = getName(DESCRIPTOR_NAMES, dst, dsn)
#    if not name:
#        name = dsn
#    return name
#
#def getFeature(dst, dsn):
#    name = getName(FEATURES_NAMES, dst, dsn)
#    if not name:
#        name = ['poi']
#    return name
#
#def getSubset(dsn, feature):
#    for key, value in FEATURES_NAMES.items():
#        if dsn in key and feature in value:
#            if '?' in key:
#                return 'generic'
#            
#    return 'specific'