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

from pathlib import Path
from tqdm.auto import tqdm
import glob2 as glob
import random

from sklearn.model_selection import KFold, train_test_split

from matdata.converter import *
#from .inc.script_def import getDescName

DS_FUNCTIONS = {
    '.csv': csv2df,
    '.parquet': parquet2df,
    '.zip': zip2df,
    '.mat': mat2df, #TODO
    '.ts': ts2df,
    '.xes': xes2df,
}

#-------------------------------------------------------------------------->>
def readDataset(data_path, folder=None, file='train.csv', class_col='label', tid_col='tid', missing='?'):
    """
    Reads a dataset file (CSV format by default, 'train.csv') and returns it as a pandas DataFrame.

    Parameters:
    -----------
    data_path : str
        The directory path where the dataset file is located.
    folder : str, optional
        The subfolder within the data path where the dataset file is located.
    file : str, optional (default='train.csv')
        The name of the dataset file to be read.
    class_col : str, optional (default='label')
        The name of the column to be treated as the class/label column.
    tid_col : str, optional (default='tid')
        The name of the column to be used as the trajectory identifier.
    missing : str, optional (default='?')
        The placeholder for missing values in the dataset.

    Returns:
    --------
    pandas.DataFrame
        A DataFrame containing the dataset from the specified file, with trajectory identifier,
        class label, and missing values handled as specified.
    """
    
    if folder:
        url = os.path.join(data_path, folder)
    else:
        url = data_path
        
    ext = Path(url).suffix
    if '' == ext:
        url = os.path.join(url, file)
        
    ext = Path(url).suffix
    if '' == ext:
        url = url + '.csv'
    
    url = os.path.abspath(url)
    ext = Path(url).suffix
    
    df = DS_FUNCTIONS[ext](url, class_col=class_col, tid_col=tid_col, missing=missing)
    
    return df

def organizeFrame(df, columns_order=None, tid_col='tid', class_col='label', make_spatials=False):
    """
    Organizes a DataFrame by reordering columns and optionally converting spatial columns.

    Parameters:
    -----------
    df : pandas.DataFrame
        The DataFrame to be organized.
    columns_order : list of str, optional
        A list of column names specifying the desired order of columns. If None, no reordering is performed.
    tid_col : str, optional (default='tid')
        The name of the column to be used as the trajectory identifier.
    class_col : str, optional (default='label')
        The name of the column to be treated as the class/label column.
    make_spatials : bool, optional (default=False)
        A flag indicating whether to convert spatial columns to both lat/lon separated or space format, which is the lat/lon concatenated in one column.

    Returns:
    --------
    pandas.DataFrame
        A DataFrame containing the organized data, with columns added as specified
        and spatial columns converted if requested.
    columns_order_zip
        A list of the columns with space column, if present.
    columns_order_csv
        A list of the columns with lat/lon columns, if present.
    """
    
    if make_spatials and (set(df.columns) & set(['lat', 'lon'])) and not 'space' in df.columns:
        df.loc[:, 'space'] = df["lat"].astype(str)  + ' ' + df["lon"].astype(str) 

        if columns_order is not None:
            columns_order.insert(columns_order.index('lon')-1, 'space')
            
    elif make_spatials and ('space' in df.columns or 'lat_lon' in df.columns) and not (set(df.columns) & set(['lat', 'lon'])):
        if 'lat_lon' in df.columns:
            df.rename(columns={'lat_lon': 'space'}, inplace=True)
            if columns_order is not None:
                columns_order[columns_order.index('lat_lon')] = 'space'
        
        ll = df['space'].str.split(" ", n = 1, expand = True) 
        df["lat"]= ll[0].astype(float)
        df["lon"]= ll[1].astype(float)
        
        if columns_order is not None:
            columns_order.insert(columns_order.index('space'), 'lat')
            columns_order.insert(columns_order.index('space')+1, 'lon')
    
    # For Columns ordering:
    if columns_order is None:
        columns_order = df.columns
            
    if class_col and class_col in df.columns:
        columns_order = [x for x in columns_order if x not in [tid_col, class_col]]
        columns_order = columns_order + [tid_col, class_col]
    else:
        columns_order = [x for x in columns_order if x not in [tid_col]]
        columns_order = columns_order + [tid_col]
            
    columns_order_zip = [x for x in columns_order if x not in ['lat', 'lon']]
    columns_order_csv = [x for x in columns_order if x not in ['space']]
    
    return df, columns_order_zip, columns_order_csv

