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

price_day["BDD"] = bdd_day["Days"] / (10**6)
price_day["Supply Adjusted BDD"] = bdd_day["Days"] / supply_data["Supply"]
price_day["MDA30"] = price_day["Supply Adjusted BDD"].rolling(30).mean()
price_day.dropna(inplace=True)
price_day.to_csv("final.csv")

#原始BDD数据
# fig = plt.figure()
# ax = fig.add_subplot(111)
# ax.plot(price_day["Time"], price_day["Price"], label = "Price")
# #ax.set_yticks([0, 0.1, 1, 10, 100, 1000, 10000, 100000])
# ax2 = ax.twinx()
# ax2.bar(price_day["Time"], price_day["BDD"], label = "BDD", color = "orange", width=7, alpha = 0.6)
# #ax2.set_yticks([0, 50, 100, 150, 200, 250, 300, 350, 400])
# ax.legend(loc = "upper left", fontsize = 10)
# ax2.legend(loc = "center left", fontsize = 10)
# plt.title("BITCOIN DAYS DESTROYED", fontsize = 15)
# ax.set_ylabel("Price/USD", fontsize = 15)
# ax2.set_ylabel("BDD/Million", fontsize = 15)
# plt.grid(axis="y", linewidth = 0.5)
# plt.show()

#BDD纯数据
#start = price_day.iloc[0]["Time"]
#print(start)
#price_day["week"] = price_day["Time"].apply(lambda x: 1 if (x-start) % 7 == 0 else 0)
# plt.plot(price_day.head()["Time"], price_day.head()["BDD"])
# plt.title("BITCOIN DAYS DESTROYED", fontsize = 15)
# plt.xlabel("Time", fontsize = 15)
# plt.ylabel("BDD/Million", fontsize = 15)
#plt.show()

#MDA30 2017-2019
# start1 = datetime.datetime(2017, 1, 1)
# end1 = datetime.datetime(2020, 1, 1)
# data_2022 = price_day[(price_day["Time"] >= start1) & (price_day["Time"] <= end1)]
# data_2022.to_csv("data_2022.csv")
# fig = plt.figure()
# ax = fig.add_subplot(111)
# ax.plot(data_2022["Time"], data_2022["Price"], label = "Price")
# ax.scatter(["2017-09-02", "2017-12-18", "2018-12-16"], [4830.77, 19325.94, 3236.72], color = "red", s = 75, alpha = 0.8)
# ax2 = ax.twinx()
# ax2.plot(data_2022["Time"], data_2022["MDA30"], label = "MDA30", color = "orange", alpha = 0.7)
# ax2.scatter(["2017-08-23", "2017-12-09", "2018-12-11"], [2.663, 1.743, 2.130], color = "purple", s = 75, alpha = 0.8)
# ax.legend(loc = "upper left", fontsize = 10)
# ax2.legend(loc = "center left", fontsize = 10)
# plt.title("Supply Adjusted BDD", fontsize = 15)
# ax.set_ylabel("Price/USD", fontsize = 15)
# ax2.set_ylabel("MDA/Million", fontsize = 15)
# plt.grid(axis="y", linewidth = 0.5)
# plt.show()

#Binary MDA
# start1 = datetime.datetime(2017, 1, 1)
# end1 = datetime.datetime(2020, 1, 1)
# data_2022 = price_day[(price_day["Time"] >= start1) & (price_day["Time"] <= end1)]
# data_2022["Binary BDD"] = data_2022["MDA30"].apply(lambda x: 1 if x >= data_2022["MDA30"].mean() else 0)
# data_2022.to_csv("data_2022.csv")
# fig = plt.figure()
# ax = fig.add_subplot(111)
# ax.plot(data_2022["Time"], data_2022["Price"], label = "Price")
# ax.scatter(["2017-09-02", "2017-12-18", "2018-12-16"], [4830.77, 19325.94, 3236.72], color = "red", s = 50, alpha = 0.8)
# ax2 = ax.twinx()
# ax2.bar(data_2022["Time"], data_2022["Binary BDD"], label = "Binary BDD", color = "orange", width=0.2)
# #ax2.scatter(["2017-08-23", "2017-12-09", "2018-12-11"], [1, 1, 1], color = "purple", s = 10, alpha = 0.8)
# ax2.set_yticks([0, 1, 2, 3, 4])
# ax.legend(loc = "upper left", fontsize = 10)
# ax2.legend(loc = "center left", fontsize = 10)
# plt.title("Binary BDD", fontsize = 15)
# ax.set_ylabel("Price/USD", fontsize = 15)
# ax2.set_ylabel("Binary BDD", fontsize = 15)
# plt.grid(axis="y", linewidth = 0.5)
# plt.show()


#price_day["Binary_MDA"] = price_day["MDA30"].apply(lambda x: 1 if x >= price_day["MDA30"].mean() else 0)
#print(price_day.head())
# price_day.to_csv("binary.csv")
# print(price_day["MDA30"].mean())
# print(price_day.head())

#最终结论双十一分析
start1 = datetime.datetime(2022, 9, 1)
end1 = datetime.datetime(2022, 12, 1)
data_2022 = price_day[(price_day["Time"] >= start1) & (price_day["Time"] <= end1)]
data_2022.to_csv("data_2022.csv")
fig = plt.figure()
ax = fig.add_subplot(111)
ax.plot(data_2022["Time"], data_2022["Price"], label = "Price")
ax.scatter(["2022-11-10"], [15915.96], color = "red", s = 75, alpha = 0.8)
ax2 = ax.twinx()
ax2.plot(data_2022["Time"], data_2022["MDA30"], label = "MDA30", color = "orange", alpha = 0.7)
ax2.scatter(["2022-11-10"], [0.641], color = "purple", s = 75, alpha = 0.8)
ax.legend(loc = "upper left", fontsize = 12)
ax2.legend(loc = "upper center", fontsize = 12)
plt.title("Supply Adjusted BDD", fontsize = 15)
ax.set_ylabel("Price/USD", fontsize = 15)
ax2.set_ylabel("MDA/Million", fontsize = 15)
plt.grid(axis="y", linewidth = 0.5)
plt.show()