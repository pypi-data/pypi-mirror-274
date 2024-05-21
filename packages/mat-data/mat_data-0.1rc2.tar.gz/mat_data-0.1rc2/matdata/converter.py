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

from zipfile import ZipFile

from tqdm.auto import tqdm

# IN METHOD, ts2df: #from matdata.inc.ts_io import load_from_tsfile_to_dataframe
#-------------------------------------------------------------------------->>
def csv2df(url, class_col='label', tid_col='tid', missing='?'): # TODO class_col, tid_col unnecessary
    """
    Converts a CSV file from a given URL into a pandas DataFrame.

    Parameters:
    -----------
    url : str
        The URL pointing to the CSV file to be read.
    class_col : str, optional (default='label')
        Unused, kept for standard.
    tid_col : str, optional (default='tid')
        Unused, kept for standard.
    missing : str, optional (default='?')
        The placeholder for missing values in the CSV file.

    Returns:
    --------
    pandas.DataFrame
        A DataFrame containing the data from the CSV file, with missing values
        handled as specified and columns renamed if necessary.
    """
    
    return pd.read_csv(url, na_values=missing)

def parquet2df(url, class_col='label', tid_col='tid', missing='?'): # TODO class_col, tid_col unnecessary
    """
    Converts a Parquet file from a given URL into a pandas DataFrame.

    Parameters:
    -----------
    url : str
        The URL pointing to the Parquet file to be read.
    class_col : str, optional (default='label')
        Unused, kept for standard.
    tid_col : str, optional (default='tid')
        Unused, kept for standard.
    missing : str, optional (default='?')
        The placeholder for missing values in the dataset.

    Returns:
    --------
    pandas.DataFrame
        A DataFrame containing the data from the Parquet file, with missing values
        handled as specified and columns renamed if necessary.
    """
    
    df = pd.read_parquet(url)
    if missing:
        df = df.fillna(missing)
    return df
    
def zip2df(url, class_col='label', tid_col='tid', missing='?', opLabel='Reading ZIP'):
    """
    Extracts and converts a CSV trajectory file from a ZIP archive located at a given URL into a pandas DataFrame.

    Parameters:
    -----------
    url : str
        The URL pointing to the ZIP archive containing the CSV file to be read.
    class_col : str, optional (default='label')
        The name of the column to be treated as the class/label column.
    tid_col : str, optional (default='tid')
        The name of the column to be used as the unique trajectory identifier.
    missing : str, optional (default='?')
        The placeholder for missing values in the CSV file.
    opLabel : str, optional (default='Reading ZIP')
        A label describing the operation, for logging purposes.

    Returns:
    --------
    pandas.DataFrame
        A DataFrame containing the data from the extracted CSV file, with missing values
        handled as specified and columns renamed if necessary.
    """

    if isinstance(url, str):
        url = ZipFile(url)
    return read_zip(url, None, class_col, tid_col, missing, opLabel)

def mat2df(url, class_col='label', tid_col='tid', missing='?'):
    """
    Converts a MATLAB .mat file from a given URL into a pandas DataFrame.

    Parameters:
    -----------
    url : str
        The URL pointing to the .mat file to be read.
    class_col : str, optional (default='label')
        The name of the column to be treated as the class/label column.
    tid_col : str, optional (default='tid')
        The name of the column to be used as the unique trajectory identifier.
    missing : str, optional (default='?')
        The placeholder for missing values in the dataset.

    Returns:
    --------
    pandas.DataFrame
        A DataFrame containing the data from the .mat file, with missing values
        handled as specified and columns renamed if necessary.
        
    Raises:
    -------
    Exception
        Not Implemented.
    """

    raise Exception('Not Implemented')
    
#def read_mat(url, class_col='label', tid_col='tid', missing='?'):
#    raise Exception('Not Implemented')
    
def ts2df(url, class_col='label', tid_col='tid', missing='?'):
    """
    Converts a time series file from a given URL into a pandas DataFrame.

    Parameters:
    -----------
    url : str
        The URL pointing to the time series file to be read.
    class_col : str, optional (default='label')
        The name of the column to be treated as the class/label column.
    tid_col : str, optional (default='tid')
        The name of the column to be used as the unique trajectory identifier.
    missing : str, optional (default='?')
        The placeholder for missing values in the dataset.

    Returns:
    --------
    pandas.DataFrame
        A DataFrame containing the data from the time series file, with missing values
        handled as specified and columns renamed if necessary.
    """
    
    from matdata.inc.ts_io import load_from_tsfile_to_dataframe
    return load_from_tsfile_to_dataframe(url, replace_missing_vals_with=missing)

