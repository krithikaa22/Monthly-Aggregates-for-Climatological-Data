import pandas as pd
from zipfile import ZipFile
import os

def prepare():

    ## get path of current directory
    SCRIPTDIR = os.path.dirname(__file__)

    ## extract the zip file
    with ZipFile(SCRIPTDIR+'/weather.zip', 'r') as zObject: 
        zObject.extractall(path=SCRIPTDIR) 

    files = os.listdir(SCRIPTDIR)
    files = [file for file in files if file.endswith('.csv')]

    file_name = ''

    for f in files:
        data = pd.read_csv(f)

        ## choose the file that has the required fields
        if data['MonthlyDepartureFromNormalAverageTemperature'].isnull().sum() < len(data['MonthlyDepartureFromNormalAverageTemperature']) and data['DailyDepartureFromNormalAverageTemperature'].isnull().sum() < len(data['DailyDepartureFromNormalAverageTemperature']):
            file_name = f 
            field_name = 'DailyDepartureFromNormalAverageTemperature'

            ## write the file name and field name to a yaml file
            with open(SCRIPTDIR+'/fileParams.yaml', 'w') as file:
                file.write(f'file_name: {file_name}\n')
                file.write(f'field_name: {field_name}\n')

    ## extract the ground truth values for monthly aggregates
    monthlyValues = data['MonthlyDepartureFromNormalAverageTemperature']
    monthlyValues.dropna(inplace=True)

    ## write the monthly ground truth values to a csv file
    monthlyValues.to_csv(SCRIPTDIR+'/monthlyValues.csv', index=False)

prepare()