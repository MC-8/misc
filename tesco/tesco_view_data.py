import json
import pandas as pd
# from pandas import DataFrame as df
import numpy as np
from datetime import datetime
# import locale
# locale.setlocale(locale.LC_MONETARY,'')

DTIME_FORMAT = "%Y-%m-%d %H:%M:%S"

with open('Tesco-Customer-Data.json') as json_file:
    data = json.load(json_file)
    purchases = data['Purchase'][0]

DF = pd.DataFrame.from_dict(purchases) # Dataframe
DF.basketValueGross = pd.to_numeric(DF.basketValueGross, downcast="float")
DF.basketValueNet = pd.to_numeric(DF.basketValueNet, downcast="float")
DF.overallBasketSavings = pd.to_numeric(DF.overallBasketSavings, downcast="float")

# Split between petrol and groceries                          # , removing refund transactions
petrol_DF    = DF[(DF.storeFormat.apply(str.lower)=='petrol') & (DF.basketValueNet>0)]
groceries_DF = DF[(DF.storeFormat.apply(str.lower)!='petrol') & (DF.basketValueNet>0)]

visit_types_dict = {'Groceries':groceries_DF,
                    'Petrol':petrol_DF}

for visit_type, visit_dataframe in visit_types_dict.items():
    print(f"{visit_type} summary:")
    print(f"=====================")
    date_begin = min(pd.to_datetime(visit_dataframe.timeStamp)).date()
    date_end = max(pd.to_datetime(visit_dataframe.timeStamp)).date()
    delta_time = (date_end - date_begin).days
    print(f"Total spent between {date_begin} and {date_end} ({delta_time} days) = £{sum(visit_dataframe.basketValueNet):.2f} (£{sum(visit_dataframe.overallBasketSavings):.2f} savings)")
    print(f"Min spent = £{min(visit_dataframe.basketValueNet):.2f}")
    print(f"Max spent = £{max(visit_dataframe.basketValueNet):.2f}")
    print(f"Avg spent = £{np.mean(visit_dataframe.basketValueNet):.2f}")
    print(f"Total savings = £{sum(visit_dataframe.overallBasketSavings):.2f}")
    print(f"=====================")

    # Yearly breakdown
    years = range(2016,2021)
    print(f"*******************************************************")
    print(f"******************** YEARLY BREAKDOWN *****************")
    print(f"*******************************************************")
    for y in years:
        VD = visit_dataframe[ (pd.to_datetime(visit_dataframe.timeStamp) >= datetime(y,1,1)) & \
                         (pd.to_datetime(visit_dataframe.timeStamp) < datetime(y+1,1,1)) ]
        if VD.empty: continue
        date_begin = min(pd.to_datetime(VD.timeStamp)).date()
        date_end = max(pd.to_datetime(VD.timeStamp)).date()
        delta_time = (date_end - date_begin).days
        print(f"Total spent between {date_begin} and {date_end} ({delta_time} days) = £{sum(VD.basketValueNet):.2f} (£{sum(VD.overallBasketSavings):.2f} savings)")
        print(f"Min spent = £{min(VD.basketValueNet>0):.2f}")
        print(f"Max spent = £{max(VD.basketValueNet>0):.2f}")
        print(f"Avg spent = £{np.mean(VD.basketValueNet):.2f}")
        print(f"Total savings = £{sum(VD.overallBasketSavings):.2f}")
        print(f"=====================")
    print(f"\n\n\n")


