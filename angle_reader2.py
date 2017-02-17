#!/usr/bin/python
import sys
from decimal import * 
# adding api to path
api_folder = "/home/pi/ISensitGateway/isensitgwapi/" 
if api_folder not in sys.path:
    sys.path.insert(0, api_folder) 
from isensit_device_adapter import * 
from lib.blescan import * 
import bluetooth._bluetooth as bluez 
from isensit_sql import * 
from isensit_dynamo import * 
import time 
import threading 
import datetime 
import math 
# from ws4py.websocket import WebSocket
deviceInfoDict = {} 
deviceValueDict = {} 
row_count = 0 
data = None 
count = 0 
table_name = "acc_beacon_table" 
device = "Acc"
#while True:
db=None

import tornado.httpserver
import tornado.websocket
import tornado.ioloop
import tornado.web


ws = None

clients = []
s = None


dev_id = 0 
rssi = 0
cal_pitch = 0 
row_count = 0 

start = datetime.datetime.now()
endt = start + datetime.timedelta(minutes=3)
print ("endtime ", endt)


def upload_data():
    global db
    try:

    	db.connect_to_db()
    	data = db.read_all_data("angle_table")
    	if data is None:
            print("No data left")
    	else:
 	    row_count = data[len(data)-1]["row_count"]
	    print("row_count ", row_count) 
	    dydb.insert_angle_data(data)		
	    db.delete_angle_data(row_count+1)
		
		   	
    except Exception as e:
        print("Error in Aws Sender, reason: ", str(e))
    else:
        db.close_db() 
def get_acc(r):
    id = r["device_info"]["ID"][0]

    accx = float(r["values"]["ACCX"][0])
    accy = float(r["values"]["ACCY"][0])
    accz = float(r["values"]["ACCZ"][0])
    acc_sum = math.sqrt(math.pow(accx,2)+math.pow(accy,2)+math.pow(accz,2))
    rssi = r["values"]["RSSI"][0]
#get roll 0-360:
    rollacc = atan2(accy, sqrt(pow(accz,2) + pow(accx,2))) 
    if accx < 0:
       if accy > 0:
            rollacc = pi - rollacc
       else:
            rollacc = -pi - rollacc
    rollacc = rollacc * 180/pi
    if rollacc < 0:
	rollacc = 360 + rollacc
    currentt = datetime.datetime.now()
    currentt2 = datetime.datetime.now().strftime('%H:%M:%S.%f') 
   
    print("tme ",currentt2)
    db.insert_angle_data(int(id.strip('\0')), accx, accy, accz, rollacc, currentt2, acc_sum)

    print datetime.datetime.now()
    print "roll : ", rollacc

sock = hci_start_scan(dev_id) 

try:
    db = ISensitGWMysql()
    dydb = ISensitDynamodb(db.gatewayID, db.config_data.get_dynamodb_table(), db.config_data.get_dynamodb_table_person(), device) 
    start_time = db.config_data.get_start_time()
    end_time = db.config_data.get_end_time()
    db.connect_to_db()
#    db.delete_all_data("angle_table")
except Exception as e:
    print("Error in initializing db, reason: ", str(e))
    running = False
    exit(-1)
    s.close()

class WSHandler(tornado.websocket.WebSocketHandler):
  def open(self):
    print 'New connection was opened'
    self.write_message("Welcome to my websocket!")

  def on_message(self, message):
    print 'Incoming message:', message
    self.write_message("You said: " + message)

  def on_close(self):
    print 'Connection was closed...'

  def broadcast(self,message):
    try:
        for client in self.clients:
            client.write_message(message)
    except Exception as e:
        print("Error sending broadcast: "+e)


application = tornado.web.Application([
  (r'/ws', WSHandler),
])

def startWS():
  http_server = tornado.httpserver.HTTPServer(application)
  http_server.listen(8888)
  mainLoop = tornado.ioloop.IOLoop.instance()
  mainLoop.start()

 
threading.Thread(target = startWS).start()

try:
    print("Start reading data")

    while True:
        returnedList = parse_events(sock)
        if returnedList is not None:
            if returnedList is not False:
                if "782" in returnedList["device_info"]["ID"][0]:
		  print("yes" )
                  db.connect_to_db()
                  get_acc(returnedList)
	          upload_data()
		  print("end time ", endt.strftime("%H:%M:%S"))
		  print("now time ", datetime.datetime.now().strftime("%H:%M:%S"))
        if datetime.datetime.now() > endt:
	    running = False
	    exit(-1)
            s.close()
except Exception as e:
    print("Error in main loop: ", str(e))
    running = False
    exit(-1)
    s.close()





