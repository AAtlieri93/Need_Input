#Victor Ruest

#add includes
from .state include State

class ObsticleStop(State):
    def __init__(self):
        super().__init__("OBSTICLE_STOP")

    def update(self, robot, fsm, sensor_data):
        second = sensor_data.second_marker

        if second is not None:
            fsm.target_marker_2 = second

            heading, distance = compute_relative_pose(robot.pose, second.pose)
            if heading > 0:
                fsm.last_seen_direction = LAST_SEEN_LEFT
            elif heading < 0:
                fsm.last_seen_direction = LAST_SEEN_RIGHT

            stop_robot(robot)
            change_state(robot, fsm, FollowSecondMarkerState())
            return

        if fsm.last_seen_direction == LAST_SEEN_LEFT:
            robot_search_left(robot)
        else:
            robot_search_right(robot)
