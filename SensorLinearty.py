#!/usr/bin/python
import xlrd
import matplotlib.pyplot as plt
import numpy as np

from matplotlib.ticker import NullFormatter


class SensorLinearty():

    def __init__(self):
        self.required_data_time = []
        self.required_data_angle = []
        self.golden_sensor = []
        self.fit = []
        self.startPoint = 0
        self.endPoint = 0
        self.r = 0

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

    def adjust_start_time(self):
        counter = 0
        for i in range(len(self.required_data_angle)):
            # print len(self.required_data_angle), i
            # print self.required_data_angle[i]
            if i<len(self.required_data_angle)-1:
                if abs((self.required_data_angle[i+1]-self.required_data_angle[i]))>=3:
                    counter +=1
                    if counter > 5:
                        self.startPoint = i
                        break
        self.required_data_time[:] = self.required_data_time[self.startPoint:]
        # print self.new_required_data_time
        self.required_data_angle[:] = self.required_data_angle[self.startPoint:]
        # print self.new_required_data_angle

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

    def make_golden_sensor(self, acc_time, acc_angle):
        index = []
        for i in range(len(self.required_data_time)):
            diff = []
            for j in range(len(acc_time)):
                diff.append(abs(acc_time[j] - self.required_data_time[i]))
            index.append(diff.index(min(diff)))
        for i in range(len(self.required_data_time)):
            self.golden_sensor.append(acc_angle[index[i]])

    def make_fit_function(self):
        slop, y = np.polyfit(self.golden_sensor, self.required_data_angle, 1)
        slop = float(slop)
        y = float(y)
        SStot_all = []
        SSres_all = []
        mean_1 = np.mean(self.required_data_angle)
        for i in self.golden_sensor:
            self.fit.append(slop * i + y)
        for i in range(len(self.golden_sensor)):
            SStot_all.append((self.required_data_angle[i] - mean_1) ** 2)
            SSres_all.append((self.required_data_angle[i] - self.fit[i]) ** 2)
        SStot = sum(SStot_all)
        SSres = sum(SSres_all)
        # self.r = 1 - (SSres / SStot)
        self.r = str(1 - (SSres / SStot))
        # print "The r square is: ", self.r
        result_1 = "The r square is: "
        result_2 = self.r
        result = result_1 + result_2
        return result

    def plot_line_graph(self, line_color = 'k'):
        plt.plot(self.golden_sensor, self.fit, color = line_color)

    def plot_dot_graph(self, dot_marker = "*", dot_color = 'k'):
        plt.scatter(self.golden_sensor, self.required_data_angle, marker = dot_marker, color = dot_color)

    def plot_graph_label(self, string_1, string_2):
        plt.xlabel(string_1)
        plt.ylabel(string_2)

    def plot_text(self, x, y, text):
        plt.text(x, y, text)

    def save_graph(self, figure_title = "Machine sensor linearty"):
        plt.savefig(figure_title)

    def show_graph(self):
        plt.show()


def main():
    mechineSensor_testPathFile = "C:/Users/HPuser/Desktop/sensorLinearty/machine.xlsx"
    accSensor_testPathFile = "C:/Users/HPuser/Desktop/sensorLinearty/acc.xlsx"
    # mechineSensor_testPathFile = "C:/Users/HPuser/Desktop/sensorLinearty/machine.xlsx"
    # accSensor_testPathFile = "C:/Users/HPuser/Desktop/sensorLinearty/acc.xlsx"
    machine_1 = SensorLinearty()
    machine_2 = SensorLinearty()
    machine_3 = SensorLinearty()
    machine_4 = SensorLinearty()
    # machine_5 = SensorLinearty()
    acc = SensorLinearty()

    testWorksheet_1 = machine_1.open_data_file(mechineSensor_testPathFile)
    testWorksheet_2 = machine_2.open_data_file(mechineSensor_testPathFile)
    testWorksheet_3 = machine_3.open_data_file(mechineSensor_testPathFile)
    testWorksheet_4 = machine_4.open_data_file(mechineSensor_testPathFile)
    # testWorksheet_5 = machine_5.open_data_file(mechineSensor_testPathFile)
    testWorksheet_acc = acc.open_data_file(accSensor_testPathFile)

    machine_1.get_data(testWorksheet_1, 0, 2)
    # machine_1.get_data(testWorksheet_1, 1, 3)
    machine_1.adjust_start_time()
    machine_1.ajust_angle()
    # machine_1.adjust_stop_time()

    machine_2.get_data(testWorksheet_2, 3, 5)
    # machine_2.get_data(testWorksheet_2, 5, 7)
    machine_2.adjust_start_time()
    machine_2.ajust_angle()
    # machine_2.adjust_stop_time()

    machine_3.get_data(testWorksheet_3, 6, 8)
    # machine_3.get_data(testWorksheet_3, 9, 11)
    machine_3.adjust_start_time()
    machine_3.ajust_angle()
    # machine_3.adjust_stop_time()

    machine_4.get_data(testWorksheet_4, 9, 11)
    # machine_4.get_data(testWorksheet_4, 13, 15)
    machine_4.adjust_start_time()
    machine_4.ajust_angle()
    # machine_4.adjust_stop_time()

    # machine_5.get_data(testWorksheet_5, 17, 19)
    # machine_5.adjust_start_time()
    # machine_5.ajust_angle()
    # machine_5.adjust_stop_time()

    acc.get_data(testWorksheet_acc,0, 1)
    # acc.get_data(testWorksheet_acc, 8, 14)
    acc.adjust_start_time()
    acc.ajust_angle()
    # acc.adjust_stop_time()
