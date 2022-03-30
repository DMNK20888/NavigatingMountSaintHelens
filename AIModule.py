from copy import deepcopy
from queue import PriorityQueue
from Point import Point
import math

'''AIModule Interface
createPath(map map_) -> list<points>: Adds points to a path'''
class AIModule:

	def createPath(self, map_):
		pass



#TRY 2
def expHeuristic(self, map_, curX, curY):
	endHeight = map_.getTile(map_.getEndPoint().x, map_.getEndPoint().y)
	curHeight = map_.getTile(curX, curY)

	distanceX = abs(curX - map_.getEndPoint().x)
	distanceY = abs(curY - map_.getEndPoint().y)
	cheb = max(distanceX, distanceY)

	if(curHeight < endHeight):
		cost = 2*(endHeight-curHeight) + max(0, cheb-(endHeight-curHeight))
		return cost

	if(curHeight > endHeight):
		slope = (endHeight-curHeight)/cheb
		return (2**slope)*cheb

	if(curHeight == endHeight):
		return cheb


def divHeuristic(self, map_, curX, curY):
	distanceX = abs(curX - map_.getEndPoint().x)
	distanceY = abs(curY - map_.getEndPoint().y)
	startHeight = map_.getTile(map_.getStartPoint().x, map_.getStartPoint().y)
	curHeight = map_.getTile(curX, curY)
	endHeight = map_.getTile(map_.getEndPoint().x, map_.getEndPoint().y)
	change = curHeight - endHeight
	#find the chebyshev distance for the below heuristic
	cheb = max(distanceX, distanceY)
	#Return the heuristic cost d/2
	return max(cheb/2, 0)


def mshHeuristic(self, map_, curX, curY):
	endHeight = map_.getTile(map_.getEndPoint().x, map_.getEndPoint().y)
	curHeight = map_.getTile(curX, curY)

	distanceX = abs(curX - map_.getEndPoint().x)
	distanceY = abs(curY - map_.getEndPoint().y)
	cheb = max(distanceX, distanceY)

	if(curHeight < endHeight):
		cost = 2*(endHeight-curHeight) + max(0, cheb-(endHeight-curHeight))
		#return 1.034*cost
		return 1.034*cost

	if(curHeight > endHeight):
		slope = (endHeight-curHeight)/cheb
		return 1.034*(2**slope)*cheb

	if(curHeight == endHeight):
		return 1.034*cheb #was 1.033 #returns a weighted chebyshev distance, providing more emphasis to the heuristic


'''
A sample AI that takes a very suboptimal path.
This is a sample AI that moves as far horizontally as necessary to reach
the target, then as far vertically as necessary to reach the target.
It is intended primarily as a demonstration of the various pieces of the
program.
'''
class StupidAI(AIModule):

	def createPath(self, map_):
		path = []
		explored = []
		# Get starting point
		path.append(map_.start)
		current_point = deepcopy(map_.start)

		# Keep moving horizontally until we match the target
		while(current_point.x != map_.goal.x):
			# If we are left of goal, move right
			if current_point.x < map_.goal.x:
				current_point.x += 1
			# If we are right of goal, move left
			else:
				current_point.x -= 1
			path.append(deepcopy(current_point))

		# Keep moving vertically until we match the target
		while(current_point.y != map_.goal.y):
			# If we are left of goal, move right
			if current_point.y < map_.goal.y:
				current_point.y += 1
			# If we are right of goal, move left
			else:
				current_point.y -= 1
			path.append(deepcopy(current_point))

		# We're done!
		return path

################################################################################################################################################

#class which implements the Dijkstra path finding algorithm
class Dijkstras(AIModule):

	def createPath(self, map_):
		q = PriorityQueue()
		cost = {}
		prev = {}
		explored = {}
		for i in range(map_.width):
			for j in range(map_.length):
				cost[str(i)+','+str(j)] = math.inf
				prev[str(i)+','+str(j)] = None
				explored[str(i)+','+str(j)] = False
		current_point = deepcopy(map_.start)
		current_point.comparator = 0
		cost[str(current_point.x)+','+str(current_point.y)] = 0
		q.put(current_point)
		while q.qsize() > 0:
			# Get new point from PQ
			v = q.get()
			if explored[str(v.x)+','+str(v.y)]:
				continue
			explored[str(v.x)+','+str(v.y)] = True
			# Check if popping off goal
			if v.x == map_.getEndPoint().x and v.y == map_.getEndPoint().y:
				break
			# Evaluate neighbors
			neighbors = map_.getNeighbors(v)
			for neighbor in neighbors:
				alt = map_.getCost(v, neighbor) + cost[str(v.x)+','+str(v.y)] # + cost of h(n)
				if alt < cost[str(neighbor.x)+','+str(neighbor.y)]: # + cost of h(n)
					cost[str(neighbor.x)+','+str(neighbor.y)] = alt
					neighbor.comparator = alt
					prev[str(neighbor.x)+','+str(neighbor.y)] = v
				q.put(neighbor)

		path = []
		while not(v.x == map_.getStartPoint().x and v.y == map_.getStartPoint().y):
			path.append(v)
			v = prev[str(v.x)+','+str(v.y)]
		path.append(map_.getStartPoint())
		path.reverse()
		return path

################################################################################################################################################

