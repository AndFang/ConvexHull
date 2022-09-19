#!/usr/bin/env python
# if using python 3, swap the next two lines
from tkinter import *
# from Tkinter import *
import copy
import os
from convexhull import computeHull, JarvisMarch

import time, random


def hello(event):
    print("Single Click, Button-l") 

def addPoint(event):
	drawPoint(w, event.x, event.y)
	points.append((event.x,event.y))

def drawPoint(canvas,x,y):
	# r = 4
	# id = canvas.create_oval(x-r,y-r,x+r,y+r)
	id = canvas.create_image((x,y),image=ram,state=NORMAL)
	return id

def showPoints(event):
	print(points)

def drawHull():
	'''
	start and end used for timing algorithm
	'''
	start = time.time()
	hull = copy.copy(computeHull(points)) # can replace 'computeHull' with 'JarvisMarch'
	# print(time.time() - start)
	hull.append(hull[0])
	for i in range(0,len(hull)-1):
		x1 = hull[i][0]
		y1 = hull[i][1]
		x2 = hull[i+1][0]
		y2 = hull[i+1][1]
		w.create_line(x1, y1, x2, y2, width=3)


master = Tk()
points = []

'''
Random points
Tested for [20000, 40000, 60000, 80000, 100000] points
with naive and Divide and Conquer algorithm

for i in range(100000):
	x = random.randint(0,1000)
	y = random.randint(0,800)
	points.append((x,y))
'''

submit_button = Button(master, text="Draw Hull", command=drawHull)
submit_button.pack()
quit_button = Button(master, text="Quit", command=master.quit)
quit_button.pack()

canvas_width = 1000
canvas_height = 800
w = Canvas(master, 
           width=canvas_width,
           height=canvas_height)
ram = PhotoImage(file= os.getcwd() + "\Images\oldhusky.gif")
w.pack()
w.bind('<Button-1>', addPoint)

w.mainloop()