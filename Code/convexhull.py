import math
import sys
from tkinter.constants import S

EPSILON = sys.float_info.epsilon

'''
Given two points, p1 and p2,
an x coordinate, x,
and y coordinates y3 and y4,
compute and return the (x,y) coordinates
of the y intercept of the line segment p1->p2
with the line segment (x,y3)->(x,y4)
'''
def yint(p1, p2, x, y3, y4):
	x1, y1 = p1
	x2, y2 = p2
	x3 = x
	x4 = x
	px = ((x1*y2 - y1*x2) * (x3 - x4) - (x1 - x2)*(x3*y4 - y3*x4)) / \
		 float((x1 - x2)*(y3 - y4) - (y1 - y2)*(x3 - x4))
	py = ((x1*y2 - y1*x2)*(y3-y4) - (y1 - y2)*(x3*y4 - y3*x4)) / \
			float((x1 - x2)*(y3 - y4) - (y1 - y2)*(x3-x4))
	return (px, py)

'''
Given three points a,b,c,
computes and returns the area defined by the triangle
a,b,c. 
Note that this area will be negative 
if a,b,c represents a clockwise sequence,
positive if it is counter-clockwise,
and zero if the points are collinear.
'''
def triangleArea(a, b, c):
	return (a[0]*b[1] - a[1]*b[0] + a[1]*c[0] \
                - a[0]*c[1] + b[0]*c[1] - c[0]*b[1]) / 2.0;

'''
Given three points a,b,c,
returns True if and only if 
a,b,c represents a clockwise sequence
(subject to floating-point precision)
'''
def cw(a, b, c):
	return triangleArea(a,b,c) < EPSILON;
'''
Given three points a,b,c,
returns True if and only if 
a,b,c represents a counter-clockwise sequence
(subject to floating-point precision)
'''
def ccw(a, b, c):
	return triangleArea(a,b,c) > EPSILON;

'''
Given three points a,b,c,
returns True if and only if 
a,b,c are collinear
(subject to floating-point precision)
'''
def collinear(a, b, c):
	return abs(triangleArea(a,b,c)) <= EPSILON

'''
Given a list of points,
sort those points in clockwise order
about their centroid.
Note: this function modifies its argument.
'''
def clockwiseSort(points):
	# get mean x coord, mean y coord
	xavg = sum(p[0] for p in points) / len(points)
	yavg = sum(p[1] for p in points) / len(points)
	angle = lambda p:  ((math.atan2(p[1] - yavg, p[0] - xavg) + 2*math.pi) % (2*math.pi))
	points.sort(key = angle)

'''
Replace the implementation of computeHull with a correct computation of the convex hull
using the divide-and-conquer algorithm
'''

def computeHull(points):
	'''
	Sorts points by x coordinates
	Calls on divide and conquer alg to compute hull
	Sorts hull in clockwise order to draw lines
	'''
	points.sort()

	result = computeHullDC(points)
	clockwiseSort(result)

	return result

def computeHullDC(points):
	'''
	Splits the list in two with half going to set A and the other half going to set B
	If the len of either set is greater than three, keep dividing
	For merging:
	- Compute the lower and upper tangent of each set
	- Combine all points in hullinto a singular list to return to the previous call
	- The set of points consist of the upper tangent point of set B, clockwise to the 
	  lower tangent point of set B, then the to lower tangent point of set A, clockwise
	  to the upper tangent point of set A
	- Sort the combine point list and return 
	'''
	split = math.ceil(len(points)/2) 

	A = points[:split]
	B = points[split:]

	if len(A) > 3:
		A = computeHullDC(A)
	if len(B) > 3:
		B = computeHullDC(B)

	lta, ltb = LT(A,B)
	uta, utb = UT(A,B)

	combine = []

	clockwiseSort(A)
	clockwiseSort(B)

	sa = A.index(uta)
	ea = A.index(lta)
	sb = B.index(ltb)
	eb = B.index(utb)

	for i in range(sa, ea + 1):
		combine.append(A[i])
	if (sb > eb):
		for i in range(sb, len(B)):
			combine.append(B[i])
	for i in range(eb + 1):
		combine.append(B[i])

	combine.sort()

	return combine
	
