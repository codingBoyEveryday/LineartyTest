#!/usr/bin/python
import xlrd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

from matplotlib.ticker import NullFormatter


class SensorLinearty():

    def __init__(self):
        self.required_data_time = []
        self.required_data_angle = []
        self.reference_sensor = []

        self.fit = []
        self.startPoint = 0
        self.endPoint = 0
        self.r = 0
        self.result = None

    def open_data_file(self, filePath):
        workbook = xlrd.open_workbook(filePath)
        worksheet = workbook.sheet_by_index(0)
        return worksheet

    def get_data(self, current_worksheet, column_1, column_2):
        """if we display the time by second, then the figure is not so good
        #time_tuple = xlrd.xldate_as_tuple(exceltime,0)
        #time_in_second = time_tuple[4]*60 + time_tuple[5]
        #required_data_time.append(time_in_second)
        """

        for rownum in range(current_worksheet.nrows):
            row_values = current_worksheet.row_values(rownum)           ### get values in all columns of every row
            exceltime = current_worksheet.cell_value(rownum,column_1)   ### get the cell value in the column column_1
            self.required_data_time.append(exceltime)                   ### make the list storing time
            self.required_data_angle.append(row_values[column_2])       ### make the list storing degree using data of column_2

    def adjust_start_time(self,min_angle):
        for i in range(len(self.required_data_angle)):
            # print len(self.required_data_angle), i
            # print self.required_data_angle[i]
            if i<len(self.required_data_angle)-1:
                if abs((self.required_data_angle[i]-min_angle))>10:
                    self.startPoint = i
                    break
        self.required_data_time[:] = self.required_data_time[self.startPoint:]
        self.required_data_angle[:] = self.required_data_angle[self.startPoint:]

    def ajust_angle(self):
        for i in range(len(self.required_data_angle)):
            if (self.required_data_angle[i]-self.required_data_angle[i-1]) > 250:
                self.required_data_angle[i] = self.required_data_angle[i] - 360
            elif (self.required_data_angle[i]-self.required_data_angle[i-1]) < -250:
                self.required_data_angle[i] = self.required_data_angle[i] + 360

    def adjust_stop_time(self):
        counter = 0
        for i in range(len(self.required_data_angle)):
            if abs(self.required_data_angle[i+1] - self.required_data_angle[i]) < 2:
                counter = counter + 1
                if counter > 10:
                    self.endPoint = i
                    break
            else:
                counter = 0
        self.required_data_time[:] = self.required_data_time[:self.endPoint]
        self.required_data_angle[:] = self.required_data_angle[:self.endPoint]

    def shift_start_time(self, min_time):
        print type(self.required_data_time[0]), type(min_time)

        shift_time_value = self.required_data_time[0] - min_time
        for i in range(len(self.required_data_time)):
            self.required_data_time[i] = self.required_data_time[i] - shift_time_value

    def shift_start_angle(self, min_angle):
        shift_angle_value = self.required_data_angle[0] - min_angle
        for i in range(len(self.required_data_angle)):
            self.required_data_angle[i] = self.required_data_angle[i] - shift_angle_value

    def make_reference_angle_xaxis(self, reference_time, reference_angle):
        self.reference_sensor = []
        index = []
        for i in range(len(self.required_data_time)):
            diff = []
            for j in range(len(reference_time)):
                diff.append(abs(reference_time[j] - self.required_data_time[i]))
            index.append(diff.index(min(diff)))
        for i in range(len(self.required_data_time)):
            self.reference_sensor.append(reference_angle[index[i]])

    def make_fit_function(self):
        self.fit = []
        slop, y = np.polyfit(self.reference_sensor, self.required_data_angle, 1)
        slop = float(slop)
        y = float(y)


        SStot_all = []
        SSres_all = []
        mean_1 = np.mean(self.required_data_angle)
        for i in self.reference_sensor:
            self.fit.append(slop * i + y)
        for i in range(len(self.reference_sensor)):
            SStot_all.append((self.required_data_angle[i] - mean_1) ** 2)
            SSres_all.append((self.required_data_angle[i] - self.fit[i]) ** 2)
        SStot = sum(SStot_all)
        SSres = sum(SSres_all)
        self.r = (1 - (SSres / SStot))
        self.r = float("{0:.4f}".format(self.r))
        self.r = str(self.r)
        result_1 = "r =  "
        result_2 = self.r
        self.result = result_1 + result_2
        return self.result

    def plot_line_graph(self, line_color = 'k'):
        plt.plot(self.reference_sensor, self.fit, color = line_color)

    def plot_dot_graph(self, dot_marker = "*", dot_color = 'k'):
        plt.scatter(self.reference_sensor, self.required_data_angle, marker = dot_marker, color = dot_color)

    def plot_graph_label(self, string_1, string_2):
        plt.xlabel(string_1)
        plt.ylabel(string_2)

    def plot_text(self, x, y):
        plt.text(x, y, self.result)

    def save_graph(self, figure_title = "Machine sensor linearty"):
        plt.savefig(figure_title)

    def show_graph(self):
        plt.show()


