#Victor Ruest
#retool for fundementals lab
########################################
#fsm.py
#
#Description - This program utilizes Cozmo and the marker cube location to navigate towards the cube using FSM and 
#state changes.
#
#Authors: Victor Ruest
#         Matt Valeri
########################################

#!/usr/bin/env python3
#!c:/Python35/python3.exe -u
import asyncio
import sys
import cv2
import numpy as np
import cozmo
import time
import os
import math
from cozmo.oled_face import convert_image_to_screen_data
from PIL import Image, ImageDraw

#Constants
#TURN_SPEED = 20
#FORWARD_SPEED = 40
#SLOW_SPEED = 10
#FACE_ANGLE_THRESHOLD = 4
#DISTANCE_THRESHOLD = 100

#create marker ids
#FIRST_MARKER_ID = cozmo.objects.CustomObjectTypes.CustomType00
3SECOND_MARKER_ID = cozmo.objects.CustomObjectTypes.CustomType01

#LAST_SEEN_LEFT = -1
#LAST_SEEN_RIGHT = 1
#DEFAULT_SEARCH_DIRECTION = LAST_SEEN_LEFT

#make sure cozmo starts a s expected
def start_up(robot):
    stop_robot(robot)
    robot.set_head_angle(cozmo.util.degrees(4)).wait_for_completed()

#show state_name on Cozmo screen
#def display_state_on_face(robot, state_name):
#    try:
#        img = Image.new('1', cozmo.oled_face.dimensions())
#        draw = ImageDraw.Draw(img)
#        draw.text((5, 20), state_name[:8], fill = 1)
#        face_image = convert_image_to_screen_data(img, invert_image = True)
#        robot.display_oled_face_image(face_image, duration_ms = 500.0)
#    except Exception as e:
#        print("Face display error: ", e)

#make cozmo beep
#def beep(robot):
    #play beep sound
#    robot.say_text("beep").wait_for_completed()

#retool to send this to fsm_node?
def stop_robot(robot):
    robot.drive_wheels(0, 0)

#keep and retool
def change_state(robot, fsm, new_state):
    print("Exiting state:", fsm.current_state.name)
    fsm.current_state.on_exit(robot,fsm)
    beep(robot)
    fsm.current_state = new_state
    display_state_on_face(robot, new_state.name)
    print("Entering state:", new_state.name)
    fsm.current_state.on_enter(robot, fsm)

#wheel controls... get rid of?
#def robot_search_left(robot):
#    robot.drive_wheels(-TURN_SPEED, TURN_SPEED)

#def robot_search_right(robot):
#    robot.drive_wheels(TURN_SPEED, -TURN_SPEED)

#def robot_drive_forward(robot):
#    robot.drive_wheels(FORWARD_SPEED, FORWARD_SPEED)

#def robot_steer_left(robot):
#    robot.drive_wheels(SLOW_SPEED, FORWARD_SPEED)

#def robot_steer_right(robot):
#    robot.drive_wheels(FORWARD_SPEED, SLOW_SPEED)

#depending on what cozmo is seeing, returns marker1, marker2, or None. this goes too
#def get_visible_marker_info(robot):
#    first_marker = None
#    second_marker = None
#    visible = list(robot.world.visible_objects)
#    for v in visible:
#        try:
#            obj_type = v.object_type
#        except AttributeError:
#            continue
#        if obj_type == FIRST_MARKER_ID:
#            first_marker = v
#        elif obj_type == SECOND_MARKER_ID:
#            second_marker = v

#    return first_marker, second_marker

#uses position of cozmo and marker to calculate distance to marker and heading
#def compute_relative_pose(robot_pose, marker_pose):
#    dx = marker_pose.position.x - robot_pose.position.x
#    dy = marker_pose.position.y - robot_pose.position.y
   
#    angle_to_marker = math.degrees(math.atan2(dy, dx))
#    robot_heading = robot_pose.rotation.angle_z.degrees
    
#    heading = angle_to_marker - robot_heading

#    while heading > 180:
#        heading -= 360
#    while heading < -180:
#        heading += 360
    
    #magnitude formula to get distance
#    distance = math.sqrt(dx**2 + dy**2)

#    return heading, distance

#def target_reached(distance):
#    return distance <= 120

