from random import randint
from PyQt4.QtGui import QTextDocument, QPrinter, QApplication
import sys
class Simulation:
    def __init__(self):
        pass
    def get_data(self):
        inter_arrival_time = input('Enter Inter Arrival Time(ex: 0-1): ')
        time = inter_arrival_time.split('-')
        inter_rand = int(input('Enter Random digit Limit for Inter Arrival Time: '))
        if not len(time) == 2:
            print('Please Enter Inter Arrival time in right format')
        try:
            start_time = float(time[0].strip())
            end_time = float(time[1].strip())
            sim_time = int(input('Enter Simulation Time: '))
        except:
            print('Please Enter numbers')
            exit(0)
        arrival_probability = 1 / ((end_time - start_time) + 1)
        self.intr_time = []; self.service_time = []; self.service_time_pr = []; self.service_priority = []; self.random_digit = []; self.random_digit_serv = []
        for i in range(int(start_time), int(end_time) + 1):
            self.intr_time.append(i)
        queue_channel_no = int(input('Enter Numbers of Channel: '))
        for i in range(0, queue_channel_no):
            print("Please input data for 'Channel " + str(i + 1) + "'. Enter q/Q to End of inserting")
            if queue_channel_no > 1:
                priority = int(input('Enter priority (higher compute from lower value 0,1,2,3): '))
            else:
                priority = 0
            self.service_priority.append(priority)
            service_times = []
            service_proba = []
            while True:
                s_time = input('Enter service time: ')
                if s_time == 'q' or s_time == 'Q':
                    break
                s_prob = input('Enter Service Probability: ')
                try:
                    service_times.append(float(s_time.strip()))
                    service_proba.append(float(s_prob.strip()))
                except:
                    print('please Enter numbers')
                    exit(0)
            self.service_time.append(service_times)
            self.service_time_pr.append(service_proba)
        for i in range(0, sim_time):
            if i == 0:
                self.random_digit.append('-')
            self.random_digit.append(randint(0, inter_rand))
        for i in range(0, sim_time):
            self.random_digit_serv.append(randint(0, 100))
        return inter_rand, sim_time, arrival_probability, self.random_digit, self.service_time, self.service_time_pr, self.service_priority, self.intr_time, self.random_digit_serv
if __name__ == '__main__':
    sim = Simulation()
    rand_dig, sim_time, arrival_probability, arri_randDigit, service_time, service_time_pr, service_priority, intr_time, randDigit_serv = sim.get_data()
    customer_num = []; timeBet_arr = []; clockTime_arr = []; server_status = []; server_use = []; server_name = []; time_ser_begin = []
    serve_time = []; end_serve = []; wait_queue = []
    for j in range(0, len(service_priority)):
        server_status.append('free')
        server_name.append('server_'+str(j+1))
    start_time = c_no = wait = process = 0
    wait_list = end_serve_flag = []
    while start_time <= sim_time:
        server_p = []
        for i in range(len(end_serve)-1, -1, -1):
            if end_serve[i] == start_time:
                server_status[server_name.index(server_use[i])] = 'free'
        for j in range(0, len(server_status)):
            if server_status[j] == 'free':
                server_p.append(service_priority[j])
        if len(server_p) > 0:
            if c_no == 0:
                timeBet_arr.append('-')
                clockTime_arr.append(0)
                customer_num.append(c_no + 1)
            else:
                if process != c_no:
                    for i in range(1, len(intr_time) + 1):
                        if arrival_probability * i * rand_dig >= arri_randDigit[c_no]:
                            timeBet_arr.append(intr_time[i - 1])
                            break
                    clockTime_arr.append(int(timeBet_arr[c_no]) + int(clockTime_arr[c_no - 1]))
                    customer_num.append(c_no + 1)
                    process = c_no
            if start_time >= clockTime_arr[c_no]:
                choose_serve_p = service_priority.index(min(server_p))
                server_use.append(server_name[choose_serve_p])
                server_status[choose_serve_p] = 'busy'
                time_ser_begin.append(start_time)
                for i in range(0, len(service_time_pr[choose_serve_p])):
                    serv_p = 0
                    for j in range(i, -1, -1):
                        serv_p += service_time_pr[choose_serve_p][j]
                    if serv_p * 100 >= randDigit_serv[c_no]:
                        serve_time.append(service_time[choose_serve_p][i])
                        break
                end_serve.append(start_time + serve_time[c_no])
                if end_serve[-1] > sim_time:
                    del end_serve[-1]; del serve_time[-1]; del server_use[-1]; del clockTime_arr[-1]; del timeBet_arr[-1]; del customer_num[-1]
                    for fre in range(0, len(server_status)):
                        server_status[fre] = 'free'
                    break
                c_no += 1
        start_time += 1
    table = '<html><head><style>table, th, td {border: 1px solid black;border-collapse: collapse;'
    table += '} th,td{text-align: center;}</style></head><body><center><table><tr><th rowspan = "2">No</th>'
    table += '<th rowspan = "2">Random Digit For Arrival</th><th rowspan = "2">Time Between Arrival</th>'
    table += '<th rowspan = "2">Clock Time of Arrival</th><th rowspan = "2">Random Digit For Service</th>'
    for i in server_name:
        table += '<th colspan="3">'+str(i)+'</th>'
    table += '<th rowspan = "2">Wait In Queue</th></tr><tr>'
    for i in range(0, len(server_name)):
        table += '<th>Service Start</th><th>Service Time</th><th>Service end</th>'
    table += '</tr>'
    for i in range(0, len(end_serve)):
        table += '<tr><td>' + str(customer_num[i]) + '</td><td>' + str(arri_randDigit[i]) + '</td><td>' + str(timeBet_arr[i]) + '</td>'
        table += '<td>' + str(clockTime_arr[i]) + '</td><td>' + str(randDigit_serv[i]) + '</td>'
        for j in range(0, len(server_name)):
            if server_use[i] == server_name[j]:
                table += '<td>' + str(time_ser_begin[i]) + '</td><td>' + str(serve_time[i]) + '</td><td>' + str(end_serve[i]) + '</td>'
            else:
                table += '<td></td><td></td><td></td>'
        table += '<td>'+str(time_ser_begin[i] - clockTime_arr[i])+'</td></tr>'
    table += '</table></center></body></html>'
    file = open('table.html','w+')
    file.write(table)
    file.close()
    app = QApplication(sys.argv)
    doc = QTextDocument()
    doc.setHtml(open("table.html").read())
    printer = QPrinter()
    printer.setOutputFileName("simulation.pdf")
    printer.setPageSize(QPrinter.A4);
    printer.setPageMargins(15, 15, 15, 15, QPrinter.Millimeter);
    doc.print_(printer)
    # 'table.html'.unlink()