#-------------------------------------------------------------------------->>
def trainTestSplit(df, train_size=0.7, random_num=1, tid_col='tid', class_col='label', fileprefix='', \
                      data_path='.', outformats=[], verbose=False, organize_columns=True):
    """
    Splits a DataFrame into training and testing sets, optionally organizes columns, and saves them to files.

    Parameters:
    -----------
    df : pandas.DataFrame
        The DataFrame to be split into training and testing sets.
    train_size : float, optional (default=0.7)
        The proportion of the dataset to include in the training set.
    random_num : int, optional (default=1)
        The random seed for reproducible results.
    tid_col : str, optional (default='tid')
        The name of the column to be used as the trajectory identifier.
    class_col : str, optional (default='label')
        The name of the column to be treated as the class/label column.
    fileprefix : str, optional (default='')
        The prefix to be added to the file names when saving.
    data_path : str, optional (default='.')
        The directory path where the output files will be saved.
    outformats : list of str, optional
        A list of output formats for saving the datasets (e.g., ['csv', 'parquet']).
    verbose : bool, optional (default=False)
        A flag indicating whether to display progress messages.
    organize_columns : bool, optional (default=True)
        A flag indicating whether to organize columns before saving.

    Returns:
    --------
    train : pandas.DataFrame
        A DataFrame containing the training set.
    test : pandas.DataFrame
        A DataFrame containing the testing set.
    """
    
    #outformats=['zip', 'csv', 'mat']
    if verbose:
        print(str(train_size)+"% train and test split ... ")
    
    if organize_columns:
        df, columns_order_zip, columns_order_csv = organizeFrame(df, None, tid_col, class_col)
    else:
        columns_order_zip = list(df.columns)
        columns_order_csv = list(df.columns)
    
    train_index, test_index, _ = splitTIDs(df, train_size, random_num, tid_col, class_col, min_elements=1)
    
    train = df.loc[df[tid_col].isin(train_index)]
    test  = df.loc[df[tid_col].isin(test_index)]
    
    # WRITE Train / Test Files
    for outType in outformats:
        writeFiles(data_path, fileprefix, train, test, tid_col, class_col, \
                 columns_order_zip if outType in ['zip', 'mat'] else columns_order_csv, outformat=outType)

    if verbose:
        print("Done.")
        print(" --------------------------------------------------------------------------------")
    return train, test

def kfold_trainTestSplit(df, k, random_num=1, tid_col='tid', class_col='label', fileprefix='', columns_order=None, ktrain=None, ktest=None, mat_columns=None, data_path='.', outformats=[], verbose=False):
    """
    Splits a DataFrame into k folds for k-fold cross-validation, optionally organizes columns, and saves them to files.

    Parameters:
    -----------
    df : pandas.DataFrame
        The DataFrame to be split into k folds.
    k : int
        The number of folds for cross-validation.
    random_num : int, optional (default=1)
        The random seed for reproducible results.
    tid_col : str, optional (default='tid')
        The name of the column to be used as the trajectory identifier.
    class_col : str, optional (default='label')
        The name of the column to be treated as the class/label column.
    fileprefix : str, optional (default='')
        The prefix to be added to the file names when saving, for example: 'specific_' or 'generic_'.
    columns_order : list of str, optional
        A list of column names specifying the desired order of columns. If None, no reordering is performed.
    ktrain : list of pandas.DataFrame, optional
        A list of training sets for each fold. If None, the function will split the data into training and testing sets.
    ktest : list of pandas.DataFrame, optional
        A list of testing sets for each fold. If None, the function will split the data into training and testing sets.
    mat_columns : list of str, optional
        A list of column names to be included in the .mat files, corresponding to `columns_order`.
    data_path : str, optional (default='.')
        The directory path where the output files will be saved.
    outformats : list of str, optional
        A list of output formats for saving the datasets (e.g., ['csv', 'zip', 'parquet']).
    verbose : bool, optional (default=False)
        A flag indicating whether to display progress messages.

    Returns:
    --------
    ktrain : list of pandas.DataFrame
        List of DataFrame containing the training sets.
    ktest : list of pandas.DataFrame
        List of DataFrame containing the testing sets.
    """

  
    if verbose:
        print(str(k)+"-fold train and test split ... ")
    
    df, columns_order_zip, columns_order_csv = organizeFrame(df, columns_order, tid_col, class_col)
    
    if not ktrain:
        ktrain, ktest = splitData(df, k, random_num, tid_col, class_col)
    elif verbose:
        print("Train and test data provided.")
    
    if len(outformats) > 0:
        for x in range(k):            
            train_aux = ktrain[x]
            test_aux  = ktest[x]

            for outType in outformats:
                if verbose:
                    print("Writing", outType, "files ... " + str(x+1) +'/'+str(k))
                path = 'run'+str(x+1)
                if not os.path.exists(os.path.join(data_path, path)):
                    os.makedirs(os.path.join(data_path, path))

                writeFiles(data_path, os.path.join(path, fileprefix), train_aux, test_aux, tid_col, class_col, \
                         columns_order_zip if outType in ['zip', 'mat'] else columns_order_csv, mat_columns, None, \
                         outType, opSuff=str(x+1))
    if verbose:
        print("Done.")
        print(" --------------------------------------------------------------------------------")
    
    return ktrain, ktest