def xes2df(url, class_col='label', tid_col='tid', opLabel='Converting XES', save=False, start_tid=1):
    """
    Converts an XES (eXtensible Event Stream) file from a given URL into a pandas DataFrame.

    Parameters:
    -----------
    url : str
        The URL pointing to the XES file to be read.
    class_col : str, optional (default='label')
        The name of the column to be treated as the class/label column.
    tid_col : str, optional (default='tid')
        The name of the column to be used as the trajectory identifier.
    opLabel : str, optional (default='Converting XES')
        A label describing the operation, useful for logging or display purposes.
    save : bool, optional (default=False)
        A flag indicating whether to save the DataFrame to a file after conversion.
    start_tid : int, optional (default=1)
        The starting value for trajectory identifiers as `tid_col` values need to be generated.

    Returns:
    --------
    pandas.DataFrame
        A DataFrame containing the data from the XES file, with columns renamed if necessary.
    """

    
    start_tid = start_tid-1
    def getTrace(log, tid):
        t = dict(log[tid].attributes)
        return t
    
    def getEvent(log, tid , j, attrs):
        ev = dict(log[tid][j])
        
        eqattr = set(attrs.keys()).intersection(set(ev.keys()))
        for k in eqattr:
            attrs[k+'_t'] = attrs.pop(k)
        
        ev.update(attrs)
        ev['tid'] = start_tid+tid+1
        return ev
    
    import pm4py
    if isinstance(url, str):
        log = pm4py.read_xes(url)
    else:
        log = pm4py.parse_event_log_string(url)
    
    data = list(map(lambda tid: 
                pd.DataFrame(list(map(lambda j: getEvent(log, tid , j, getTrace(log, tid)), range(len(log[tid]))))),
                tqdm(range(len(log)), desc=opLabel)))

    df = pd.concat(data, ignore_index=True)
    
    return df
    
#-------------------------------------------------------------------------->>
def df2parquet(df, data_path, file="train", tid_col='tid', class_col='label', select_cols=None, opLabel='Writing Parquet'):
    """
    Writes a pandas DataFrame to a Parquet file.

    Parameters:
    -----------
    df : pandas.DataFrame
        The DataFrame to be written to the Parquet file.
    data_path : str
        The directory path where the Parquet file will be saved.
    file : str, optional (default='train')
        The base name of the Parquet file (without extension).
    tid_col : str, optional (default='tid')
        The name of the column to be used as the trajectory identifier.
    class_col : str, optional (default='label')
        The name of the column to be treated as the class/label column.
    select_cols : list of str, optional
        A list of column names to be included in the Parquet file. If None, all columns are included.
    opLabel : str, optional (default='Writing PARQUET')
        A label describing the operation, useful for logging or display purposes.

    Returns:
    --------
    pandas.DataFrame
        The input DataFrame
    """
    
    F = os.path.join(data_path, file+'.parquet')
    
    print(opLabel+": " + F)
    if not os.path.exists(data_path):
        os.makedirs(data_path)
    
    if not select_cols:
        select_cols = list(df.columns)
    
    df[select_cols].to_parquet(F)
    print("Done.")
    print(" --------------------------------------------------------------------------------")
    return df

def df2csv(df, data_path, file="train", tid_col='tid', class_col='label', select_cols=None, opLabel='Writing CSV'):
    """
    Writes a pandas DataFrame to a CSV file.

    Parameters:
    -----------
    df : pandas.DataFrame
        The DataFrame to be written to the CSV file.
    data_path : str
        The directory path where the Parquet file will be saved.
    file : str, optional (default='train')
        The base name of the CSV file (without extension).
    tid_col : str, optional (default='tid')
        The name of the column to be used as the trajectory identifier.
    class_col : str, optional (default='label')
        The name of the column to be treated as the class/label column.
    select_cols : list of str, optional
        A list of column names to be included in the CSV file. If None, all columns are included.
    opLabel : str, optional (default='Writing PARQUET')
        A label describing the operation, useful for logging or display purposes.

    Returns:
    --------
    pandas.DataFrame
        The input DataFrame
    """
    
    F = os.path.join(data_path, file+'.csv')
    
    print(opLabel + ": " + F)
    if not os.path.exists(data_path):
        os.makedirs(data_path)
    
    if not select_cols:
        select_cols = list(df.columns)
    
    df[select_cols].to_csv(F)
    print("Done.")
    print(" --------------------------------------------------------------------------------")
    return df

