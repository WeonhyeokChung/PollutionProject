#-------------------------------------------------------
#
#   Weonhyeok Chung weonhyeok.chung@gmail.com
#   Feb-14-2022
#
#-------------------------------------------------------
#   Summary: Tn this file I use region by pollution running
#       variable and covariates to estimate effect of 
#       pollution information on actual search in Korea.
#-------------------------------------------------------
#   Previous Steps: Use pollution data from AirKorea and
#       search data from Naver Data Lab. Create running variable
#       for pollution information. 
#-------------------------------------------------------
### Load RDROBUST package
from rdrobust import rdrobust,rdbwselect,rdplot
import pandas as pd

### Load data base
rdrobust_pm = pd.read_excel("data/pollution.xlsx")

print(rdrobust_pm)

pm_rv = rdrobust_pm.pm_run
outcome = rdrobust_pm.search

covs = rdrobust_pm.iloc[:,4:40]

### rdplot with 95% confidence intervals
rdplot(y=outcome, x=pm_rv, binselect="es", ci=95, 
         title="RD Plot: Pollution and Media Forecasting Data", 
         y_label="Forecast Bad Particular Matter",
         x_label="Running Variable of PM")

### rdrobust 
print(rdrobust(y=outcome, x=pm_rv, covs=covs))