def stratify(df, sample_size=0.5, train_size=0.7, random_num=1, tid_col='tid', class_col='label', 
             organize_columns=True, mat_columns=None, fileprefix='', outformats=[], data_path='.'):  
    """
    Stratifies a DataFrame by class label and splits it into training and testing sets, optionally organizes columns, and saves them to files.

    Parameters:
    -----------
    df : pandas.DataFrame
        The DataFrame to be stratified and split into training and testing sets.
    sample_size : float, optional (default=0.5)
        The proportion of the dataset to sample for stratification.
    train_size : float, optional (default=0.7)
        The proportion of the stratified dataset to include in the training set.
    random_num : int, optional (default=1)
        The random seed for reproducible results.
    tid_col : str, optional (default='tid')
        The name of the column to be used as the trajectory identifier.
    class_col : str, optional (default='label')
        The name of the column to be treated as the class/label column.
    organize_columns : bool, optional (default=True)
        A flag indicating whether to organize columns before saving.
    mat_columns : list of str, optional (unused for now)
        A list of column names to be included in the .mat files, if set to save.
    fileprefix : str, optional (default='')
        The prefix to be added to the file names when saving.
    outformats : list of str, optional
        A list of output formats for saving the datasets (e.g., ['csv', 'zip', 'parquet']).
    data_path : str, optional (default='.')
        The directory path where the output files will be saved.

    Returns:
    --------
    train : pandas.DataFrame
        A DataFrame containing the training set.
    test : pandas.DataFrame
        A DataFrame containing the testing set.
    """
    
    train_index, _, _ = splitTIDs(df, sample_size, random_num, tid_col, class_col, min_elements=2)
    
    df = df.loc[df[tid_col].isin(train_index)].copy()
    
    train_index, test_index, _ = splitTIDs(df, train_size, random_num, tid_col, class_col, min_elements=1)
    
    if organize_columns:
        df, columns_order_zip, columns_order_csv = organizeFrame(df, None, tid_col, class_col)
    else:
        columns_order_zip = list(df.columns)
        columns_order_csv = list(df.columns)
    
    train = df.loc[df[tid_col].isin(train_index)]
    test  = df.loc[df[tid_col].isin(test_index)]
    
    for outType in outformats:
        path = 'S'+str(int(sample_size*100))
        if not os.path.exists(os.path.join(data_path, path)):
                os.makedirs(os.path.join(data_path, path))
            
        writeFiles(data_path, os.path.join(path, fileprefix), train, test, tid_col, class_col, \
                 columns_order_zip if outType in ['zip', 'mat'] else columns_order_csv, mat_columns, None, outType, opSuff=path)
    
    return train, test
    
# TODO fix stratify:
def kfold_stratify(df, k=10, inc=1, limit=10, random_num=1, tid_col='tid', class_col='label', fileprefix='', 
             ktrain=None, ktest=None, organize_columns=True, mat_columns=None, data_path='.', outformats=[], ignore_ltk=True):
   
    print(str(k)+"-fold stratification of train and test ... ")
    
    if organize_columns:
        df, columns_order_zip, columns_order_csv = organizeFrame(df, None, tid_col, class_col)
    else:
        columns_order_zip = list(df.columns)
        columns_order_csv = list(df.columns)
        
    if not ktrain:
        ktrain, ktest = splitData(df, k, random_num, tid_col, class_col, ignore_ltk=ignore_ltk)
    else:
        print("Train and test data provided.")
    
    for x in range(0, limit, inc):
        
        train_aux = ktrain[0]
        test_aux  = ktest[0]
        for y in range(1, x+1):
            train_aux = pd.concat([train_aux,  ktrain[y]])
            test_aux  = pd.concat([test_aux,   ktest[y]])
            
        for outType in outformats:
            path = 'S'+str((x+1)*int(100/k))

            if not os.path.exists(os.path.join(data_path, path)):
                os.makedirs(os.path.join(data_path, path))
            
            writeFiles(data_path, os.path.join(path, fileprefix), train_aux, test_aux, tid_col, class_col, \
                     columns_order_zip if outType in ['zip', 'mat'] else columns_order_csv, mat_columns, None, outType, opSuff=str(x+1))
    print(" Done.")
    print(" --------------------------------------------------------------------------------")
    
    return ktrain, ktest

