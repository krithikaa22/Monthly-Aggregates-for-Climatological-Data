from sklearn.metrics import r2_score
import pandas as pd
import os

def evaluate():

    ## get path of current directory
    SCRIPTDIR = os.path.dirname(__file__)

    ## load the ground truth and computed monthly values
    monthlyValues = pd.read_csv(SCRIPTDIR+'/monthlyValues.csv')
    monthlyValuesComputed = pd.read_csv(SCRIPTDIR+'/monthlyComputed.csv')

    ## if the length of the two datasets is not equal, truncate the longer dataset
    if len(monthlyValues) != len(monthlyValuesComputed):
        if len(monthlyValues) > len(monthlyValuesComputed):
            monthlyValues = monthlyValues[:len(monthlyValuesComputed)]
        else:
            monthlyValuesComputed = monthlyValuesComputed[:len(monthlyValues)]

    ## compute the r2 score
    r2 = r2_score(monthlyValues, monthlyValuesComputed)

    ## check if the dataset is consistent
    if r2 >= 0.9:
        print('The dataset is consistent')
    else:
        print('The dataset is not consistent')
    return r2

evaluate()