def LT(A,B):
	'''
	Set a as the rightmost point of A and b as the leftmost point of B
	Clockwise Sort each of the lists
	Locate the index of a and b in their respective set 
	While both a and b aren't the lower tangent of their respective set:
	  - increment a so that it is the lower tangenet of set A
	  - increment b so that it is the lower tangenet of set B
	  - check that the tangent formed by points a and b is the lower tangenet of both sets
	Return the points that correspond with the lower tangent
	'''
	a = A[-1]
	b = B[0]

	tempA = []
	tempB = []
	tempA.extend(A)
	tempB.extend(B)

	clockwiseSort(tempA)
	clockwiseSort(tempB)

	indexa = tempA.index(a)
	indexb = tempB.index(b)

	while(not LTChecker(indexa, tempA, a, b) or not LTChecker(indexb, tempB, a, b)):
		while(not LTChecker(indexa, tempA, a, b)):
			a = tempA[(indexa - 1) % len(A)]
			indexa = tempA.index(a)
		while(not LTChecker(indexb, tempB, a, b)):
			b = tempB[(indexb + 1) % len(B)]
			indexb = tempB.index(b)

	return (a,b)

def LTChecker(p, points, a, b):
	'''
	Check that point p is the lower tangent of the set points
	be and af correspond with the before and after point of p in points
	Compute the current tangent based off points a and b
	If the tangent y value of points be and af are lower than the actual y value
	of points be and af, than this is the lower tangenet of set points, otherwise no
	'''
	be = (p-1) % len(points)
	af = (p+1) % len(points)
	
	try:
		inter = yint(a,b,0,1,2)
	except:
		return True

	inter = yint(a,b,0,1,2)
	slope = (b[1]-a[1]) / (b[0]-a[0])
	bey = slope*points[be][0] + inter[1]
	afy = slope*points[af][0] + inter[1]

	if (bey <= points[be][1] and afy <= points[af][1]):
		return True
	else:
		return False

def UT(A,B):
	'''
	Set a as the rightmost point of A and b as the leftmost point of B
	Clockwise Sort each of the lists
	Locate the index of a and b in their respective set 
	While both a and b aren't the upper tangent of their respective set:
	  - increment a so that it is the upper tangenet of set A
	  - increment b so that it is the upper tangenet of set B
	  - check that the tangent formed by points a and b is the upper tangenet of both sets
	Return the points that correspond with the upper tangent
	'''
	a = A[-1]
	b = B[0]
	
	tempA = []
	tempB = []
	tempA.extend(A)
	tempB.extend(B)

	clockwiseSort(tempA)
	clockwiseSort(tempB)

	indexa = tempA.index(a)
	indexb = tempB.index(b)

	while(not UTChecker(indexa, tempA, a, b) or not UTChecker(indexb, tempB, a, b)):
		while(not UTChecker(indexa, tempA, a, b)):
			a = tempA[(indexa + 1) % len(A)]
			indexa = tempA.index(a)
		while(not UTChecker(indexb, tempB, a, b)):
			b = tempB[(indexb - 1) % len(B)]
			indexb = tempB.index(b)

	return (a,b)

def UTChecker(p, points, a, b):
	'''
	Check that point p is the upper tangent of the set points
	be and af correspond with the before and after point of p in points
	Compute the current tangent based off points a and b
	If the tangent y value of points be and af are higher than the actual y value
	of points be and af, than this is the upper tangenet of set points, otherwise no
	'''
	be = (p-1) % len(points)
	af = (p+1) % len(points)

	try:
		inter = yint(a,b,0,1,2)
	except:
		return True

	inter = yint(a,b,0,1,2)
	slope = (b[1]-a[1]) / (b[0]-a[0])
	bey = slope*points[be][0] + inter[1]
	afy = slope*points[af][0] + inter[1]

	if (bey >= points[be][1] and afy >= points[af][1]):
		return True
	else:
		return False

def JarvisMarch(points):
	'''
	Naive way of implementing computeHull
	Initialize p as leftmost point
	Do following while we do not come back to the first (or leftmost) point:
    - The next point q is the point such that the triplet (p, q, r) is counterclockwise for any other point r.
    - next[p] = q (Store q as next of p in the output convex hull).
    - p = q (Set p as q for next iteration).
	O(nh) with h being the number of points
	Taken from https://iq.opengenus.org/gift-wrap-jarvis-march-algorithm-convex-hull/
	'''
	if len(points) < 3:
		return points

	points.sort()
	p = 0

	hull = []

	hull.append(points[p])
	q = (p+1) % len(points)
	for i in range(len(points)):
		if (orientation(points[p], points[i], points[q]) == 2):
			q = i
	p = q

	while (p != 0):
		hull.append(points[p])
		q = (p+1) % len(points)
		for i in range(len(points)):
			if (orientation(points[p], points[i], points[q]) == 2):
				q = i
		p = q
	
	return hull

def orientation(p, q, r):
	val = (q[1] - p[1]) * (r[0] - q[0]) - (q[0] - p[0]) * (r[1] - q[1])
	ans = -1
	if (val == 0):
		ans = 0
	if (val > 0):
		ans = 1
	if (val < 0):
		ans = 2
	return ans