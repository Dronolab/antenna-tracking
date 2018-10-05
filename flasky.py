import time
from flask import Flask, Response, request
from Utility.abstract_process import processAbstract
from tabulate import tabulate
import math
#import time
#from Utility.MultiprocessDataType import antenna_shared_data, uav_shared_data, setpoint_shared_data
#from multiprocessing import Value
from Control.antennaControl import antennaControl


class Flasky(processAbstract):

    def __init__(self, antenna_data, uav_data, actuator_setpoint):
        processAbstract.__init__(self)
        self.antenna_data = antenna_data
        self.uav_data = uav_data
        self.actuator_setpoint = actuator_setpoint
        self.antenna_control = antennaControl(
            self.antenna_data,
            self.uav_data,
            self.actuator_setpoint)

        self.head = [' Pitch',
                     'P_goal',
                     '  Yaw',
                     'Y_goal',
                     'D_Lat',
                     'D_Lon',
                     'D_Alt',
                     'A_Lat',
                     'A_Lon',
                     'A_Alt', ]
        self.header = tabulate([[]], headers=self.head, tablefmt="orgtbl")
        self.app = Flask(__name__)
        self.running = False
        self.refreshing = False
        self.input_template = '<form action="/" method="POST"><p><input type="{}" name="{}" value="{}"></p></form>'
        self.refresher_state = ['REFRESHER ON', 'REFRESHER OFF']
        self.ctrl_state = ['START', 'STOP']
        self.page = ''

        @self.app.route("/", methods=['POST', 'GET'])
        def index():
            if request.method == "POST":

                if list(request.form)[0] == 'switch':
                    print('refresh')
                    if request.form['switch'] == self.refresher_state[1] and self.refreshing:
                        self.refreshing = False
#                        time.sleep(0.1)

                    if request.form['switch'] == self.refresher_state[0] and not self.refreshing:
                        #                       self.page += refresher
                        self.refreshing = True

                elif list(request.form)[0] == 'antenna_ctrl':
                    print('ctrl')
                    if request.form['antenna_ctrl'] == 'START' and not self.running:
                        try:
                            self.antenna_control.start()
                        except:
                            self.antenna_control.soft_stop_everything()
                            self.antenna_control = antennaControl(
                                self.antenna_data, self.uav_data, self.actuator_setpoint)
                            self.antenna_control.start()
                        self.running = True

                    if request.form['antenna_ctrl'] == 'STOP' and self.running:
                        self.antenna_control.soft_stop_everything()
                        self.running = False

                elif list(request.form)[0] == 'reset':
                    print('reset')
                    self.antenna_control.soft_stop_everything()
                    self.running = False
                    self.antenna_control = antennaControl(
                        self.antenna_data, self.uav_data, self.actuator_setpoint)
                    try:
                        self.antenna_control.start()
                        self.running = True
                    except:
                        pass

                else:
                    print('offset')
                    try:
                        off_deg = float(request.form['offset'])
                    except:
                        print('Error on offset input')
                        off_deg = math.degrees(self.antenna_data.getYawOffset())

                    if off_deg >= 90:
                        off_deg = 90
                    if off_deg <= -90:
                        off_deg = -90
                    off = math.radians(off_deg)

                    self.antenna_data.setYawOffset(off)

            def inner():
                self.page = ''
                body = [math.degrees(self.antenna_data.getPitch()),
                        math.degrees(self.actuator_setpoint.getPitch()),
                        math.degrees(self.antenna_data.getYaw()),
                        math.degrees(self.actuator_setpoint.getYaw()),
                        self.uav_data.getLat(),
                        self.uav_data.getLon(),
                        self.uav_data.getAlt(),
                        self.antenna_data.getLat(),
                        self.antenna_data.getLon(),
                        self.antenna_data.getAlt()
                        ]

                values = tabulate(
                    [map(str, body)],
                    headers=self.head,
                    tablefmt="orgtbl",
                    floatfmt=".2f"
                ).split('|\n')[-1]

                # refresher switch
                self.page += self.input_template.format(
                    'submit',
                    'switch',
                    self.refresher_state[self.refreshing]
                )

                # antenna Control
                self.page += self.input_template.format(
                    'submit',
                    'antenna_ctrl',
                    self.ctrl_state[self.running]
                )

                # offset
                self.page += 'Offset:'
                self.page += self.input_template.format(
                    'text',
                    'offset',
                    ''
                )

                # table
                self.page += "<textarea cols='120' rows='15'>"
                self.page += self.header + '\n' + values + '&#13;&#10;\n'

                # list
                self.page += '\n'.join(
                    list(map(lambda x: '\t:\t'.join(map(str, x)), zip(self.head, body))))
                self.page += "</textarea>"

                # Offset value
                self.page += '\n<p>Offset: ' + \
                    str(round(math.degrees(self.antenna_data.getYawOffset()), 2)) + '</p>\n'

                # refresher
                if self.refreshing:
                    self.page += '\n<meta http-equiv="refresh" content=1>\n'
                self.page += 'running:' + str(self.running)

                # reset
                self.page += self.input_template.format(
                    'submit',
                    'reset',
                    'RESET'
                )
                return self.page
            return Response(inner(), mimetype='text/html')

    def process(self):
        self.app.run(host='0.0.0.0')


# for local testing
"""
antenna_data = antenna_shared_data()
uav_data = uav_shared_data()
setpoint_data = setpoint_shared_data()

flasky = Flasky(antenna_data, uav_data, setpoint_data)
flasky.start()
"""
