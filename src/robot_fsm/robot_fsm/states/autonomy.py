#Victor Ruest

#add includes
from .state include State

class Autonomy(State):
    def __init__(self):
        super().__init__("AUTONOMY")

    def on_enter(self, fsm):
        fsm.lost_counter = 0

    def update(self, fsm, sensor_data):
        first = sensor_data.first_marker

        if first is None:
            fsm.lost_counter += 1
            if fsm.lost_counter > 10:
                print("switching to Search_first")
                stop_robot(robot)
                change_state(robot, fsm, SearchFirstMarkerState())
            return

        fsm.lost_counter = 0
        fsm.target_marker_1 = first

        heading, distance = compute_relative_pose(robot.pose, fsm.target_marker_1.pose)

        # reached first cube. change state
        if target_reached(distance):
            stop_robot(robot)
            change_state(robot, fsm, SearchSecondMarkerState())
            return

        # if marker is far off-center, turn toward it
        if heading > 15:
            robot_search_left(robot)
            return
        elif heading < -15:
            robot_search_right(robot)
            return

        # otherwise drive straight toward it
        robot_drive_forward(robot)
