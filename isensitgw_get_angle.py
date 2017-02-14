import sys
import xlsxwriter

import unicodedata
api_folder = "/home/pi/ISensitGateway/isensitgwapi/"
if api_folder not in sys.path:
    sys.path.insert(0, api_folder)

from isensit_sql import *
from isensit_dynamo import *
import datetime
device = "Acc"

def read_data(id):
    db.connect_to_db()
    returned_items = dydb.get_angle_item(id)
    # print type(returned_items)

    workbook = xlsxwriter.Workbook('acc.xlsx')
    worksheet = workbook.add_worksheet()

    row = 0
    col = 0
    timeArray = []
    angleArray = []

    for i in returned_items:
        print i['created_at']
        data = unicodedata.normalize('NFKD', i['created_at']).encode('ascii', 'ignore')

        hour = data[0:2]
        minute = data[3:5]
        second = data[6:8]
        microsecond = data[9:]

        time = float(hour)*3600 + float(minute)*60 + float(second) + (float(microsecond))/1000000
        angle = float(i['angle'])
        timeArray.append(time)
        angleArray.append(angle)
    timeArray.reverse()
    angleArray.reverse()


    for i in range(len(timeArray)):
        worksheet.write(row, col, timeArray[i])
        worksheet.write(row, col + 1, angleArray[i])
        row +=1
    workbook.close()

    db.close_db()





try:
    db = ISensitGWMysql()
#    start_time = db.config_data.get_start_time()
#    end_time = db.config_data.get_end_time()
    dydb = ISensitDynamodb(db.gatewayID, db.config_data.get_dynamodb_table(), db.config_data.get_dynamodb_table_person, device)
#    print ("dydb ", dydb)
except Exception as e:
    print("Error in ISensitDynamodb, reason: ", str(e))


#while True:
#    if db.working():
#    if db.half_hour():
read_data(782)


#        time.sleep(60)
##       else:
##	    print("not working hour")
##	    time.sleep(60)
#    else:
#	print("not working hour")

#start_t = "2017-01-12 13:40:00"
#created_at = "2017-01-13 13:46:20"
#for id in beacons:
#    upload_data(id, created_at,start_t)
