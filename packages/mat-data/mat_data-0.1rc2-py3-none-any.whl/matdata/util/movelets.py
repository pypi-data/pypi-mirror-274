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
import glob2 as glob

from matdata.util.parsers import json2movelet

def read_all_movelets(path_name, name='movelets'):
    count = 0
    path_to_file = glob.glob(os.path.join(path_name, '**', 'moveletsOnTrain.json'), recursive=True)

    movelets = []
    for file_name in path_to_file:
        aux_mov = read_movelets(file_name, name, count)
        movelets = movelets + aux_mov
        count = len(movelets)

    return movelets
    
def read_movelets(file_name, name='movelets', count=0):
    with open(file_name) as f:
        return json2movelet(f, name, count)
    return []