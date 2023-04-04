import requests 
import json
import pandas as pd 
def getData():
    # while next:
    # headers = {
    #     "Authorization": "Basic ZEZ3VmtsYjlpVnhIVFRlbV90R3NRZjUtLVFOWndqenZoQVVTbExhaUxnNDo="

    # }
    # data = []
    # url = "https://ev.caltech.edu/api/v1/"
    # next = "sessions/caltech"
    # page = 0
    # while next:
    #     getUrl = url + next
    #     resp = json.loads(requests.get(getUrl, headers = headers).content)
    #     data += resp["_items"]
    #     href = resp["_links"].get("next",None)
    #     if href != None:
    #         next = href["href"]
    #     else :
    #         break
    #     page += 1
    #     print(page)
    with open('data.json', 'r+') as f:
        data = json.load(f)
        df = pd.DataFrame(data)
        df.drop(columns=["userInputs"])
        df.to_csv("data.csv", index = False )
            
# getData()
import pandas as pd
import datetime
import pytz
def extractDate(curr_time_str):
    date_time_obj = ""
    if not isinstance(curr_time_str,str):
        return datetime.datetime.strptime("Tue, 16 Oct 2018 09:40:56 GMT",'%a, %d %b %Y %H:%M:%S GMT')
    if 'GMT' in curr_time_str:
        # desired_timezone = pytz.timezone("America/Los_Angeles")
        # orig_timezone = pytz.timezone("UTC")
        date_time_obj = datetime.datetime.strptime(curr_time_str, '%a, %d %b %Y %H:%M:%S GMT') 
        # date_time_obj = orig_timezone.localize(date_time_obj).astimezone(desired_timezone)
        date_time_obj = date_time_obj - datetime.timedelta(hours=7)
    else :
        date_time_obj = datetime.datetime.strptime(curr_time_str, '%a, %d %b %Y %H:%M:%S') 
    # date = date_time_obj.strftime("%m/%d/%Y")
    return date_time_obj
def makeTimeSeries():
    df = pd.read_csv("data.csv")
    df['ConnectionDateTime'] = df['connectionTime'].map(extractDate)
    df['ConnectionDateTime'] = df['ConnectionDateTime'].dt.round("H")

    df['disconnectTime'] = df['disconnectTime'].map(extractDate)
    df['doneChargingTime'] = df['doneChargingTime'].map(extractDate)
    df['DisconnectionDateTime'] = df[['disconnectTime','doneChargingTime']].values.min(axis=1)
    df['DisconnectionDateTime'] = df['DisconnectionDateTime'].dt.round("H")

    df["Duration"] = df["DisconnectionDateTime"] - df["ConnectionDateTime"]
    df["Duration"] = df["Duration"] / datetime.timedelta(hours = 1)

    min_date = min(df["ConnectionDateTime"])
    max_date = max(df["DisconnectionDateTime"])

    # df1 = pd.DataFrame(
	# index=pd.date_range(start=min_date,end=max_date,freq="h"))
    # df1["kwh"] = 0
    # print(df1.head())
    # for i in range(len(df)):
    #     start = df.loc[i,"ConnectionDateTime"]
    #     end = df.loc[i,"DisconnectionDateTime"]
    #     while (start <= end):
    #         df1.loc[str(start),"kwh"] += df.loc[i,"kWhDelivered"]
    #         # print(start)
    #         start = start + datetime.timedelta(hours=1)
    print(min_date,max_date)
    # print(min_date)
    # print((max_date - min_date)/datetime.timedelta(hours= 1))

makeTimeSeries()
