from Fit20Exercise import *  
import datetime
import xlsxwriter

print 'Please input the file name: '
filename = raw_input('')
workbook = xlsxwriter.Workbook(filename + '.xlsx')
worksheet = workbook.add_worksheet()

time_now = datetime.datetime.now()
t = time_now.strftime('%H:%M:%S')


a = NewConnectionTest(mac_addr = '7C:EC:79:E3:97:F6', iface = 0)
print('Connecting to EC129')
b = NewConnectionTest(mac_addr = '7C:EC:79:E4:49:12', iface = 1)
print('Connecting to EC140')
# c = NewConnectionTest(mac_addr = '7C:EC:79:E4:5A:EC', iface = 2)
# print('Connecting to EC100')
# d = NewConnectionTest(mac_addr = '7C:EC:79:E3:9A:AF', iface = 3)
# print('Connecting to EC125')
# b = NewConnectionTest(mac_addr = '7C:EC:79:E4:49:66', iface = 1)
# print('Connecting to EC120')

# Start from the first cell. Rows and columns are zero indexed.
row = 0
col = 0

for i in range(1, 50):
    print 'ec129 ', a.get_data()
    # f.write(str(datetime.datetime.now()) +',ec129,' + str(a.get_data()) + ' ')
    worksheet.write(row, col, str(t))
    worksheet.write(row, col + 1, 'ec129')
    worksheet.write(row, col + 2, str(a.get_data()))

    print 'ec140 ', b.get_data()
    # f.write(str(datetime.datetime.now()) + ',ec140,' + str(b.get_data()) + ' ')
    worksheet.write(row, col + 3, str(t))
    worksheet.write(row, col + 4, 'ec140')
    worksheet.write(row, col + 5, str(b.get_data()))
    # print 'ec000 ', c.get_data()
    # f.write(str(datetime.datetime.now()) + ',ec401,' + str(c.get_data()) + ' ')
    # print 'ec001 ', d.get_data()
    # f.write(str(datetime.datetime.now()) + ',ec125,' + str(d.get_data()) + ' ')
    # print 'ec000 ', e.get_data()
    # f.write(str(datetime.datetime.now()) + ',ec120,' + str(e.get_data()))
    # f.write("\n")

    row += 1





a.disconnect()
b.disconnect()
# c.disconnect()
# d.disconnect()
# e.disconnect()

workbook.close()