def klabels_stratify(df, kl=10, train_size=0.7, random_num=1, tid_col='tid', class_col='label', 
             organize_columns=True, mat_columns=None, fileprefix='', outformats=[], data_path='.'):
    """
    Stratifies a DataFrame by a specified number of class labels and splits it into training and testing sets,
    optionally organizes columns, and saves them to files.

    Parameters:
    -----------
    df : pandas.DataFrame
        The DataFrame to be stratified and split into training and testing sets.
    kl : int, optional (default=10)
        The number of class labels to stratify the DataFrame.
    train_size : float, optional (default=0.7)
        The proportion of the stratified dataset to include in the training set.
    random_num : int, optional (default=1)
        The random seed for reproducible results.
    tid_col : str, optional (default='tid')
        The name of the column to be used as the trajectory identifier.
    class_col : str, optional (default='label')
        The name of the column to be treated as the class/label column.
    organize_columns : bool, optional (default=True)
        A flag indicating whether to organize columns before saving.
    mat_columns : list of str, optional (unused for now)
        A list of column names to be included in the .mat files, if set to save.
    fileprefix : str, optional (default='')
        The prefix to be added to the file names when saving.
    outformats : list of str, optional
        A list of output formats for saving the datasets (e.g., ['csv', 'zip', 'parquet']).
    data_path : str, optional (default='.')
        The directory path where the output files will be saved.

    Returns:
    --------
    train : pandas.DataFrame
        A DataFrame containing the training set.
    test : pandas.DataFrame
        A DataFrame containing the testing set.
    """

    min_elements=1
    
    random.seed(random_num)
    labels = df[class_col].unique()

    n = min_elements if kl < min_elements else kl

    labels_index = random.sample(list(labels), n)
    df = df.loc[df[class_col].isin(labels_index)].copy()
    
    train_index, test_index, _ = splitTIDs(df, train_size, random_num, tid_col, class_col, min_elements=min_elements)
    
    if organize_columns:
        df, columns_order_zip, columns_order_csv = organizeFrame(df, None, tid_col, class_col)
    else:
        columns_order_zip = list(df.columns)
        columns_order_csv = list(df.columns)
    
    train = df.loc[df[tid_col].isin(train_index)]
    test  = df.loc[df[tid_col].isin(test_index)]
    
    for outType in outformats:
        path = 'L'+str(n)
        if not os.path.exists(os.path.join(data_path, path)):
                os.makedirs(os.path.join(data_path, path))
                
        writeFiles(data_path, os.path.join(path, fileprefix), train, test, tid_col, class_col, \
                 columns_order_zip if outType in ['zip', 'mat'] else columns_order_csv, mat_columns, None, outType, opSuff=path)
    
    return train, test

def joinTrainTest(dir_path, train_file="train.csv", test_file="test.csv", tid_col='tid', class_col = 'label', to_file=False): 
    """
    Joins training and testing datasets from separate files into a single DataFrame.

    Parameters:
    -----------
    dir_path : str
        The directory path where the training and testing files are located.
    train_file : str, optional (default="train.csv")
        The name of the training file to be read.
    test_file : str, optional (default="test.csv")
        The name of the testing file to be read.
    tid_col : str, optional (default='tid')
        The name of the column to be used as the trajectory identifier.
    class_col : str, optional (default='label')
        The name of the column to be treated as the class/label column.
    to_file : bool, optional (default=False)
        A flag indicating whether to save the joined DataFrame to a file, and saves the joined DataFrame to a file named 'joined.csv'.

    Returns:
    --------
    pandas.DataFrame
        A DataFrame containing the joined training and testing data.
        If `to_file` is True, returns the DataFrame and saves the joined DataFrame to a file named 'joined.csv'.
    """
    
    print("Joining train and test data from... " + dir_path)
    
    # Read datasets
    dataset_train = readDataset(dir_path, None, train_file)
    dataset_test  = readDataset(dir_path, None, test_file)
    
    dataset = pd.concat([dataset_train, dataset_test])
    dataset.sort_values([class_col, tid_col])
    
    if to_file:
        print("Saving joined dataset as: " + os.path.join(dir_path, 'joined.csv'))
        dataset.to_csv(os.path.join(dir_path, 'joined.csv'), index=False)
        
    print("Done.")
    print(" --------------------------------------------------------------------------------")
    
    return dataset

#-------------------------------------------------------------------------->> DESCRIPTORS
def readDsDesc(data_path, folder=None, file='train.csv', tid_col='tid', class_col='label', missing='?'):
    # TODO Deprecated
    
    df = readDataset(data_path, folder, file, class_col, missing)
    
    columns_order = [x for x in df.columns if x not in [tid_col, class_col]]
    df = df[columns_order + [tid_col, class_col]]
    
    if folder == None:
        folder = os.path.basename(data_path)
        data_path = os.path.dirname(data_path)
    
    return df

