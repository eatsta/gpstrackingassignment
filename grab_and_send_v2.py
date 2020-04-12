import psycopg2
from datetime import datetime
import pandas as pd
import requests
import json
from time import sleep
headers = {
        'Accept': 'application/json',
        'Authorization': 'key ttn-account-Y',
    }


def grab_from_website():
    #GRABING DATA FROM WEBSITE
    response = requests.get('https://eaapmw_gps.data.thethingsnetwork.org/api/v2/query?last=30s', headers=headers)
    validation = str(response)
    if validation == '<Response [204]>':
        print("No data")
        sleep(5)
        local_data=0
        return(local_data)
    else:
        data_from_web = json.dumps(response.json())
        local_data = json.loads(data_from_web)
    return(local_data)

def remove_raw(data_with_raw):
    #REMOVING RAW FROM JSON
    for element in data_with_raw:
        if 'raw' in element:
            del element['raw']
    return(data_with_raw)


def adjust_data(data_without_raw):
    result=[]
    for temp in data_without_raw:
        newTime = temp['time'].split('.')
        newCoord = temp['receivedString'].split(',')
        latitude = str(newCoord[0]).replace('(', '')
        longtitude = str(newCoord[1]).replace(')', '')
        longtitude = longtitude.replace(' ', '')
        result.append({"device_id": temp["device_id"],
                       "time": newTime[0],
                       "Latitude": latitude,
                       "Longtitude": longtitude})
    fixed_data = json.dumps(result)
    final_data = json.loads(fixed_data)
    return(final_data)

def send_data_to_db(final_data):
    con = psycopg2.connect(database="", user="", password="", host="localhost", port="5432")
    cur = con.cursor()
    for element in final_data:
        # COLLECTING DATA
        ###########################
        now = datetime.now()
        pd_now = pd.Timestamp(now)
        freq = '1s'
        pd_round = pd_now.round(freq)
        dt_round = pd_round.to_pydatetime()
        ###########################
        device_id = element['device_id']
        time = element['time']
        latitude = element['Latitude']
        longtitude = element['Longtitude']
        record_to_insert = (dt_round, device_id, time, latitude, longtitude)
        insert_query = """ INSERT INTO iotdata (time_db, device_id, time_iot,latitude,longtitude) VALUES (%s,%s,%s,%s,%s)"""
        cur.execute(insert_query, record_to_insert)
        con.commit()
    con.close()
    sleep(30)


while True:
    data_with_raw=grab_from_website()
    while data_with_raw!=0:
        data_without_raw=remove_raw(data_with_raw)
        adjusted_data=adjust_data(data_without_raw)
        send_data_to_db(adjusted_data)
        sleep(25)
