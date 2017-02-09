from Fit20Exercise import *  
import datetime

print 'Please input the file name: '
filename = raw_input('')
f = open(filename+'.txt', 'w')
#f = open(filename+'.xlsx','w')

# a = NewConnectionTest(mac_addr = '34:B1:F7:D0:5A:02', iface = 0)
# print('Connecting to EC401')
a = NewConnectionTest(mac_addr = '7C:EC:79:E3:97:F6', iface = 0)
print('Connecting to EC129')
b = NewConnectionTest(mac_addr = '7C:EC:79:E4:49:12', iface = 1)
print('Connecting to EC140')
#c = NewConnectionTest(mac_addr = '7C:EC:79:E4:5A:EC', iface = 2)
#print('Connecting to EC100')
#d = NewConnectionTest(mac_addr = '7C:EC:79:E3:9A:AF', iface = 3)
#print('Connecting to EC125')
#b = NewConnectionTest(mac_addr = '7C:EC:79:E4:49:66', iface = 1)
#print('Connecting to EC120')

for i in range(1, 500):
    print 'ec000 ', a.get_data()
    f.write(str(datetime.datetime.now()) +',ec129,' + str(a.get_data()) + ' ')
    print 'ec001 ', b.get_data()
    f.write(str(datetime.datetime.now()) + ',ec140,' + str(b.get_data()) + ' ')
    #print 'ec000 ', a.get_data()
    #f.write(str(datetime.datetime.now()) + ',ec401,' + str(a.get_data()) + ' ')
    # print 'ec001 ', d.get_data()
    #f.write(str(datetime.datetime.now()) + ',ec125,' + str(d.get_data()) + ' ')
#    print 'ec000 ', b.get_data()
#    f.write(str(datetime.datetime.now()) + ',ec120,' + str(b.get_data()))
    f.write("\n")

a.disconnect()
b.disconnect()
#c.disconnect()
#d.disconnect()
#e.disconnect()

f.close()
print "Testing is finished !"