def featuresJSON(df, version=1, deftype='nominal', defcomparator='equals', tid_col='tid', label_col='label', file=False):
    """
    Generates a JSON representation of features from a DataFrame.

    Parameters:
    -----------
    df : pandas.DataFrame
        The DataFrame containing the dataset.
    version : int, optional (default=1)
        The version number of the JSON schema (1 for MASTERMovelets format, 2 for HiPerMovelets format).
    deftype : str, optional (default='nominal')
        The default type of features.
    defcomparator : str, optional (default='equals')
        The default comparator for features.
    tid_col : str, optional (default='tid')
        The name of the column to be used as the trajectory identifier.
    label_col : str, optional (default='label')
        The name of the column to be treated as the class/label column.
    file : bool, optional (default=False)
        A flag indicating whether to save the JSON representation to a file.

    Returns:
    --------
    str
        If `file` is False, returns a str representing the features in JSON format.
        If `file` is str, returns a str of JSON features and saves the JSON representation to a `file` param name.
    """
    
    if isinstance(df, list):
        cols = {x: deftype for x in df}
    elif isinstance(df, dict):
        cols = df
    else:
        cols = descTypes(df)
    
    if tid_col not in cols.keys() or label_col not in cols.keys():
        aux = {tid_col: 'numeric', label_col: 'nominal'}
        cols = {**aux, **cols}
            
    if version == 1:
        s = '{\n   "readsDesc": [\n'

        order = 1
        for f, deftype in cols.items():
            s += ('    {\n          "order": '+str(order)+',\n          "type": "'+deftype+'",\n          "text": "'+f+'"\n    }')
            if len(cols) == order:
                s += ('\n')
            else:
                s += (',\n')
            order += 1

        s += ('    ],\n    "pointFeaturesDesc": [],\n    "subtrajectoryFeaturesDesc": [],\n')
        s += ('    "trajectoryFeaturesDesc": [],\n    "pointComparisonDesc": {\n      "pointDistance": "euclidean",\n')
        s += ('      "featureComparisonDesc": [\n')

        order = 1
        for f, deftype in cols.items():
            if f != tid_col and f != label_col:
                s += ('            {\n              "distance": "'+defcomparator+'",\n              "maxValue": -1,\n              "text": "'+f+'"\n            }')
                if len(cols)-1 == order:
                    s += ('\n')
                else:
                    s += (',\n')
            order += 1

        s += ('        ]\n    },\n    "subtrajectoryComparisonDesc": {\n        "subtrajectoryDistance": "euclidean",\n')
        s += ('        "featureComparisonDesc": [\n            {\n              "distance": "euclidean",\n              "text": "points"\n')
        s += ('            }\n        ]\n    }\n}')
    else: # VERSION 2 (*_hp.json)      
        s  = '{\n   "input": {\n          "train": ["train"],\n          "test": ["test"],\n          "format": "CSV",\n'
        s += '          "loader": "interning"\n   },\n'
        s += '   "idFeature": {\n          "order": '+str(list(cols.keys()).index(tid_col)+1)+',\n          "type": "numeric",\n          "text": "'+tid_col+'"\n    },\n'
        s += '   "labelFeature": {\n          "order": '+str(list(cols.keys()).index(label_col)+1)+',\n          "type": "nominal",\n          "text": "label"\n    },\n'
        s += '   "attributes": [\n'
        
        order = 1
        for f, deftype in cols.items():
            if f != tid_col and f != label_col:
                s += '        {\n              "order": '+str(order)+',\n              "type": "'+deftype+'",\n              "text": "'+str(f)+'",\n              "comparator": {\n                "distance": "'+defcomparator+'"\n              }\n        }'
                if len(cols)-1 == order:
                    s += ('\n')
                else:
                    s += (',\n')
            order += 1
        s += '    ]\n}'
        
    if file:
        file = open(file, 'w')
        print(s, file=file)
        file.close()
    else:
        print(s)
    
#-------------------------------------------------------------------------->> STATISTICS
def countClasses(data_path, folder, file='train.csv', tid_col = 'tid', class_col = 'label', markd=False):
    """
    Counts the occurrences of each class label in a dataset.

    Parameters:
    -----------
    data_path : str
        The directory path where the dataset file is located.
    folder : str
        The subfolder within the data path where the dataset file is located.
    file : str, optional (default='train.csv')
        The name of the dataset file to be read.
    tid_col : str, optional (default='tid')
        The name of the column to be used as the trajectory identifier.
    class_col : str, optional (default='label')
        The name of the column to be treated as the class/label column.
    markd : bool, optional (default=False)
        A flag indicating whether to print the class counts in Markdown format.

    Returns:
    --------
    pandas.DataFrame or str
        If `markd` is False, prins the markdown text and returns a dictionary DataFrame containing the counts of each class label in the dataset.
        If `markd` is True, returns str markdown of the counts of each class label in the dataset.
    """
    
    df = readDataset(data_path, folder, file, class_col, tid_col, markd)
    return countClasses_df(df, tid_col, class_col, markd)

def countClasses_df(df, tid_col = 'tid', class_col = 'label', markd=False):
    group = df.groupby([class_col, tid_col])
    df2 = group.apply(lambda x: ', '.join([str(s) for s in list(x[class_col].unique())]))
    md = "Number of Samples: " + str(len(df[tid_col].unique()))
    md += '\n\r'
    md += "Samples by Class:"
    md += '\n\r'
        
    if markd:
        md += '\n\r'
        md += df2.value_counts().to_markdown(tablefmt="github", headers=["Label", "#"])
        return md
    else:
        print(md)
        print(df2.value_counts())
        return df2.value_counts()

