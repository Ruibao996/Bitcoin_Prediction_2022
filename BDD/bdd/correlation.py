import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import datetime as datetime
from scipy.stats import pearsonr
import seaborn as sns

supply_data = pd.read_csv("daily_supply.csv")
supply_data["t"] = pd.to_datetime(supply_data["t"])
supply_data["t"] = supply_data["t"].apply(lambda x: x.to_pydatetime())
supply_data["t"] = supply_data["t"].dt.date
supply_data["t"] = pd.to_datetime(supply_data["t"])
supply_data.rename(columns={"t":"Time", "v":"Supply"}, inplace=True)
# print(supply_data.head())
# print(supply_data.info())


price_day = pd.read_csv("full_price_day.csv")
price_day.rename(columns={"Price (BTC/USD) – Bitcoin":"Price"}, inplace=True)
price_day["Time"] = pd.to_datetime(price_day["Time"], dayfirst=True)
# print(price_day.head())
# print(price_day.info())

bdd_day = pd.read_csv("full_bdd_day.csv")
bdd_day.rename(columns={"sum(Coindays destroyed – Blocks) – Bitcoin":"Days"}, inplace=True)
bdd_day["Time"] = pd.to_datetime(bdd_day["Time"], dayfirst=True)
# print(bdd_day.head())
# print(bdd_day.info())

start = datetime.datetime(2012, 1, 1)

supply_data.drop(supply_data[supply_data["Time"] <= start].index, inplace=True)
supply_data.reset_index(inplace=True ,drop=True)
price_day.drop(price_day[price_day["Time"] <= start].index, inplace=True)
price_day.reset_index(inplace=True ,drop=True)
bdd_day.drop(bdd_day[bdd_day["Time"] <= start].index, inplace=True)
bdd_day.reset_index(inplace=True ,drop=True)

# print(price_day.head())
# print(supply_data.head())
# print(bdd_day.head())

price_day["Supply Adjusted BDD"] = bdd_day["Days"] / supply_data["Supply"]
price_day["MDA30"] = price_day["Supply Adjusted BDD"].rolling(30).mean()
price_day.dropna(inplace=True)
#price_day["Binary_MDA"] = price_day["MDA30"].apply(lambda x: 1 if x >= price_day["MDA30"].mean() else 0)
#print(price_day.head())
# price_day.to_csv("binary.csv")
# print(price_day["MDA30"].mean())
# print(price_day.head())

# fig = plt.figure()
# ax1 = fig.add_subplot(111)
# ax1.plot(price_day["Time"], price_day["Price"])
# ax2 = ax1.twinx()
# ax2.plot(price_day["Time"] ,price_day["MDA30"], color="orange")
# plt.show()

def find_atl(data: pd.DataFrame):
    #market_data = data[(data["Time"] >= start) & (data["Time"] <= end)].reset_index(drop=True)
    atl = data["Price"].min()
    low_info = data[data["Price"] <= atl].reset_index(drop=True)
    return low_info

def find_ath(data: pd.DataFrame, start, end):
    market_data = data[(data["Time"] >= start) & (data["Time"] <= end)].reset_index(drop=True)
    ath = market_data["Price"].max()
    high_info = market_data[market_data["Price"] >= ath].reset_index(drop=True)
    return high_info

def corr_cal(start, end, data: pd.DataFrame, indicator:str):
    market_data = data[(data["Time"] >= start) & (data["Time"] <= end)].reset_index(drop=True)
    if indicator == "Binary_MDA":
        market_data["Binary_MDA"] = market_data["MDA30"].apply(lambda x: 1 if x >= market_data["MDA30"].mean() else 0)
    atl = find_atl(market_data)
    atl_day = atl["Time"][0]
    print(atl_day)
    delta_t = datetime.timedelta(30)
    atl_data = market_data[(market_data["Time"] >= atl_day-2*delta_t) & (market_data["Time"] <= atl_day+delta_t)].reset_index(drop=True)
    atl_data.to_csv("atl.csv")
    atl_data["Distance"] = atl_data["Time"].apply(lambda x: abs((x - atl_day).days))
    if indicator == "MDA30":
     plt.title("BDD - Time Interval", fontsize = 15)
     plt.xlabel("MDA30/Days", fontsize = 15)
     plt.ylabel("Time Interval/Days", fontsize = 15)
     plt.scatter(atl_data[indicator], atl_data["Distance"], s = 50)
     plt.show()
    else:
        sns.boxplot(data=atl_data, x="Binary_MDA", y="Distance")
        plt.show()
    corr, p = pearsonr(atl_data[indicator], atl_data["Distance"])
    co_var = np.cov(atl_data[indicator], atl_data["Distance"])
    print(co_var)
    return corr

def datetime_gen(year, month, day):
    return datetime.datetime(year, month, day)

datetime_gen(2017, 12, 10)
start = datetime_gen(2017, 12, 18)
end = datetime_gen(2019, 3, 24)

start1 = datetime_gen(2013, 11, 30)
end1 = datetime_gen(2015, 10, 15)

#start2 = datetime_gen()
#end2 = datetime_gen()
# 0.794
# 0.664

#a = corr_cal(start, end, price_day, "MDA30")
b = corr_cal(start1, end1, price_day, "MDA30")
#print(a)
print(b)

