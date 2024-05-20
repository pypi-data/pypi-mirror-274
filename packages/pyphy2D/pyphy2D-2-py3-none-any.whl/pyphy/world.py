from pyphy.pygame_integration import PyphyPygame
from pyphy.collision_manifold import Manifold
from pyphy.transform import Transform
from pyphy.vector2 import Vector2
from pyphy.pyphymath import math
from pyphy.body import Body
import collisions_c
import resolveCollisions_c


class World:
    MinIterations = 1
    MaxIterations = 64

    def __init__(self, window, gravity: tuple, iterations: int=1) -> None:
        self.window = window
        self.window_height = PyphyPygame.GetWindowHeight(window)
        self.window_width = PyphyPygame.GetWindowWidth(window)

        self.gravity = Vector2.from_tuple(gravity) * 100
        self.iterations = math.clamp(iterations, self.MinIterations, self.MaxIterations)

        self.bodies: list[Body] = []
        self.contactpairs: list[tuple[int, int]] = []
        
        self.doFriction = True
        self.groundIsLava = True
        self.drawCircleAxis = True

    def ToggleGroundIsLava(self) -> None:
        self.groundIsLava = not self.groundIsLava

    def Render(self) -> None:
        for body in self.bodies:
            if body.shape == Body.CIRCLE:
                self.__drawCircleBody__(body)
            else:
                self.__drawPolygonBody__(body)

    def CreateBounds(self, width=None, height=None) -> None:
        if width is None or height is None:
            width, height = PyphyPygame.GetWindowSize(self.window)

        walls = [
            # Top boundary
            Body.CreateBoxBody(width, 1, Vector2.from_tuple((width / 2, -0.5)), -1, 1, True),
            # Bottom boundary
            Body.CreateBoxBody(width, 1, Vector2.from_tuple((width / 2, height + 0.5)), -1, 1, True),
            # Left boundary
            Body.CreateBoxBody(1, height, Vector2.from_tuple((-2, height / 2)), -1, 1, True),
            # Right boundary
            Body.CreateBoxBody(1, height, Vector2.from_tuple((width + 0.5, height / 2)), -1, 1, True)
        ]
        
        for wall in walls:
            self.AddBody(wall)

    def __drawCircleBody__(self, body: Body) -> None:
        if body.texture is None:
            PyphyPygame.DrawCircle(self.window, body.color, body.position, body.radius)
            
            if not self.drawCircleAxis:
                return
            
            transformer = Transform(body.position, body.angle)
            va = Vector2.transform(Vector2.zero(), transformer)
            vb = Vector2.transform(Vector2(body.radius, 0), transformer)
            PyphyPygame.DrawLine(self.window, 'black', va, vb, 2)
        else:
            PyphyPygame.Blit(self.window, body.texture, body.position - body.radius)

    def __drawPolygonBody__(self, body: Body) -> None:
        if body.texture is None:
            PyphyPygame.DrawPolygon(self.window, body.color, body.getTransformedVertices())
        else:
            texture = PyphyPygame.RotateImage(body.texture, math.ToDegrees(-body.angle))
            PyphyPygame.Blit(self.window, texture, (body.position.x - body.width/2, body.position.y - body.height/2))

    def GetBody(self, index: int) -> Body | bool:
        if index < 0 or index >= len(self.bodies):
            return False
        return self.bodies[int(index)]

    def AddBody(self, body: Body) -> None:
        self.bodies.append(body)

    def RemoveBody(self, body: Body) -> bool:
        if body not in self.bodies:
            return False
        self.bodies.remove(body)
        return True
    
    def __lavaGround__(self) -> None:
        if not self.groundIsLava:
            return
        
        for body in self.bodies:
            aabb = body.getAABB()
            if aabb.minVector.y > self.window_height:
                self.RemoveBody(body)

    def step(self, dt) -> None:
        dt /= self.iterations

        for _ in range(self.iterations):
            [body.step(self.gravity, dt) for body in self.bodies]

            # Check Collisions
            self.contactpairs.clear()

            self.__broadPhase__()
            self.__narrowPhase__()

        self.__lavaGround__()

    def __broadPhase__(self) -> None:
        for i in range(len(self.bodies)):
            bodyA = self.bodies[i]
            bodyA_aabb = bodyA.getAABB()

            for j in range(i+1, len(self.bodies)):
                bodyB = self.bodies[j]
                bodyB_aabb = bodyB.getAABB()

                if bodyA.isStatic and bodyB.isStatic:
                    continue

                if not collisions_c.IntersectAABB(bodyA_aabb, bodyB_aabb):
                    continue

                self.contactpairs.append((i, j))

    def __narrowPhase__(self) -> None:
        for i, j in self.contactpairs:
            bodyA, bodyB = self.bodies[i], self.bodies[j]
            
            collision, normal, depth = collisions_c.Collide(bodyA, bodyB, Vector2.zero())
            if collision:
                if bodyA.isStatic:
                    bodyB.Move(normal * depth)
                elif bodyB.isStatic:
                    bodyA.Move(-normal * depth)
                else:
                    bodyA.Move(-normal * depth/2)
                    bodyB.Move(normal * depth/2)

                contact1, contact2, contactCount = collisions_c.FindContactPoints(bodyA, bodyB, Vector2.zero())

                contact = Manifold(bodyA, bodyB, normal, depth, contact1, contact2, contactCount)
                resolveCollisions_c.callResolveCollisions(contact, Vector2.zero(), self.doFriction)