def df2zip(df, data_path, file, tid_col='tid', class_col='label', select_cols=None, opLabel='Writing MAT'):
    """
    Writes a pandas DataFrame to a CSV file and compresses it into a ZIP archive.

    Parameters:
    -----------
    df : pandas.DataFrame
        The DataFrame to be written to the CSV file and then compressed into a ZIP archive.
    data_path : str
        The directory path where the ZIP archive will be saved.
    file : str
        The base name of the CSV file (without extension) to be compressed into the ZIP archive.
    tid_col : str, optional (default='tid')
        The name of the column to be used as the trajectory identifier.
    class_col : str, optional (default='label')
        The name of the column to be treated as the class/label column.
    select_cols : list of str, optional
        A list of column names to be included in the CSV file. If None, all columns are included.
    opLabel : str, optional (default='Writing ZIP')
        A label describing the operation, useful for logging or display purposes.

    Returns:
    --------
    pandas.DataFrame
        The input DataFrame
    """
    
    EXT = '.r2'
    if not os.path.exists(data_path):
        os.makedirs(data_path)
    zipf = ZipFile(os.path.join(data_path, file+'.zip'), 'w')
    
    n = len(str(len(df.index)))
    tids = df[tid_col].unique()
    
    if not select_cols:
        select_cols = list(df.columns)
    select_cols = [x for x in select_cols if x not in [tid_col, class_col]]
    
    def writeMAT(x):
        filename = str(x).rjust(n, '0') + ' s' + str(x) + ' c' + str(df.loc[df[tid_col] == x][class_col].iloc[0]) + EXT
        data = df[df.tid == x]
        # Selected
        if select_cols is not None:
            data = data[select_cols]
        
        # Remove tid and label:
        data = data.drop([tid_col, class_col], axis=1, errors='ignore')
        
        data.to_csv(filename, index=False, header=False)
        zipf.write(filename)
        os.remove(filename)
    list(map(lambda x: writeMAT(x), tqdm(tids, desc=opLabel)))
    zipf.close()
    
def df2mat(df, folder, file, cols=None, mat_cols=None, desc_cols=None, label_columns=None, other_dsattrs=None,
           tid_col='tid', class_col='label', opLabel='Converting MAT'):
    """
    Converts a pandas DataFrame to a Multiple Aspect Trajectory .mat file and saves it to the specified folder.

    Parameters:
    -----------
    df : pandas.DataFrame
        The DataFrame to be converted to a .mat file.
    folder : str
        The directory where the .mat file will be saved.
    file : str
        The base name of the .mat file (without extension).
    cols : list of str, optional
        A list of column names from the DataFrame to include in the .mat file. If None, all columns are included.
    mat_cols : list of str, optional
        A list of column names representing the trajectory attibutes. If None, no columns are used.
    desc_cols : list of str, optional
        A dict of column descriptors to be included as descriptive metadata.
    label_columns : list of str, optional
        A list of column names that can be treated as labels in the .mat file.
    other_dsattrs : dict, optional
        A dictionary of additional dataset attributes to be included in the .mat file.
    tid_col : str, optional (default='tid')
        The name of the column to be used as the trajectory identifier.
    class_col : str, optional (default='label')
        The name of the column to be treated as the class/label column.
    opLabel : str, optional (default='Converting MAT')
        A label describing the operation, useful for logging or display purposes.

    Returns:
    --------
    None
    """
    
    if '.mat' in file:
        url = os.path.join(folder, file)
        file = file.replace('.mat', '')
    else:
        url = os.path.join(folder, file+'.mat')
    
    if not cols:
        cols = list(df.columns)
    cols = [x for x in cols if x not in [tid_col, class_col]]
    
    if mat_cols:
        mat_cols = [x for x in mat_cols if x not in [tid_col, class_col]]
    
    f = open(url, "w")
    f.write("# Dataset: " + os.path.basename(folder) + ' (comment description)\n')
    f.write("@problemName " + os.path.basename(folder) + '\n')
    
    if label_columns:
        f.write('@labelColumns ' + (','.join(label_columns)) + '\n')
        
    f.write("@missing "+ str(df.apply(lambda ts: '?' in ts.values, axis=1).any() or df.isnull().any().any())+'\n')
    f.write("@aspects " + str(len(cols)) + '\n')
    f.write('@aspectNames ' + (','.join(cols)) + '\n')
    if mat_cols:
        f.write('@trajectoryAspectNames ' + (','.join(mat_cols)) + '\n')
        
    if not desc_cols:
        # dictionary in the format: {'aspectName': 'type', 'aspectName': 'type'}
        desc_cols = descTypes(df)    
    f.write('@aspectDescriptor ' + (','.join(':'.join((key,val)) for (key,val) in desc_cols.items())) + '\n')
    
    if other_dsattrs:
        for k,v in other_dsattrs:
            f.write('@'+k+' ' + (','.join(v)) + '\n')
    
    f.write("@data\n")
    def getTrace(df, tid):
        s = ''
        s += '@trajectory \n' + str(tid) + ',' + str(df[class_col].values[0]) + '\n'
        if mat_cols:
            s += '@trajectoryAspects\n'
            s += df[mat_cols][0:1].to_csv(index=False,header=False, quotechar='"')
                
        s += '@trajectoryPoints\n'
        s += df[cols].to_csv(index=False,header=False, quotechar='"')

        return s
           
    list(map(lambda tid: f.write(getTrace(df[df[tid_col] == tid], tid)),
            tqdm(df[tid_col].unique(), desc=opLabel)))

    f.close()

