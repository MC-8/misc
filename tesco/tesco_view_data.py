import json
import pandas as pd
# from pandas import DataFrame as df
from matplotlib import pyplot as plt
import numpy as np
from datetime import datetime
# import locale
# locale.setlocale(locale.LC_MONETARY,'')

DTIME_FORMAT = "%Y-%m-%d %H:%M:%S"

with open('misc/tesco/Tesco-Customer-Data.json') as json_file:
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
fig, ax = plt.subplots(2, 1)
k=0
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
    print(f"=====================")

    # Yearly breakdown
    years = range(2017,2021)
    months = range(1,13)
    print(f"*******************************************************")
    print(f"******************** YEARLY BREAKDOWN *****************")
    print(f"*******************************************************")
    pltx = []
    pltx_ticks = []
    plty = []
    idx = 0
    for y in years:
        for m in months:
            if m<=3 and y<=2017: continue
            if m<12:
                VD = visit_dataframe[ (pd.to_datetime(visit_dataframe.timeStamp) >= datetime(y,m,1)) & \
                                      (pd.to_datetime(visit_dataframe.timeStamp) < datetime(y,m+1,1)) ]
            else:
                VD = visit_dataframe[ (pd.to_datetime(visit_dataframe.timeStamp) >= datetime(y,m,1)) & \
                                      (pd.to_datetime(visit_dataframe.timeStamp) < datetime(y+1,1,1)) ]
            if VD.empty:
                pltx.append(idx)
                pltx_ticks.append(f"{m}")
                plty.append(0)
                idx+=1
                continue
            pltx.append(idx)
            pltx_ticks.append(f"{m}")
            plty.append(sum(VD.basketValueNet))
            date_begin = min(pd.to_datetime(VD.timeStamp)).date()
            date_end = max(pd.to_datetime(VD.timeStamp)).date()
            delta_time = (date_end - date_begin).days
            savings = sum(VD.overallBasketSavings)
            print(f"Total spent between {date_begin} and {date_end} ({delta_time} days) = £{sum(VD.basketValueNet):.2f} (£{sum(VD.overallBasketSavings):.2f} savings)")
            print(f"Min spent = £{min(VD.basketValueNet):.2f}")
            print(f"Max spent = £{max(VD.basketValueNet):.2f}")
            print(f"Avg spent = £{np.mean(VD.basketValueNet):.2f}")
            print(f"=====================")
            idx+=1
    ax[k].scatter(pltx, plty)
    ax[k].grid(True)
    k +=1

    print(f"\n\n\n")

plt.setp(ax, xticks=pltx, xticklabels=pltx_ticks, )
ax[0].set_title('Groceries')
ax[1].set_title('Petrol')
plt.show()
total_price = 0
total_quantity = 0
for p in DF['product']:
    for e in p:
        pname = e['name'].lower()
        #if 'bread' in pname and 'flour' not in pname and 'ginger' not in pname or 'baton' in pname and 'chicken' not in pname and 'breaded' not in pname: 
        if 'tomato' in pname: 
            # print(pname)
            total_price += float(e['price'])
            total_quantity += float(e['quantity'])

print(f"You had {total_quantity} things and spent £{total_price:.2f}")