from cgi import print_arguments
from re import A
from pythena_lite import pivot_and_resample_iot_data
import pandas as pd
import numpy as np
import matplotlib
from datetime import datetime
import datetime as dt
from matplotlib import pyplot as plt
import numpy as np
import matplotlib.dates as md
import functools as ft
import glob
from pathlib import Path
import os


directory = r"C:\Users\Marco\Desktop\Masterarbeit\Thema Viesmann\Daten_Test"

files = glob.glob(r"C:\Users\Marco\Desktop\Masterarbeit\Thema Viesmann\Prog_Neu\Outside_Temp_Data_870_HP\**\*.parquet")

data_list = []



#Create DF for NaN_Values
NaN_Values_df = pd.DataFrame()

for filename in files:
    #resampling with 15 Min time steps and limit of 1h
    df = pd.read_parquet(filename)
    df = pivot_and_resample_iot_data(df, "15T", limit= 3600)
    
    #insert and merge another data frame to fill the cut time
    dtMin = df["timestamp"].min()
    dtMax = df["timestamp"].max()
    df1 = pd.DataFrame(pd.date_range(dtMin, dtMax, freq="15T"), columns=["timestamp"])
    df3 = df1.merge(df, on="timestamp", how="left")
    
    #count NaN values of each device
    NaN_Values_sum_outside_temp = df3["heating.sensors.temperature.outside/value"].isna().sum()

    #Short filename to the gateway uuid
    filename = os.path.basename(filename)
    filename = os.path.splitext(filename)[0]
    # add counted Nan Values and gateway uuid to list
    NaN_Values_df = NaN_Values_df.append({"Filename": filename, "heating.sensors.temperature.outside/value":NaN_Values_sum_outside_temp }, ignore_index=True)


print(NaN_Values_df.head())
NaN_Values_df.to_excel(r"C:\Users\Marco\Desktop\Masterarbeit\Thema Viesmann\Prog_Neu\NaN_Values_V2.xlsx")