def dfVariance(df):
    """
    Computes the variance for each column in a DataFrame.

    Parameters:
    -----------
    df : pandas.DataFrame
        The DataFrame for which variance is to be computed.

    Returns:
    --------
    pandas.Series
        A Series containing the variance for each column in the DataFrame.
    """
    
    stats=pd.DataFrame()
    dfx = df.apply(pd.to_numeric, args=['coerce'])
    #stats["Mean"]=dfx.mean(axis=0, skipna=True)
    #stats["Std.Dev"]=dfx.std(axis=0, skipna=True)
    stats["Variance"]=dfx.var(axis=0, skipna=True)

    dfx = df.fillna('?')
    for col in df.columns:
        if not np.issubdtype(dfx[col].dtype, np.number):
            categories = list(dfx[col].unique())
            dfx[col] = pd.Categorical(dfx[col], categories, ordered=True)
            #stats["Mean"][col] = categories[int( np.median(dfx[col].cat.codes) )]
            #stats["Std.Dev"][col] = np.std(dfx[col].cat.codes)
            stats["Variance"][col] = np.var(dfx[col].cat.codes)
    
    return stats.sort_values('Variance', ascending=False)

def dfStats(df):
    """
    Computes summary statistics for each column in a DataFrame.

    Parameters:
    -----------
    df : pandas.DataFrame
        The DataFrame for which statistics are to be computed.

    Returns:
    --------
    pandas.DataFrame
        A DataFrame containing summary statistics for each column, including mean, standard deviation,
        and variance. Columns are sorted by variance in descending order.
    """
    
    stats=pd.DataFrame()
    dfx = df.apply(pd.to_numeric, args=['coerce'])
    stats["Mean"]=dfx.mean(axis=0, skipna=True)
    stats["Std.Dev"]=dfx.std(axis=0, skipna=True)
    stats["Variance"]=dfx.var(axis=0, skipna=True)

    dfx = df.fillna('?')
    for col in df.columns:
        if not np.issubdtype(dfx[col].dtype, np.number):
            categories = list(dfx[col].unique())
            dfx[col] = pd.Categorical(dfx[col], categories, ordered=True)
            stats["Mean"][col] = categories[int( np.median(dfx[col].cat.codes) )]
            stats["Std.Dev"][col] = np.std(dfx[col].cat.codes)
            stats["Variance"][col] = np.var(dfx[col].cat.codes)
    
    return stats.sort_values('Variance', ascending=False)
    
def datasetStatistics(data_path, folder, file_prefix='', tid_col = 'tid', class_col = 'label', to_file=False):
    """
    Computes statistics for a dataset, including summary statistics for each column and class distribution into a markdown file format.

    Parameters:
    -----------
    data_path : str
        The directory path where the dataset file(s) are located.
    folder : str
        The subfolder within the data path where the dataset file(s) are located.
    file_prefix : str, optional (default='')
        The prefix to be added to the dataset file names.
    tid_col : str, optional (default='tid')
        The name of the column to be used as the trajectory identifier.
    class_col : str, optional (default='label')
        The name of the column to be treated as the class/label column.
    to_file : bool, optional (default=False)
        A flag indicating whether to save the statistics to a file.

    Returns:
    --------
    dict or None
        If `to_file` is False, prints markdown and returns a str containing the computed statistics.
        If `to_file` is str, returns markdown str and saves the statistics to a file named as in `to_file` value.
    """

    def addLine(i):
        return '\n\r' + ('&nbsp;'.join(['\n\r' for x in range(i)])) + '\n\r'
    
    train = readDsDesc(data_path, folder, file_prefix+'train.csv', tid_col, class_col, missing='NaN')
    test = readDsDesc(data_path, folder, file_prefix+'test.csv', tid_col, class_col, missing='NaN')
    
    md = '##### Descriptive Statistics for ' + folder
    
    sam_train = len(train.tid.unique())
    sam_test  = len(test.tid.unique())
    points    = len(train) + len(test)
    samples = sam_train + sam_test
    top_train = train.groupby(['tid']).count().sort_values('label').tail(1)['label'].iloc[0]
    bot_train = train.groupby(['tid']).count().sort_values('label').head(1)['label'].iloc[0]
    top_test  = test.groupby(['tid']).count().sort_values('label').tail(1)['label'].iloc[0]
    bot_test  = test.groupby(['tid']).count().sort_values('label').head(1)['label'].iloc[0]
    classes = train[class_col].unique()
    avg_size = points / samples
    diff_size = max( avg_size - min(bot_train, bot_test) , max(top_train, top_test) - avg_size )
    
    stats_df = pd.DataFrame({
        'Number of Classes': [len(classes), '-', '-'],
        'Number of Attributes': [len(train.columns), '-', '-'],
        'Avg Size of Trajs': ['{:.2f}'.format(avg_size) + ' / ±' + str(diff_size), '-', '-'],
        'Number of Trajs': [str(samples), str(sam_train), str(sam_test)],
        'Hold-out': ['100%', '{:.2f}%'.format(sam_train*100/samples),
                     '{:.2f}%'.format(sam_test*100/samples)],
        'Number of Points': [str(points), str(len(train)), str(len(test))],
        'Longest Size':  [str(max(top_train, top_test)), str(top_train), str(top_test)],
        'Shortest Size': [str(max(bot_train, bot_test)), str(bot_train), str(bot_test)],
    }, index=['Total', 'Train', 'Test'])
    
    md += addLine(1)
    md += stats_df.to_markdown(tablefmt="github", colalign="right")
    md += addLine(2)
    
