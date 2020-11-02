"""
See https://www.pygame.org/docs/ref/joystick.html for mapping reference
"""
import pygame

# All axes values are [-1,1] float
axes_name_map = {
    'LEFT YAW'           : 0, # LEFT STICK lr
    'LEFT PITCH'         : 1, # LEFT STICK ud
    'RIGHT YAW'          : 2, # RIGHT STICK lr
    'RIGHT PITCH'        : 3, # RIGHT SITCK ud
    'LEFT ROLL INCREASE' : 4, # LEFT TRIGGER
    'RIGHT ROLL INCREASE': 5  # RIGHT TRIGGER
}

button_name_map = {
    'LEFT ROLL DECREASE' : 9,  # L1 - doesn't match documentation
    'RIGHT ROLL DECREASE': 10, # R1 - doesn't match documentation
    'LEFT GRASP'         : 7,  # L3 - doesn't match documentation
    'RIGHT GRASP'        : 8   # R3 - doesn't match documentation
}

MAX_ANGLE = 90  # deg
MIN_ANGLE = -90 # deg

class PS4ControllerWrist(object):
    
    def __init__(self, joystick_id:int):
        pygame.init()
        self.j = pygame.joystick.Joystick(joystick_id)
        self.j.init()
        self.data = {'L-pitch': 0,
                     'L-yaw'  : 0,
                     'L-roll' : 0,
                     'L-grasp': False,
                     'R-pitch': 0,
                     'R-yaw'  : 0,
                     'R-roll' : 0,
                     'R-grasp': False,
                     'roll_speed': 1} # Maximum degrees change per "update"

    def __axis_to_degree(self, axis_value:float) -> float:
        def mapFromTo(x,a,b,c,d):
            y=(x-a)/(b-a)*(d-c)+c
            return y
        
        return mapFromTo(axis_value, -1, 1, MIN_ANGLE, MAX_ANGLE)
    
    def __axis_to_roll_delta(self, axis_value):
        axis_magnitude = (axis_value + 1)/2 # Remember axis are [-1, +1]
        return axis_magnitude

    def set_roll_speed(self, roll_speed:float):
        """ 
        Roll is increased and decreased using L1L2R1R2 to increase and
        decrease, rather than set absolute values.
        """
        assert isinstance(roll_speed, float)
        self.data['roll_speed'] = roll_speed

    def update(self):
        # To keep pygame in sync with the system, you will need to call
        # pygame.event.pump() internally process pygame event handlers to keep
        # everything current. Usually, this should be called once per game
        # loop. Note: Joysticks will not send any events until the device has
        # been initialized.
        pygame.event.pump()

        self.data['L-pitch'] = self.__axis_to_degree(self.j.get_axis(axes_name_map['LEFT PITCH']))
        self.data['L-yaw']   = self.__axis_to_degree(self.j.get_axis(axes_name_map['LEFT YAW']))
        self.data['R-pitch'] = self.__axis_to_degree(self.j.get_axis(axes_name_map['RIGHT PITCH']))
        self.data['R-yaw']   = self.__axis_to_degree(self.j.get_axis(axes_name_map['RIGHT YAW']))
        
        self.data['L-roll'] += \
            (self.__axis_to_roll_delta(self.j.get_axis(axes_name_map['LEFT ROLL INCREASE'])) - \
             self.j.get_button(button_name_map['LEFT ROLL DECREASE'])) * \
                 self.data['roll_speed']
        
        self.data['R-roll'] += \
            (self.__axis_to_roll_delta(self.j.get_axis(axes_name_map['RIGHT ROLL INCREASE'])) - \
             self.j.get_button(button_name_map['RIGHT ROLL DECREASE'])) * \
                 self.data['roll_speed']

        self.data['L-grasp'] = self.j.get_button(button_name_map['LEFT GRASP'])
        self.data['R-grasp'] = self.j.get_button(button_name_map['RIGHT GRASP'])

    def get(self):
        self.update()
        return self.data


if __name__=="__main__":
    import time
    ctrl = PS4ControllerWrist(3)
    try:
        while True:
            print(ctrl.get())
            time.sleep(0.2)

    except KeyboardInterrupt:
        print("EXITING NOW")
        j.quit()