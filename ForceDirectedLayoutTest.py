from vectors import Vector
import matplotlib.pyplot as plt
import numpy as np


class Graph:

    def __init__(self, data):

        self.nodes = data['nodes']
        self.links = data['links']
        self.linkMatrix = np.zeros((len(self.nodes), len(self.nodes)), dtype=bool)

        self.figure = None
        self.canvasSize = 700
        self.setupCanvas()

        self.iterations = 0
        self.iterationLimit = 100

        self.energyThreshold = 0.01

        self.constant = 0.5  # Ratio of repulsion to attraction
        self.springLength = 100.0
        self.delta = 20.0
        self.deltaDelta = 0.99

        self.buildLinkMatrix()

        return

    def buildLinkMatrix(self):

        for link in self.links:
            self.linkMatrix[link[0], link[1]] = True
            self.linkMatrix[link[1], link[0]] = True

        return

    def converge(self, iterationLimit=50):

        # Update the maximum number of iterations if required
        self.iterationLimit = iterationLimit

        self.iterations = 0
        while (self.iterationLimitReached() is not True) and (self.stabilised() is not True):
            self.update()
            self.draw()
            self.delta = self.delta*self.deltaDelta

    def update(self):
        self.iterations += 1

        # Constant velocity (just a test)
        vertexSpringForces = self.springForce()  #  Attraction
        vertexMagneticForces = self.magneticForce()  # Repulsion

        for index, node in enumerate(self.nodes):
            node.position = node.position + vertexSpringForces[index]*self.delta + vertexMagneticForces[index]*self.delta
            node.velocity = vertexSpringForces[index] + vertexMagneticForces[index]
        return

    def springForce(self):

        forces = [Vector(0, 0)]*len(self.nodes)

        # for n1 in range(1, self.linkMatrix.shape[0]):
        #     for n2 in range(1, self.linkMatrix.shape[1]):
        #
        #         if self.linkMatrix[n1, n2] is True:
        #             node1 = self.nodes[n1]
        #             node2 = self.nodes[n2]
        #
        #             r = node2.position - node1.position
        #             unit = r.unit()
        #             attraction = unit * (r.length() / self.springLength)
        #
        #             forces[node1.id] += attraction
        #             forces[node2.id] -= attraction

        for spring in self.links:
            node1 = self.nodes[spring[0]]
            node2 = self.nodes[spring[1]]

            # This roughly follows Fruchterman and Reingold (1991)
            r = node2.position - node1.position
            unit = r.unit()
            attraction = unit * (r.length() / self.springLength)

            forces[node1.id] += attraction
            forces[node2.id] -= attraction

        return forces

    def magneticForce(self):

        forces = [Vector(0, 0)] * len(self.nodes)
        for node1 in self.nodes:
            for node2 in self.nodes:
                if node1 is not node2:

                    # This roughly follows Fruchterman and Reingold (1991)
                    r = node2.position - node1.position
                    unit = r.unit()
                    repulsion = unit * self.constant * self.springLength**2 / r.lengthSquared()

                    forces[node1.id] -= repulsion

        return forces

    # def gravityForce(self):
    #     forces = [Vector(0, 0)] * len(self.nodes)
    #     for node1 in self.nodes:
    #         r = node1.position
    #         unit = r.unit()
    #         gravity = unit * (r.length() / self.springLength)
    #
    #         forces[node1.id] += gravity
    #
    #     return forces

    def setupCanvas(self):
        self.figure = plt.figure()
        plt.style.use('seaborn-dark')
        plt.grid(True)
        plt.xlim(-self.canvasSize, self.canvasSize)
        plt.ylim(-self.canvasSize, self.canvasSize)
        plt.xlabel('x')
        plt.ylabel('y')
        return

    def draw(self):

        plt.cla()

        for link in self.links:
            plt.plot([self.nodes[link[0]].position.x, self.nodes[link[1]].position.x],
                     [self.nodes[link[0]].position.y, self.nodes[link[1]].position.y],
                     '-b')

        for node in self.nodes:
            plt.plot(node.position.x, node.position.y, 'ro', markersize = 12)

        plt.xlim(-self.canvasSize, self.canvasSize)
        plt.ylim(-self.canvasSize, self.canvasSize)
        plt.grid(True)
        plt.title('Frame {}'.format(self.iterations))

        self.figure.canvas.draw()
        plt.pause(0.0001)

        return

    def cost(self):
        # Calculate a cost for the arrangement of this graph
        pass
        return

    def iterationLimitReached(self):
        # Simple check on iterations to prevent infinite loops, etc.
        if self.iterations >= self.iterationLimit:
            return True
        else:
            return False

    def stabilised(self):
        # Check to see if the nodes have stopped moving
        energy = 0
        for node in self.nodes:
            energy += node.velocity.lengthSquared()

        if self.iterations > 0 and energy < self.energyThreshold:
            return True
        else:
            return False


class Node:

    def __init__(self, id, position):

        self.id = id
        self.links = []
        self.position = position
        self.velocity = Vector(0, 0)
        self.weight = 1

        return


class Link:

    def __init__(self, source, destination, strength):

        self.source = source
        self.destination = destination
        self.strength = strength

        return


# Main code entry point
theNodes = []
for n in range(0, 14):
    theNodes.append(Node(n, Vector(np.random.rand()*1000-500, np.random.rand()*1000-500)))

randomGraph = {'nodes': theNodes,
               'links': [(0, 1),
                         (0, 2),
                         (0, 3),
                         (1, 4),
                         (1, 5),
                         (1, 6),
                         (2, 7),
                         (2, 8),
                         (3, 9),
                         (3, 10),
                         (10, 11),
                         (10, 12),
                         (10, 13)]}

graph = Graph(randomGraph)
graph.converge(iterationLimit=1000)