#     print('\n--------------------------------------------------------------------')
    md += '###### Attributes: '
    md += ', '.join([str(x) for x in train.columns])
    md += addLine(1)
    md += '###### Labels: '
#     md += addLine(1)
    md += ', '.join([str(x) for x in classes])
    md += addLine(2)
    
#     md += addLine(2)
    df = pd.concat([train, test])
    df.drop(['tid'], axis=1, inplace=True)
    stats = df.describe(include='all').fillna('')
    md += stats.to_markdown(tablefmt="github")
    md += addLine(2)
    
    md += 'Descriptive Statistics (by Variance): '
    md += addLine(1)
    #stats=pd.DataFrame()
    #dfx = df.apply(pd.to_numeric, args=['coerce'])
    #stats["Mean"]=dfx.mean(axis=0, skipna=True)
    #stats["Std.Dev"]=dfx.std(axis=0, skipna=True)
    #stats["Variance"]=dfx.var(axis=0, skipna=True)
#
    #df.fillna('?', inplace=True)
    #for col in df.columns:
    #    if not np.issubdtype(df[col].dtype, np.number):
    #        categories = list(df[col].unique())
    #        df[col] = pd.Categorical(df[col], categories, ordered=True)
    #        stats["Mean"][col] = categories[int( np.median(df[col].cat.codes) )]
    #        stats["Std.Dev"][col] = np.std(df[col].cat.codes)
    #        stats["Variance"][col] = np.var(df[col].cat.codes)
    
    md += dfStats(df).to_markdown(tablefmt="github")
    #md += stats.sort_values('Variance', ascending=False).to_markdown(tablefmt="github")
    md += addLine(2)
    
    
    if len(classes) < 15:
    #     print('\n--------------------------------------------------------------------')
        md += '###### Labels for TRAIN:'
        md += addLine(1)
        md += countClasses_df(train, markd=True)
        md += addLine(2)
    #     md += train.describe().to_markdown(tablefmt="github")
    #     md += addLine(2)

    #     print('\n--------------------------------------------------------------------')
        md += '###### Labels for TEST.:'
        md += addLine(1)
        md += countClasses_df(test, markd=True)
#         md += addLine(2)
    #     md += test.describe().to_markdown(tablefmt="github")
    #     md += addLine(2)
    
    if to_file:
        f = open(to_file, "w")
        f.write(f''+md)
        f.close()
    else:
        print('\n--------------------------------------------------------------------')
        print(md)
    return md

#-------------------------------------------------------------------------->> HELPERS
def splitTIDs(df, train_size=0.7, random_num=1, tid_col='tid', class_col='label', min_elements=1):
    train = list()
    test = list()
    
    df_ = df.groupby(tid_col).first().reset_index()[[tid_col, class_col]]
    
    def splitByLabel(label):
        nonlocal df_, train, test
        tids = df_.loc[df_[class_col] == label][tid_col].unique()
        random.seed(random_num)
        
        n = int(float(len(tids))*train_size)
        n = min_elements if n < min_elements else n
            
        train_index = random.sample(list(tids), n)
        test_index  = tids[np.isin(tids, train_index, invert=True)]
        
        train = train + list(train_index)
        test  = test  + list(test_index)
        
    list(map(lambda label: splitByLabel(label), tqdm(df_[class_col].unique())))
    
    return train, test, df_

def splitData(df, k, random_num, tid_col='tid', class_col='label', opLabel='Spliting Data', ignore_ltk=True):
    
    if ignore_ltk: # removes labels with less than k trajectories...
        df = dropLabelsltk(df, k, tid_col, class_col)
    
    ktrain = []
    ktest = []
    for x in range(k):
        ktrain.append( pd.DataFrame() )
        ktest.append( pd.DataFrame() )

    kfold = KFold(n_splits=k, shuffle=True, random_state=random_num)

    def addData(label):
        tids = df.loc[df[class_col] == label][tid_col].unique()
        x = 0
        for train_idx, test_idx in kfold.split(tids):
            ktrain[x] = pd.concat([ktrain[x], df.loc[df[tid_col].isin(tids[train_idx])]])
            ktest[x]  = pd.concat([ktest[x],  df.loc[df[tid_col].isin(tids[test_idx])]])
            x += 1
    list(map(lambda label: addData(label), tqdm(df[class_col].unique(), desc=opLabel)))
    
    return ktrain, ktest

def dropLabelsltk(df, k, tid_col='tid', class_col='label'):
    df_ = df.groupby(by=class_col, as_index=False).agg({tid_col: pd.Series.nunique})
    index_names = df[df[class_col].isin(df_[df_[tid_col] < k][class_col])].index
    return df.drop(index_names)

def labels_extract(df, labels=[], tid_col='tid', class_col='label', organize_columns=True):

    df = df.loc[df[class_col].isin(labels)].copy()
    
    if organize_columns:
        df, columns_order_zip, columns_order_csv = organizeFrame(df, None, tid_col, class_col)
    else:
        columns_order_zip = list(df.columns)
        columns_order_csv = list(df.columns)
    
    return df
        