#class which implements the A* path finding algorithm with the exponential cost function
class AStarExp(AIModule):

	def createPath(self, map_):

		q = PriorityQueue()
		cost = {}
		prev = {}
		explored = {}
		#sets all nodes to unexplored and giving an infinite cost
		for i in range(map_.width):
			for j in range(map_.length):
				cost[str(i)+','+str(j)] = math.inf
				prev[str(i)+','+str(j)] = None
				explored[str(i)+','+str(j)] = False
		current_point = deepcopy(map_.start)
		current_point.comparator = 0
		#cost[str(current_point.x)+','+str(current_point.y)] = 0 
		cost[str(current_point.x)+','+str(current_point.y)] = expHeuristic(self, map_, current_point.x, current_point.y)
		q.put(current_point)
		while q.qsize() > 0:
			# Get new point from PQ
			v = q.get()
			if explored[str(v.x)+','+str(v.y)]:
				continue
			explored[str(v.x)+','+str(v.y)] = True
			# Check if popping off goal
			if v.x == map_.getEndPoint().x and v.y == map_.getEndPoint().y:
				break
			# Evaluate neighbors
			neighbors = map_.getNeighbors(v)
			for neighbor in neighbors:
				alt = map_.getCost(v, neighbor) + cost[str(v.x)+','+str(v.y)]
				if alt < cost[str(neighbor.x)+','+str(neighbor.y)]:
					cost[str(neighbor.x)+','+str(neighbor.y)] = alt #+ expHeuristic(self, map_, v.x, v.y)
					#neighbor.comparator = alt + expHeuristic(self, map_, v.x, v.y)
					neighbor.comparator = alt + expHeuristic(self, map_, neighbor.x, neighbor.y)
					prev[str(neighbor.x)+','+str(neighbor.y)] = v
				q.put(neighbor)
		path = []
		while not(v.x == map_.getStartPoint().x and v.y == map_.getStartPoint().y):
			path.append(v)
			v = prev[str(v.x)+','+str(v.y)]
		path.append(map_.getStartPoint())
		path.reverse()
		return path

################################################################################################################################################

#class which implements the A* path finding algorithm which uses the division cost function
class AStarDiv(AIModule):

	def createPath(self, map_):
		
		q = PriorityQueue()
		cost = {}
		prev = {}
		explored = {}
		#sets all nodes to unexplored and giving an infinite cost
		for i in range(map_.width):
			for j in range(map_.length):
				cost[str(i)+','+str(j)] = math.inf
				prev[str(i)+','+str(j)] = None
				explored[str(i)+','+str(j)] = False
		current_point = deepcopy(map_.start)
		current_point.comparator = 0
		#cost[str(current_point.x)+','+str(current_point.y)] = 0 # + h(n)
		cost[str(current_point.x)+','+str(current_point.y)] = divHeuristic(self, map_, current_point.x, current_point.y)
		q.put(current_point)
		while q.qsize() > 0:
			# Get new point from PQ
			v = q.get()
			if explored[str(v.x)+','+str(v.y)]:
				continue
			explored[str(v.x)+','+str(v.y)] = True
			# Check if popping off goal
			if v.x == map_.getEndPoint().x and v.y == map_.getEndPoint().y:
				break
			# Evaluate neighbors
			neighbors = map_.getNeighbors(v)
			for neighbor in neighbors:
				alt = map_.getCost(v, neighbor) + cost[str(v.x)+','+str(v.y)]
				if alt < cost[str(neighbor.x)+','+str(neighbor.y)]:
					cost[str(neighbor.x)+','+str(neighbor.y)] = alt #+ divHeuristic(self, map_, v.x, v.y)
					neighbor.comparator = alt + divHeuristic(self, map_, v.x, v.y)
					prev[str(neighbor.x)+','+str(neighbor.y)] = v
				q.put(neighbor)
		path = []
		while not(v.x == map_.getStartPoint().x and v.y == map_.getStartPoint().y):
			path.append(v)
			v = prev[str(v.x)+','+str(v.y)]
		path.append(map_.getStartPoint())
		path.reverse()
		return path

#class which implements the Weighted A* path finding algorithm usign the exponential 
class AStarMSH(AIModule):

	def createPath(self, map_):
		q = PriorityQueue()
		cost = {}
		prev = {}
		explored = {}
		#sets all nodes to unexplored and giving an infinite cost
		for i in range(map_.width):
			for j in range(map_.length):
				cost[str(i)+','+str(j)] = math.inf
				prev[str(i)+','+str(j)] = None
				explored[str(i)+','+str(j)] = False
		current_point = deepcopy(map_.start)
		current_point.comparator = 0
		cost[str(current_point.x)+','+str(current_point.y)] = 0 
		q.put(current_point)
		while q.qsize() > 0:
			# Get new point from PQ
			v = q.get()
			if explored[str(v.x)+','+str(v.y)]:
				continue
			explored[str(v.x)+','+str(v.y)] = True
			# Check if popping off goal
			if v.x == map_.getEndPoint().x and v.y == map_.getEndPoint().y:
				break
			# Evaluate neighbors
			neighbors = map_.getNeighbors(v)
			for neighbor in neighbors:
				alt = map_.getCost(v, neighbor) + cost[str(v.x)+','+str(v.y)]
				if alt < cost[str(neighbor.x)+','+str(neighbor.y)]:
					cost[str(neighbor.x)+','+str(neighbor.y)] = alt
					neighbor.comparator = alt + mshHeuristic(self, map_, neighbor.x, neighbor.y)
					prev[str(neighbor.x)+','+str(neighbor.y)] = v
				q.put(neighbor)
		path = []
		while not(v.x == map_.getStartPoint().x and v.y == map_.getStartPoint().y):
			path.append(v)
			v = prev[str(v.x)+','+str(v.y)]
		path.append(map_.getStartPoint())
		path.reverse()
		return path












