def main():
    # mechineSensor_testPathFile = "C:/Users/HPuser/Desktop/sensorLinearty/machine.xlsx"
    # accSensor_testPathFile = "C:/Users/HPuser/Desktop/sensorLinearty/acc.xlsx"
    mechineSensor_testPathFile = "machine.xlsx"
    accSensor_testPathFile = "acc.xlsx"
    machine_1 = SensorLinearty()
    machine_2 = SensorLinearty()
    machine_3 = SensorLinearty()
    # machine_4 = SensorLinearty()
    golden_sensor = SensorLinearty()
    acc = SensorLinearty()

    testWorksheet_1 = machine_1.open_data_file(mechineSensor_testPathFile)
    testWorksheet_2 = machine_2.open_data_file(mechineSensor_testPathFile)
    testWorksheet_3 = machine_3.open_data_file(mechineSensor_testPathFile)
    # testWorksheet_4 = machine_4.open_data_file(mechineSensor_testPathFile)
    testWorksheet_golden = golden_sensor.open_data_file(mechineSensor_testPathFile)
    testWorksheet_acc = acc.open_data_file(accSensor_testPathFile)


    machine_1.get_data(testWorksheet_1, 0, 2)
    # machine_1.get_data(testWorksheet_1, 1, 3)
    machine_2.get_data(testWorksheet_2, 3, 5)
    machine_3.get_data(testWorksheet_3, 6, 8)
    golden_sensor.get_data(testWorksheet_golden, 9, 11)
    acc.get_data(testWorksheet_acc, 0, 1)

####### adjust the start point in angle #################
    min_start_angle_point = min(machine_1.required_data_angle[0], machine_2.required_data_angle[0],
                               machine_3.required_data_angle[0], golden_sensor.required_data_angle[0],
                               acc.required_data_angle[0])

    machine_1.shift_start_angle(min_start_angle_point)
    machine_2.shift_start_angle(min_start_angle_point)
    machine_3.shift_start_angle(min_start_angle_point)
    # machine_4.shift_start_angle(min_start_angle_point)
    golden_sensor.shift_start_angle(min_start_angle_point)
    acc.shift_start_angle(min_start_angle_point)


     								
    machine_1.adjust_start_time(min_start_angle_point)
    machine_1.ajust_angle()
    # machine_1.adjust_stop_time()

    # machine_2.get_data(testWorksheet_2, 3, 5)
    # machine_2.get_data(testWorksheet_2, 5, 7)
    machine_2.adjust_start_time(min_start_angle_point)
    machine_2.ajust_angle()
    # machine_2.adjust_stop_time()

    # machine_3.get_data(testWorksheet_3, 6, 8)
    # machine_3.get_data(testWorksheet_3, 9, 11)
    machine_3.adjust_start_time(min_start_angle_point)
    machine_3.ajust_angle()
    # machine_3.adjust_stop_time()

    # machine_4.get_data(testWorksheet_4, 9, 11)
    # machine_4.get_data(testWorksheet_4, 13, 15)
    # machine_4.adjust_start_time(min_start_angle_point)
    # machine_4.ajust_angle()
    # machine_4.adjust_stop_time()

    # golden_sensor.get_data(testWorksheet_golden, 9, 11)
    golden_sensor.adjust_start_time(min_start_angle_point)
    golden_sensor.ajust_angle()
    # golden_sensor.adjust_stop_time()

    # acc.get_data(testWorksheet_acc,0, 1)
    # acc.get_data(testWorksheet_acc, 8, 14)
    acc.adjust_start_time(min_start_angle_point)
    acc.ajust_angle()
    # acc.adjust_stop_time()
