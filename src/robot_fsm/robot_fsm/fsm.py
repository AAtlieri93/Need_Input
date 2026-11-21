
########################################
#fsm.py
#
#Description - The finite state machine received information 
#              from the fsm_node and decides which action the 
#              robot can take next.
#
#Authors: Victor Ruest
########################################

#!/usr/bin/env python3
from .states.teleop import Teleop
from .states.autonomy import Autonomy
from .states.obsticle_stop import ObsticleStop
from .states.estop import EmergencyStop





#FSM container
class RobotFSM: #robot goes away everywhere?
    def __init__(self):
        self.current_state = Teleop() #change to a starting state of motors off
        self.estop_latched = False
        #self.emergeny = False

    
    def start(self):
        self.current_state.on_enter(self)
        print("Entering state: ", self.current_state.name)

    def update(self, data):
        if data.emergency_stop is True:
            if self.estop_latched is False:
                self.estop_latched = True
                return self.change_state(EmergencyStop())
            
        elif data.emergency_release is True and self.estop_latched is True:
            self.estop_latched = False
            return self.change_state(Teleop())

        return self.current_state.update(self, data)
    
    def change_state(self, new_state):
        if new_state.name != self.current_state.name:
            print("Exiting state:", self.current_state.name)
            self.current_state.on_exit(self) 
            self.current_state = new_state
            return self.current_state.on_enter(self)


