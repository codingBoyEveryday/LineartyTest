import sys
import xlsxwriter

api_folder = "/home/pi/ISensitGateway/isensitgwapi/"
if api_folder not in sys.path:
    sys.path.insert(0, api_folder)

from isensit_sql import *
from isensit_dynamo import *
import datetime
device = "Acc"

def read_data(id):
    currentt = datetime.datetime.now()
    created_at = currentt.strftime("%Y-%m-%d %H:%M:%S")
    db.connect_to_db()
    returned_items = dydb.get_angle_item(id,created_at)
    # print("returned item ", returned_items)

    workbook = xlsxwriter.Workbook('test.xlsx')
    worksheet = workbook.add_worksheet()

    # print returned_items[0].keys()
    # print returned_items[0]['created_at'], returned_items[0]['angle']
    # print returned_items[0]['deviceID'], returned_items[0]['angle']
    # print returned_items[0]['angle']
    # print returned_items[0]['created_at']

    row = 0
    col = 0

    for i in returned_items:
        worksheet.write(row, col, i['created_at'])
        worksheet.write(row, col + 1, i['angle'])

        # print i['angle']
        # print i['created_at']
        row +=1
   #
    # workbook.close()

    # dydb.delete_angle_item(id,returned_items)
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
