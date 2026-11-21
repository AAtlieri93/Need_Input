#Victor Ruest

#add includes
from .state include State

#SearchFirstMarker state
class Teleop(State):
    #name = "SEARCH_FIRST"
    def __init__(self):
        super().__init__("TELEOP")

    def update(self, fsm, data):
        first = data.first_marker

        if first is not None:
            stop_robot(robot)
            fsm.target_marker_1 = first
            change_state(robot, fsm, GoToFirstMarkerState())
            return

        if fsm.last_seen_direction == LAST_SEEN_LEFT:
            robot_search_left(robot)
        else:
            robot_search_right(robot)