#-------------------------------------------------------------------------->>
def read_zip(zipFile, cols=None, class_col='label', tid_col='tid', missing='?', opLabel='Reading ZIP'):
    ### [Private helper function]
    
    data = pd.DataFrame()
    with zipFile as z:
        files = z.namelist()
        files.sort()
        def readCSV(filename):
            if cols is not None:
                df = pd.read_csv(z.open(filename), names=cols, na_values=missing)
            else:
                df = pd.read_csv(z.open(filename), header=None, na_values=missing)
            df[tid_col]   = filename.split(" ")[1][1:]
            df[class_col] = filename.split(" ")[2][1:-3]
            return df
        data = list(map(lambda filename: readCSV(filename), tqdm(z.namelist(), desc=opLabel)))
        data = pd.concat(data)
    return data

#-------------------------------------------------------------------------->>
def zip2csv(folder, file, cols, class_col = 'label', tid_col='tid', missing='?'):
    """
    Extracts and compile Trajectory CSV files from a ZIP archive and converts it into a pandas DataFrame.

    Parameters:
    -----------
    folder : str
        The directory path where the ZIP archive is located, and destination to the CSV resulting file.
    file : str
        The name of the ZIP archive file (with or without extension).
    cols : list of str
        A list of column names to be included in the DataFrame.
    class_col : str, optional (default='label')
        The name of the column to be treated as the class/label column.
    tid_col : str, optional (default='tid')
        The name of the column to be used as the trajectory identifier.
    missing : str, optional (default='?')
        The placeholder for missing values in the CSV file.

    Returns:
    --------
    pandas.DataFrame
        A DataFrame containing the data from the extracted CSV file, with missing values
        handled as specified and columns renamed if necessary.
    """

    data = zip2df(folder, file, cols, class_col, tid_col, missing)
    print("Saving dataset as: " + os.path.join(folder, file+'.csv'))
    data.to_csv(os.path.join(folder, file+'.csv'), index = False)
    print("Done.")
    print(" --------------------------------------------------------------------------------")
    return data

def zip2arf(folder, file, cols, tid_col='tid', class_col = 'label', missing='?', opLabel='Reading CSV'):
    """
    Extracts a CSV file from a ZIP archive and converts it into an ARFF (Attribute-Relation File Format) file.

    Parameters:
    -----------
    folder : str
        The directory path where the ZIP archive is located.
    file : str
        The name of the ZIP archive file (with or without extension).
    cols : list of str
        A list of column names to be included in the ARFF file.
    tid_col : str, optional (default='tid')
        The name of the column to be used as the trajectory identifier.
    class_col : str, optional (default='label')
        The name of the column to be treated as the class/label column.
    missing : str, optional (default='?')
        The placeholder for missing values in the CSV file.
    opLabel : str, optional (default='Reading CSV')
        A label describing the operation, useful for logging or display purposes.

    Returns:
    --------
    pandas.DataFrame
        A DataFrame containing the data from the extracted ZIP file, with missing values
        handled as specified and columns renamed if necessary.
    """
    
    data = pd.DataFrame()
    print("Converting "+file+" data from... " + folder)
    if '.zip' in file:
        url = os.path.join(folder, file)
    else:
        url = os.path.join(folder, file+'.zip')
    with ZipFile(url) as z:
