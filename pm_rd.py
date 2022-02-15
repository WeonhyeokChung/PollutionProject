#-------------------------------------------------------
#   Weonhyeok Chung weonhyeok.chung@gmail.com
#   Feb-15-2022
#-------------------------------------------------------
#   Summary: In this file I use pollution running
#       variable and covariates to estimate effect of 
#       pollution information on actual search in Korea.
#-------------------------------------------------------
#   Previous Steps: Use pollution data from AirKorea and
#       search data from Naver Data Lab. 
#       I don't provide specific data as this is an on-going research.
#-------------------------------------------------------
import os
import sys
import pandas as pd
from rdrobust import rdrobust,rdbwselect,rdplot
import pandas as pd
import matplotlib.pyplot as plt

# merge two data sets (pollution data & search data)
df1 = pd.read_excel("data/pollution_collase.xlsx")
# VARIABLES: region date PM10 PM25 min_twohr min_twohr bad year month day

df2 = pd.read_excel("data/search.xlsx")
# VARIABLES: DATE region year month day search

df = pd.merge(df1, df2, how="left", on=['region', 'year', 'month', 'day'])
df=pd.get_dummies(df, prefix=['year', 'month', 'region'], columns=['year', 'month', 'region'])

# create running variables for information (either "bad air forecast" or "alert")
df["pm10_run"] = df["PM10"] - 81 # pm10 bad air forecast
df["pm25_run"] = df["PM25"] - 36 # pm25 bad air forecast
df["twohr10_run"] = df["min_twohr10"] - 150 # pm10 alert
df["twohr25_run"] = df["min_twohr25"] - 90 # pm25 alert
df["pm_run"] = df[["pm10_run", "pm25_run", "twohr10_run", "twohr25_run"]].max(axis=1)

# I restrict days when the running variable is between -20 and 20. 
df = df.loc[df["pm_run"]>-20]
df = df.loc[df["pm_run"]<=20]

# running variable, outcome, and covariates
pm_rv = df.pm_run
outcome = df.search
covs = df.iloc[:,10:40]

rdrobust_pm = df

### rdplot with 95% confidence intervals
rdplot(y=outcome, x=pm_rv, binselect="es", ci=95, 
         title="RD Plot: Search Behavior and PM Information", 
         y_label="Search Behavior",
         x_label="Running Variable of PM")

### rdrobust 
original_stdout = sys.stdout # Save a reference to the original standard output
with open('results/rdrobust_result.txt', 'w') as f:
    sys.stdout = f # Change the standard output to the file we created.
    print(rdrobust(y=outcome, x=pm_rv, covs=covs))
    sys.stdout = original_stdout # Reset the standard output to its original value
    
    