def writeFile(data_path, df, file, tid_col, class_col, columns_order, mat_columns=None, desc_cols=None, outformat='zip', opSuff=''):
    if outformat == 'zip':
        # WRITE ZIP >> FOR MASTERMovelets:
        df2zip(data_path, df, file, tid_col, class_col, select_cols=columns_order,\
               opLabel='Writing - ZIP |' + opSuff)
        
    elif outformat == 'csv':
        print('Writing - CSV |' + opSuff)
        df[columns_order].to_csv(os.path.join(data_path, file+".csv"), index = False)
        
    elif outformat == 'parquet':
        print('Writing - Parquet |' + opSuff)
        df[columns_order].to_parquet(os.path.join(data_path, file+".parquet"), index = False)
        
    elif outformat == 'mat':
        # WRITE MAT Files >> FOR HiPerMovelets:
        df2mat(df, data_path, file, cols=columns_order, mat_cols=mat_columns, tid_col=tid_col, class_col=class_col, \
               desc_cols=desc_cols, opLabel='Writing - MAT|' + opSuff)
        
def writeFiles(data_path, file, train, test, tid_col, class_col, columns_order, mat_columns=None, desc_cols=None, outformat='zip', opSuff=''):
    # WRITE Train
    writeFile(data_path, train, file+'train', tid_col, class_col, columns_order, mat_columns, desc_cols, 
              outformat, opSuff='TRAIN - '+opSuff)
    # WRITE Test
    writeFile(data_path, test,  file+'test',  tid_col, class_col, columns_order, mat_columns, desc_cols, 
              outformat, opSuff='TEST - '+ opSuff)
    

#-------------------------------------------------------------------------->>
def splitframe(data, name='tid'):    
    n = data[name][0]

    df = pd.DataFrame(columns=data.columns)

    datalist = []

    for i in range(len(data)):
        if data[name][i] == n:
            df = df.append(data.iloc[i])
        else:
            datalist.append(df)
            df = pd.DataFrame(columns=data.columns)
            n = data[name][i]
            df = df.append(data.iloc[i])

    return datalist

#--------------------------------------------------------------------------------
def convertDataset(dir_path, k=None, cols = None, fileprefix='', tid_col='tid', class_col='label'):
    def convert_file(file, cols):
        df = readDataset(dir_path, fileprefix+file+'.csv')
            
        if not cols:
            cols = list(df.columns)
        df, columns_order_zip, columns_order_csv = organizeFrame(df, cols, tid_col, class_col)
        
        outformats = []
        if not os.path.exists(os.path.join(dir_path, file+'.zip')):
            outformats.append('zip')
#            print("Saving dataset as: " + os.path.join(dir_path, file+'.zip'))
#            df2zip(dir_path, df, file, tid_col, class_col, select_cols=columns_order_zip)
        if not os.path.exists(os.path.join(dir_path, fileprefix+file+'.csv')):
            outformats.append('csv')
#            print("Saving dataset as: " + os.path.join(dir_path, file+'.csv'))
#            df[columns_order_csv].to_csv(os.path.join(dir_path, fileprefix+file+'.csv'), index = False)
        if not os.path.exists(os.path.join(dir_path, fileprefix+file+'.mat')):
            outformats.append('mat')
#            print("Saving dataset as: " + os.path.join(dir_path, file+'.mat'))
#            df[columns_order_csv].to_csv(os.path.join(dir_path, fileprefix+file+'.mat'), index = False)
            
        return df, columns_order_zip, columns_order_csv, outformats
        
    df_test, columns_order_zip, columns_order_csv, outformats = convert_file('test', cols)
    df_train, columns_order_zip, columns_order_csv, outformats = convert_file('train', cols)
    
    for outType in outformats:
        writeFiles(dir_path, fileprefix, df_train, df_test, tid_col, class_col, \
                 columns_order_zip if outType in ['zip', 'mat'] else columns_order_csv, None, outType, opSuff='')
    
    data = pd.concat([df_train,df_test])

    if k and not os.path.exists(os.path.join(dir_path, 'run1')):
        train, test = kfold_trainTestSplit(data, k, fileprefix=fileprefix, random_num=1, tid_col=tid_col, class_col=class_col, columns_order=columns_order_csv, data_path=dir_path)
        for i in range(1, k+1):
            for file in ['train', 'test']:
                os.rename(os.path.join(dir_path, 'run'+str(i), fileprefix+file+'.zip'), 
                          os.path.join(dir_path, 'run'+str(i), file+'.zip'))

        if 'space' in columns_order_zip:
            kfold_trainTestSplit(None, k, random_num=1, fileprefix='raw_', tid_col=tid_col, class_col=class_col, columns_order=columns_order_csv, ktrain=train, ktest=test, data_path=dir_path)
            for i in range(1, k+1):
                for file in ['train', 'test']:
                    os.remove(os.path.join(dir_path, 'run'+str(i), 'raw_'+file+'.zip'))
    
    print("All Done.")
#--------------------------------------------------------------------------------