######### ajust the start point of time #################
    min_start_time_point = min(machine_1.required_data_time[0], machine_2.required_data_time[0],
                               machine_3.required_data_time[0], machine_4.required_data_time[0],
                               acc.required_data_time[0])

    # min_start_time_point = min(machine_1.required_data_time[0], machine_2.required_data_time[0],
    #                            machine_3.required_data_time[0], machine_4.required_data_time[0])
    machine_1.shift_start_time(min_start_time_point)
    machine_2.shift_start_time(min_start_time_point)
    machine_3.shift_start_time(min_start_time_point)
    machine_4.shift_start_time(min_start_time_point)
    # machine_5.shift_start_time(min_start_time_point)
    acc.shift_start_time(min_start_time_point)
####### adjust the start point in angle #################
    min_start_angle_point = min(machine_1.required_data_angle[0], machine_2.required_data_angle[0],
                               machine_3.required_data_angle[0], machine_4.required_data_angle[0],
                               acc.required_data_angle[0])

    # min_start_angle_point = min(machine_1.required_data_angle[0], machine_2.required_data_angle[0],
    #                            machine_3.required_data_angle[0], machine_4.required_data_angle[0])
    machine_1.shift_start_angle(min_start_angle_point)
    machine_2.shift_start_angle(min_start_angle_point)
    machine_3.shift_start_angle(min_start_angle_point)
    machine_4.shift_start_angle(min_start_angle_point)
    # machine_5.shift_start_angle(min_start_angle_point)
    acc.shift_start_angle(min_start_angle_point)
######################### make golden sensor for machine 1 ###########################
    machine_1.make_golden_sensor(acc.required_data_time, acc.required_data_angle)
    machine_2.make_golden_sensor(acc.required_data_time, acc.required_data_angle)
    machine_3.make_golden_sensor(acc.required_data_time, acc.required_data_angle)
    machine_4.make_golden_sensor(acc.required_data_time, acc.required_data_angle)
    # machine_5.make_golden_sensor(acc.required_data_time, acc.required_data_angle)
######################### make fit function for the plot and calculate the r^2 for machine 1 #################################
    machine_1.make_fit_function()
    machine_2.make_fit_function()
    machine_3.make_fit_function()
    machine_4.make_fit_function()
    # machine_5.make_fit_function()
#########################  make graph of each machine sensor and the accelermeter ##############################################
    plt.figure(1)

    plt.subplot(221)
    machine_1.plot_line_graph()
    machine_1.plot_dot_graph(dot_color='g')
    machine_1.plot_graph_label("Golden sensor", "Machine sensor 1")
    machine_1.save_graph("Machine sensor 1 linearty")
    plt.grid(True)
    # machine_1.show_graph()

    plt.subplot(222)
    machine_2.plot_line_graph()
    machine_2.plot_dot_graph(dot_color='g')
    machine_2.plot_graph_label("Golden sensor", "Machine sensor 2")
    machine_2.save_graph("Machine sensor 2 linearty")
    plt.grid(True)
    # machine_2.show_graph()

    plt.subplot(223)
    machine_3.plot_line_graph()
    machine_3.plot_dot_graph(dot_color='g')
    machine_3.plot_graph_label("Golden sensor", "Machine sensor 3")
    machine_3.save_graph("Machine sensor 3 linearty")
    plt.grid(True)
    # machine_3.show_graph()

    plt.subplot(224)
    machine_4.plot_line_graph()
    machine_4.plot_dot_graph(dot_color='g')
    machine_4.plot_graph_label("Golden sensor", "Machine sensor 4")
    machine_4.save_graph("Machine sensor 4 linearty")
    plt.grid(True)
    # machine_4.show_graph()

    plt.gca().yaxis.set_minor_formatter(NullFormatter())
    plt.subplots_adjust(top=0.92, bottom=0.08, left=0.10, right=0.95, hspace=0.25, wspace=0.35)

###########  test  ###################################################################################
    # plt.plot(machine_1.required_data_time, machine_1.required_data_angle, color='r')
    # plt.plot(machine_2.required_data_time, machine_2.required_data_angle, color='b')
    # plt.plot(machine_3.required_data_time, machine_3.required_data_angle, color='y')
    # plt.plot(machine_4.required_data_time, machine_4.required_data_angle, color='g')
    # plt.plot(acc.required_data_time, acc.required_data_angle, color='k')

    plt.show()


if __name__ == "__main__":
    main()