#         for filename in z.namelist():
# #             data = filename.readlines()
#             df = pd.read_csv(z.open(filename), names=cols, na_values=missing)
# #             print(filename)
#             df[tid_col]   = filename.split(" ")[1][1:]
#             df[class_col] = filename.split(" ")[2][1:-3]
#             data = pd.concat([data,df])
        def readCSV(filename):
#             data = filename.readlines()
            df = pd.read_csv(z.open(filename), names=cols, na_values=missing)
#             print(filename)
            df[tid_col]   = filename.split(" ")[1][1:]
            df[class_col] = filename.split(" ")[2][1:-3]
            return df
        data = list(map(lambda filename: readCSV(filename), tqdm(z.namelist(), desc=opLabel)))
        data = pd.concat(data)
    print("Done.")
    
    print("Saving dataset as: " + os.path.join(folder, file+'.csv'))
    data.to_csv(os.path.join(folder, file+'.csv'), index = False)
    print("Done.")
    print(" --------------------------------------------------------------------------------")
    return data

def any2ts(data_path, folder, file, cols=None, tid_col='tid', class_col = 'label', opLabel='Converting TS'):
    """
    Converts data from various formats (CSV, Parquet, etc.) to a time series format.

    Parameters:
    -----------
    data_path : str
        The directory path where the data files are located.
    folder : str
        The folder containing the data file to be converted.
    file : str
        The name of the data file to be converted.
    cols : list of str, optional
        A list of column names to be included in the time series data.
    tid_col : str, optional (default='tid')
        The name of the column to be used as the trajectory identifier.
    class_col : str, optional (default='label')
        The name of the column to be treated as the class/label column.
    opLabel : str, optional (default='Converting TS')
        A label describing the operation, useful for logging or display purposes.

    Returns:
    --------
    pandas.DataFrame
        A DataFrame containing the time series data, with trajectory identifier, class label, and specified columns.
    """
    
    print("Converting "+file+" data from... " + data_path + " - " + folder)
    data = readDataset(data_path, folder, file, class_col)
    
    file = file.replace('specific_',  '')
    
    tsName = os.path.join(data_path, folder, folder+'_'+file.upper()+'.ts')
    tsDesc = os.path.join(data_path, folder, folder+'.md')
    print("Saving dataset as: " + tsName)
    if not cols:
        cols = list(data.columns)
    cols = [x for x in cols if x not in [tid_col, class_col]]
    
    f = open(tsName, "w")
    
    if os.path.exists(tsDesc):
        fd = open(tsDesc, "r")
        for line in fd:
            f.write("# " + line)
#         fd.close()

    f.write("#\n")
    f.write("@problemName " + folder + '\n')
    f.write("@timeStamps false")
    f.write("@missing "+ str('?' in data)+'\n')
    f.write("@univariate "+ ('false' if len(cols) > 1 else 'true') +'\n')
    f.write("@dimensions " + str(len(cols)) + '\n')
    f.write("@equalLength false" + '\n')
    f.write("@seriesLength " + str(len(data[data[tid_col] == data[tid_col][0]])) + '\n')
    f.write("@classLabel true " + ' '.join([str(x).replace(' ', '_') for x in list(data[class_col].unique())]) + '\n')
    f.write("@data\n")
    
#     for tid in data[tid_col].unique():
    def writeLine(tid):
        df = data[data[tid_col] == tid]
        line = ''
        for col in cols:
            line += ','.join(map(str, list(df[col]))) + ':'
        f.write(line + str(df[class_col].unique()[0]) + '\n')
    list(map(lambda tid: writeLine(tid), tqdm(data[tid_col].unique(), desc=opLabel)))
    
    f.write('\n')
    f.close()
    print("Done.")
    print(" --------------------------------------------------------------------------------")
    return data

# --------------------------------------------------------------------------------
def descTypes(df):
    ### [Private helper function]
    
    def getType(k, t):
        if t.name == 'category':
            return 'nominal'
        elif t is int or t is float or np.issubdtype(t, np.number):
            return 'numeric'
        elif 'space' in k or 'lat_lon' in k:
            return 'space2d'
        else:
            return 'nominal'
            
    return {k: getType(k, df.dtypes[k]) for k in df.columns}
    