######### ajust the start point of time #################
    min_start_time_point = min(machine_1.required_data_time[0], machine_2.required_data_time[0],
                               machine_3.required_data_time[0], golden_sensor.required_data_time[0],
                               acc.required_data_time[0])

    machine_1.shift_start_time(min_start_time_point)
    machine_2.shift_start_time(min_start_time_point)
    machine_3.shift_start_time(min_start_time_point)
    # machine_4.shift_start_time(min_start_time_point)
    golden_sensor.shift_start_time(min_start_time_point)
    acc.shift_start_time(min_start_time_point)



######################### plot  ###########################
    plt.figure(1)
    #
    machine_1.make_reference_angle_xaxis(golden_sensor.required_data_time, golden_sensor.required_data_angle)
    machine_1.make_fit_function()
    plt.subplot(331)
    machine_1.plot_line_graph()
    machine_1.plot_dot_graph(dot_color='g')
    machine_1.plot_graph_label("Golden sensor", "Machine sensor 1")
    machine_1.plot_text(5, 200)
    plt.grid(True)
    #
    machine_2.make_reference_angle_xaxis(golden_sensor.required_data_time, golden_sensor.required_data_angle)
    machine_2.make_fit_function()
    plt.subplot(332)
    machine_2.plot_line_graph()
    machine_2.plot_dot_graph(dot_color='g')
    machine_2.plot_graph_label("Golden sensor", "Machine sensor 2")
    machine_2.plot_text(5, 200)
    plt.grid(True)
    #
    machine_3.make_reference_angle_xaxis(golden_sensor.required_data_time, golden_sensor.required_data_angle)
    machine_3.make_fit_function()
    plt.subplot(333)
    machine_3.plot_line_graph()
    machine_3.plot_dot_graph(dot_color='g')
    machine_3.plot_graph_label("Golden sensor", "Machine sensor 3")
    machine_3.plot_text(5, 200)
    plt.grid(True)
    #
    golden_sensor.make_reference_angle_xaxis(acc.required_data_time, acc.required_data_angle)
    golden_sensor.make_fit_function()
    plt.subplot(334)
    golden_sensor.plot_line_graph()
    golden_sensor.plot_dot_graph(dot_color='g')
    golden_sensor.plot_graph_label("Acc", "Golden sensor")
    golden_sensor.plot_text(5, 200)
    plt.grid(True)
    #
    machine_1.make_reference_angle_xaxis(acc.required_data_time, acc.required_data_angle)
    machine_1.make_fit_function()
    plt.subplot(335)
    machine_1.plot_line_graph()
    machine_1.plot_dot_graph(dot_color='g')
    machine_1.plot_graph_label("Acc", "Machine sensor 1")
    machine_1.plot_text(5, 200)
    plt.grid(True)
    #
    machine_2.make_reference_angle_xaxis(acc.required_data_time, acc.required_data_angle)
    machine_2.make_fit_function()
    plt.subplot(336)
    machine_2.plot_line_graph()
    machine_2.plot_dot_graph(dot_color='g')
    machine_2.plot_graph_label("Acc", "Machine sensor 2")
    machine_2.plot_text(5, 200)
    plt.grid(True)
    #
    machine_3.make_reference_angle_xaxis(acc.required_data_time, acc.required_data_angle)
    machine_3.make_fit_function()
    plt.subplot(337)
    machine_3.plot_line_graph()
    machine_3.plot_dot_graph(dot_color='g')
    machine_3.plot_graph_label("Acc", "Machine sensor 3")
    machine_3.plot_text(5, 200)
    plt.grid(True)
    #
    #
    plt.gca().yaxis.set_minor_formatter(NullFormatter())
    plt.subplots_adjust(top=0.92, bottom=0.08, left=0.10, right=0.95, hspace=0.25, wspace=0.35)

###########  test  ###################################################################################
#    plt.plot(machine_1.required_data_time, machine_1.required_data_angle, color='r')
#    plt.plot(machine_2.required_data_time, machine_2.required_data_angle, color='b')
#    plt.plot(machine_3.required_data_time, machine_3.required_data_angle, color='y')
#    plt.plot(golden_sensor.required_data_time, golden_sensor.required_data_angle, color='g')
#    plt.plot(acc.required_data_time, acc.required_data_angle, color='k')


    plt.savefig("Linearty_2")
    # plt.show()


if __name__ == "__main__":
    main()
