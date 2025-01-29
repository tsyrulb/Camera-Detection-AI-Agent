from direct.showbase.ShowBase import ShowBase
from panda3d.core import CollisionSphere, CollisionNode, CollisionHandlerPusher

class MyApp(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)
        
        # Load a room model or build your own geometry for the walls
        self.room = self.loader.loadModel("my_room.egg")
        self.room.reparentTo(self.render)

        # Load a ball
        self.ball = self.loader.loadModel("ball.egg")
        self.ball.setScale(0.2)
        self.ball.reparentTo(self.render)
        self.ball.setPos(0, 20, 1)

        # Add collision sphere
        c_sphere = CollisionSphere(0, 0, 0, 0.5)
        c_node = CollisionNode('ball')
        c_node.addSolid(c_sphere)
        c_nodepath = self.ball.attachNewNode(c_node)

        self.c_handler = CollisionHandlerPusher()
        self.c_handler.addCollider(c_nodepath, self.ball)
        self.taskMgr.add(self.updateBall, "updateBall")

    def updateBall(self, task):
        # Move or apply velocity to self.ball
        # The collisionHandlerPusher will push it if it intersects walls
        return task.cont

app = MyApp()
app.run()