#Base state class keeping for sure
class State:
    def __init__(self, name):
        self.name = name
    
    def on_enter(self, robot, fsm):
        pass

    def on_exit(self, robot, fsm):
        pass
        
    def update(self, robot, fsm, sensor_data):
        pass

#our states used to have more complex steering and "bias timers" in order to attempt
#getting cozmo to face the marker head on. We removed and simplified once we learned
#this wasn't needed.

#SearchFirstMarker state
class SearchFirstMarkerState(State):
    #name = "SEARCH_FIRST"
    def __init__(self):
        super().__init__("SEARCH_FIRST")

    def update(self, robot, fsm, sensor_data):
        first = sensor_data.first_marker

        if first is not None:
            stop_robot(robot)
            fsm.target_marker_1 = first
            change_state(robot, fsm, GoToFirstMarkerState())
            return

        if fsm.last_seen_direction == LAST_SEEN_LEFT:
            robot_search_left(robot)
        else:
            robot_search_right(robot)


class GoToFirstMarkerState(State):
    def __init__(self):
        super().__init__("GOTO_FIRST")

    def on_enter(self, robot, fsm):
        fsm.lost_counter = 0

    def update(self, robot, fsm, sensor_data):
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

class SearchSecondMarkerState(State):
    def __init__(self):
        super().__init__("SEARCH_SECOND")

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

class FollowSecondMarkerState(State):
    def __init__(self):
        super().__init__("FOLLOW_SECOND")

    def update(self, robot, fsm, sensor_data):
        second = sensor_data.second_marker

        if second is None:
            stop_robot(robot)
            change_state(robot, fsm, SearchSecondMarkerState())
            return

        fsm.target_marker_2 = second

        heading, distance = compute_relative_pose(robot.pose, second.pose)
        print("FOLLOW_SECOND heading:", heading, "distance:", distance)

        if heading > 0:
            fsm.last_seen_direction = LAST_SEEN_LEFT
        elif heading < 0:
            fsm.last_seen_direction = LAST_SEEN_RIGHT

        if heading > FACE_ANGLE_THRESHOLD:
            robot_steer_left(robot)
            return
        elif heading < -FACE_ANGLE_THRESHOLD:
            robot_steer_right(robot)
            return

        if distance > DISTANCE_THRESHOLD:
            robot_drive_forward(robot)
            return

        stop_robot(robot)
        beep(robot)
        print("SECOND CUBE REACHED")
        return

#FSM container
class RobotFSM:
    def __init__(self):
        self.current_state = SearchFirstMarkerState()
        self.last_seen_direction = DEFAULT_SEARCH_DIRECTION
        self.target_marker_1 = None
        self.target_marker_2 = None
        self.lost_counter = 0
    
    def start(self, robot):
        self.current_state.on_enter(robot, self)
        print("Entering state: ", self.current_state.name)

    def update(self, robot, sensor_data):
        self.current_state.update(robot, self, sensor_data)

#Sensor data container
class SensorData:
    def __init__(self, first_marker, second_marker):
        self.first_marker = first_marker
        self.second_marker = second_marker

#Main
def run(robot):
    start_up(robot)
    #register cubes
    cube1 = robot.world.define_custom_cube(cozmo.objects.CustomObjectTypes.CustomType00, cozmo.objects.CustomObjectMarkers.Diamonds5, 40, 40, 40, True)
    cube2 = robot.world.define_custom_cube(cozmo.objects.CustomObjectTypes.CustomType01, cozmo.objects.CustomObjectMarkers.Circles4, 40, 40, 40, True)
    #print(cube1, cube2)

    #create fsm and start states
    fsm = RobotFSM()
    fsm.start(robot)

    while True:
        first_marker, second_marker = get_visible_marker_info(robot)

        sensor = SensorData(first_marker, second_marker)

        #changes state based on what cozmo is seeing
        fsm.update(robot, sensor)

        time.sleep(0.2)

if __name__ == '__main__':
    cozmo.run_program(run)

'''
References:

define_custom_cube()
https://github.com/anki/cozmo-python-sdk/blob/master/src/cozmo/world.py

custom objects
https://github.com/anki/cozmo-python-sdk/blob/master/src/cozmo/objects.py
'''