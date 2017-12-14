The control packages is responsible for the Antenna behaviour.

It takes the multiples sensors inputs and convert it into a command for the actuators.

It manage the error handeling for bad uav behaviour and manage the dynamic of the antenna.

General antenna behavoir:
    control type :
            yaw : 0-360
            pitch 0-90

    The antenna must have a smimple way to select multiturn or singleturn:
        - multiturn allow the antenna to du multiple rotations along the yaw axis.
        - singleturn make sure that the antenna dosent do more thant a 30 rotation along the yaw axis.

