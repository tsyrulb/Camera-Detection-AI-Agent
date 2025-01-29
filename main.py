# main.py
#
# The main entry point: 
# 1. Opens the camera 
# 2. Creates MyGame
# 3. On each frame, we do detection => rocket_x,y,z => MyGame
# 4. Runs the Panda3D main loop

import sys
import cv2
import time
from direct.task import Task
from config import FPS
from detection import detect_hand_3D
from game import MyGame

def main():
    # 1) Open camera
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Could not open camera.")
        sys.exit(1)

    # 2) Create our Panda3D game
    app = MyGame()

    # We'll store rocket_x,y,z in a local variable, updated each detection
    rocket_xyz = (app.rocket_x, app.rocket_y, app.rocket_z)

    # 3) Create a "task" that calls detection each frame 
    #    and updates MyGame's rocket position
    def detectionTask(task):
        nonlocal rocket_xyz

        rocket_xyz = detect_hand_3D(cap, rocket_xyz)
        # detection_hand_3D => returns (rx, ry, rz)
        if isinstance(rocket_xyz, tuple):
            app.setRocketPosition(*rocket_xyz)
        return Task.cont

    app.taskMgr.add(detectionTask, "detectionTask")
    app.run()
    cap.release()

if __name__ == "__main__":
    main()
