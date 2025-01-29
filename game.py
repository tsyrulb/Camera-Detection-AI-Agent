# game.py
#
# Our Panda3D "game" logic. We set up:
# - A ShowBase class to create a window
# - A "room" bounding box in 3D
# - A ball that bounces around
# - A rocket NodePath that we move in 3D
#
# We do "manual" bounding logic for the ball, reflecting velocity.

from direct.showbase.ShowBase import ShowBase
from direct.task import Task
import time

from panda3d.core import WindowProperties, Vec3, NodePath, CollisionSphere, CollisionNode

from config import (
    ROOM_MIN_X, ROOM_MAX_X,
    ROOM_MIN_Y, ROOM_MAX_Y,
    ROOM_MIN_Z, ROOM_MAX_Z,
    BALL_START_X, BALL_START_Y, BALL_START_Z,
    BALL_VX, BALL_VY, BALL_VZ,
    ROCKET_START_X, ROCKET_START_Y, ROCKET_START_Z,
    FPS
)

class MyGame(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)

        # Hide mouse cursor (optional)
        props = WindowProperties()
        props.setCursorHidden(False)
        self.win.requestProperties(props)

        # Some camera setup
        self.disableMouse()  # We'll manually position the camera
        self.camera.setPos(0, -700, 300)
        self.camera.lookAt(0, 100, 50)

        # Set background color
        self.setBackgroundColor(0, 0, 0)

        # 3D models for ball and rocket
        # Use "self.loader" (not just "loader") 
        self.ball = self.loader.loadModel("models/smiley")
        self.ball.setScale(5)  # bigger
        self.ball.reparentTo(self.render)

        self.rocket = self.loader.loadModel("models/frowney")
        self.rocket.setScale(3)
        self.rocket.reparentTo(self.render)

        # Starting positions
        self.ball_x = BALL_START_X
        self.ball_y = BALL_START_Y
        self.ball_z = BALL_START_Z

        self.ball_vx = BALL_VX
        self.ball_vy = BALL_VY
        self.ball_vz = BALL_VZ

        self.rocket_x = ROCKET_START_X
        self.rocket_y = ROCKET_START_Y
        self.rocket_z = ROCKET_START_Z

        # Store last update time for delta
        self.last_time = time.time()

        # Add a task for updating each frame
        self.taskMgr.add(self.updateTask, "updateTask")

    def updateTask(self, task):
        """
        Runs every frame. We'll move the ball, do bounding logic,
        position the rocket, etc.
        """
        now = time.time()
        dt = now - self.last_time
        self.last_time = now

        # Move the ball
        self.ball_x += self.ball_vx * dt
        self.ball_y += self.ball_vy * dt
        self.ball_z += self.ball_vz * dt

        # Check collisions with bounding box
        # Floor
        if self.ball_y < ROOM_MIN_Y:
            self.ball_y = ROOM_MIN_Y
            self.ball_vy = -self.ball_vy
        # Ceiling
        if self.ball_y > ROOM_MAX_Y:
            self.ball_y = ROOM_MAX_Y
            self.ball_vy = -self.ball_vy
        # Left/Right
        if self.ball_x < ROOM_MIN_X:
            self.ball_x = ROOM_MIN_X
            self.ball_vx = -self.ball_vx
        if self.ball_x > ROOM_MAX_X:
            self.ball_x = ROOM_MAX_X
            self.ball_vx = -self.ball_vx
        # Front/Back
        if self.ball_z < ROOM_MIN_Z:
            self.ball_z = ROOM_MIN_Z
            self.ball_vz = -self.ball_vz
        if self.ball_z > ROOM_MAX_Z:
            self.ball_z = ROOM_MAX_Z
            self.ball_vz = -self.ball_vz

        # Position the ball NodePath
        # Note: in Panda3D, default axis is X=left/right, Y=forward/back, Z=up/down
        # We'll do:  self.ball.setPos( x => X,  y => Z,  z => Y)
        self.ball.setPos(self.ball_x, self.ball_z, self.ball_y)

        # Position the rocket NodePath similarly
        self.rocket.setPos(self.rocket_x, self.rocket_z, self.rocket_y)

        return Task.cont

    def setRocketPosition(self, x, y, z):
        """
        Called externally to update the rocket's (x,y,z) from detection.
        """
        self.rocket_x = x
        self.rocket_y = y
        self.rocket_z = z
