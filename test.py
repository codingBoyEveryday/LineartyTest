from Fit20Exercise import *  
import datetime
import xlsxwriter

print 'Please input the file name: '
filename = raw_input('')
workbook = xlsxwriter.Workbook(filename + '.xlsx')
worksheet = workbook.add_worksheet()

# time_now = datetime.datetime.now()
# print type(time_now.hour), type(time_now.minute), type(time_now.second)
# t = time_now.strftime('%H:%M:%S')
# t = time_now.hour*3600 + time_now.minute*60 + time_now.second + time_now.microsecond/1000
# print t


a = NewConnectionTest(mac_addr = '7C:EC:79:E3:97:F6', iface = 0)
print('Connecting to EC129')
b = NewConnectionTest(mac_addr = '7C:EC:79:E4:49:12', iface = 1)
print('Connecting to EC140')
# c = NewConnectionTest(mac_addr = '7C:EC:79:E4:5A:EC', iface = 2)
# print('Connecting to EC100')
c = NewConnectionTest(mac_addr = '7C:EC:79:E4:49:66', iface = 2)
print('Connecting to EC120')
d = NewConnectionTest(mac_addr = '7C:EC:79:E3:9A:AF', iface = 3)
print('Connecting to EC125')

# Start from the first cell. Rows and columns are zero indexed.
row = 0
col = 0

for i in range(1, 501):
    time_now = datetime.datetime.now()
    t = time_now.hour * 3600 + time_now.minute * 60 + time_now.second + time_now.microsecond / 1000000
    # t = time_now
    print t
    print 'ec129 ', a.get_data()
    # f.write(str(datetime.datetime.now()) +',ec129,' + str(a.get_data()) + ' ')
    worksheet.write(row, col, t)
    worksheet.write(row, col + 1, 'ec129')
    worksheet.write(row, col + 2, a.get_data())

    # time_now_2 = datetime.datetime.now()
    # t = time_now_2.hour * 3600 + time_now_2.minute * 60 + time_now_2.second + time_now_2.microsecond / 1000
    # print t_2
    print 'ec140 ', b.get_data()
    # f.write(str(datetime.datetime.now()) + ',ec140,' + str(b.get_data()) + ' ')
    worksheet.write(row, col + 3, t)
    worksheet.write(row, col + 4, 'ec140')
    worksheet.write(row, col + 5, b.get_data())

    # time_now_3 = datetime.datetime.now()
    # t_3 = time_now_3.hour * 3600 + time_now_3.minute * 60 + time_now_3.second + time_now_3.microsecond / 1000
    # print t_3
    print 'ec120 ', c.get_data()
    # f.write(str(datetime.datetime.now()) + ',ec401,' + str(c.get_data()) + ' ')
    worksheet.write(row, col + 6, t)
    worksheet.write(row, col + 7, 'ec120')
    worksheet.write(row, col + 8, c.get_data())

    # time_now_4 = datetime.datetime.now()
    # t_4 = time_now_4.hour * 3600 + time_now_4.minute * 60 + time_now_4.second + time_now_4.microsecond / 1000
    # print t_4
    print 'ec125 ', d.get_data()
    # f.write(str(datetime.datetime.now()) + ',ec125,' + str(d.get_data()) + ' ')
    worksheet.write(row, col + 9, t)
    worksheet.write(row, col + 10, 'ec125')
    worksheet.write(row, col + 11, d.get_data())


    # print 'ec000 ', e.get_data()
    # f.write(str(datetime.datetime.now()) + ',ec120,' + str(e.get_data()))
    # f.write("\n")

    row += 1

a.disconnect()
b.disconnect()
c.disconnect()
d.disconnect()
# e.disconnect()

workbook.close()