#Victor Ruest

#add includes
from .state import State
from geometry_msgs.msg import Twist
class EmergencyStop(State):
    def __init__(self):
        super().__init__("EMERGENCY_STOP")

    def on_enter(self, fsm):
        return Twist() # twist defaults to zero
    def update(self, fsm, data):
        return Twist()
        

