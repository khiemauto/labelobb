#!/usr/bin/python
# -*- coding: utf-8 -*-

import math
import numpy as np

# from turtledemo import paint
# from audioop import minmax


from PyQt5.QtGui import *
from PyQt5.QtCore import *


from libs.lib import distance
import sys

DEFAULT_LINE_COLOR = QColor(0, 255, 0, 0)
DEFAULT_FILL_COLOR = QColor(255, 0, 0, 0)
DEFAULT_SELECT_LINE_COLOR = QColor(255, 255, 255)
DEFAULT_SELECT_FILL_COLOR = QColor(0, 128, 255, 0)
DEFAULT_VERTEX_FILL_COLOR = QColor(0, 255, 0, 0)
DEFAULT_HVERTEX_FILL_COLOR = QColor(255, 0, 0)
DEFAULT_ORIGIN_FILL_COLOR = QColor(0, 0, 0)
MIN_Y_LABEL = 10


class Shape(object):
    P_SQUARE, P_ROUND = range(2)

    MOVE_VERTEX, NEAR_VERTEX = range(2)

    # The following class variables influence the drawing
    # of _all_ shape objects.
    line_color = DEFAULT_LINE_COLOR
    fill_color = DEFAULT_FILL_COLOR
    select_line_color = DEFAULT_SELECT_LINE_COLOR
    select_fill_color = DEFAULT_SELECT_FILL_COLOR
    vertex_fill_color = DEFAULT_VERTEX_FILL_COLOR
    hvertex_fill_color = DEFAULT_HVERTEX_FILL_COLOR
    origin_fill_color = DEFAULT_ORIGIN_FILL_COLOR
    
    point_type = P_ROUND
    point_size = 8
    scale = 1.0

    def __init__(self, label=None, line_color=None, difficult=False, paintLabel=False):
        self.label = label
        self.points = []
        self.origin = [0,0]
        self.angle = 0
        self.height = 0
        self.width = 0
        self.fill = False
        self.selected = False
        self.difficult = difficult
        self.paintLabel = paintLabel

        self._highlightIndex = None
        self._highlightMode = self.NEAR_VERTEX
        self._highlightSettings = {
            self.NEAR_VERTEX: (4, self.P_ROUND),
            self.MOVE_VERTEX: (1.5, self.P_SQUARE),
        }

        self._closed = False

        if line_color is not None:
            # Override the class line_color attribute
            # with an object attribute. Currently this
            # is used for drawing the pending line a different color.
            self.line_color = line_color

    def close(self):
        self._closed = True

    def reachMaxPoints(self):
        if len(self.points) >= 4:
            return True
        return False

    def addPoint(self, point):
        if not self.reachMaxPoints():
            self.points.append(point)

    def popPoint(self):
        if self.points:
            return self.points.pop()
        return None

    def isClosed(self):
        return self._closed

    def setOpen(self):
        self._closed = False

    def paint(self, painter):
        if self.points:
            color = self.select_line_color if self.selected else self.line_color
            pen = QPen(color)
            # Try using integer sizes for smoother drawing(?)
            pen.setWidth(max(1, int(round(2.0 / self.scale))))
            painter.setPen(pen)

            line_path = QPainterPath()
            vrtx_path = QPainterPath()
            originPoint_path = QPainterPath()

            line_path.moveTo(self.points[0])
            # Uncommenting the following line will draw 2 paths
            # for the 1st vertex, and make it non-filled, which
            # may be desirable.
            #self.drawVertex(vrtx_path, 0)

            for i, p in enumerate(self.points):
                line_path.lineTo(p)
                self.drawVertex(vrtx_path, i)
            self.drawOrigin(originPoint_path) # Draw object origin (centre)
            
            if self.isClosed():
                line_path.lineTo(self.points[0])

            painter.drawPath(line_path)
            painter.drawPath(vrtx_path)
            painter.drawPath(originPoint_path)
            painter.fillPath(vrtx_path, self.vertex_fill_color)
            painter.fillPath(originPoint_path, self.origin_fill_color)

            # Print debug info
            min_x = sys.maxsize
            min_y = sys.maxsize
            for point in self.points:
                min_x = min(min_x, point.x())
                min_y = min(min_y, point.y())
            if min_x != sys.maxsize and min_y != sys.maxsize:
                font = QFont()
                font.setPointSize(3)
                font.setBold(True)
                painter.setFont(font)
                if(self.label == None):
                    self.label = ""
                if(min_y < MIN_Y_LABEL):
                    min_y += MIN_Y_LABEL
                painter.drawText(int(min_x), int(min_y), "H={0:.1f} W={1:.1f} A={2:.1f}".format(self.height, self.width, -self.angle))

            # Draw text at the top-left
            if self.paintLabel:
                min_x = sys.maxsize
                min_y = sys.maxsize
                for point in self.points:
                    min_x = min(min_x, point.x())
                    min_y = min(min_y, point.y())
                if min_x != sys.maxsize and min_y != sys.maxsize:
                    font = QFont()
                    font.setPointSize(8)
                    font.setBold(True)
                    painter.setFont(font)
                    if(self.label == None):
                        self.label = ""
                    if(min_y < MIN_Y_LABEL):
                        min_y += MIN_Y_LABEL
                    painter.drawText(int(min_x), int(min_y), self.label)

            if self.fill:
                color = self.select_fill_color if self.selected else self.fill_color
                painter.fillPath(line_path, color)

    def drawVertex(self, path, i):
        d = self.point_size / self.scale
        shape = self.point_type
        point = self.points[i]
        if i == self._highlightIndex:
            size, shape = self._highlightSettings[self._highlightMode]
            d *= size
        if self._highlightIndex is not None:
            self.vertex_fill_color = self.hvertex_fill_color
        else:
            self.vertex_fill_color = Shape.vertex_fill_color
        if shape == self.P_SQUARE:
            path.addRect(point.x() - d / 2, point.y() - d / 2, d, d)
        elif shape == self.P_ROUND:
            path.addEllipse(point, d / 2.0, d / 2.0)
        else:
            assert False, "unsupported vertex shape"
            
    def drawOrigin(self, path):
        d = self.point_size / self.scale
        path.addEllipse(QPoint(int(self.origin[0]), int(self.origin[1])), d / 2.0, d / 2.0)

    def nearestVertex(self, point, epsilon):
        for i, p in enumerate(self.points):
            if distance(p - point) <= epsilon:
                return i
        return None

    def containsPoint(self, point):
        return self.makePath().contains(point)

    def makePath(self):
        path = QPainterPath(self.points[0])
        for p in self.points[1:]:
            path.lineTo(p)
        return path

    def boundingRect(self):
        return self.makePath().boundingRect()

    def moveBy(self, offset):
        self.points = [p + offset for p in self.points]
        self.updateOBBInfo()

    def moveVertexBy(self, i, offset):
        self.points[i] = self.points[i] + offset
        self.updateOBBInfo()

    def rotate_point(self, x, y, cx, cy, alpha):
        x_new = cx + math.cos(alpha) * (x - cx) - math.sin(alpha) * (y - cy)
        y_new = cy + math.sin(alpha) * (x - cx) + math.cos(alpha) * (y - cy)
        
        return x_new, y_new
        
    def rotateBy(self, angle, pixmap_width, pixmap_height): # Clock-wise
        new_xs = []
        new_ys = []
        for i in range(4):
            point_x = self.points[i].x()
            point_y = self.points[i].y()
            new_x, new_y = self.rotate_point(point_x, point_y, self.origin[0], self.origin[1], angle)
            new_xs.append(new_x)
            new_ys.append(new_y)
        if all( (0 <= new_xs[i] <= pixmap_width and 0 <= new_ys[i] <= pixmap_height) for i in range(4) ):
            for j in range(4):
                self.points[j].setX(new_xs[j])
                self.points[j].setY(new_ys[j])
            self.updateOBBInfo()
        
    def updateOBBInfo(self):
        if (self.reachMaxPoints()):
            # Update Origin (Centre info)
            self.origin[0] = sum([self.points[i].x() for i in range(4)]) / 4.0
            self.origin[1] = sum([self.points[i].y() for i in range(4)]) / 4.0

            self.angle = math.degrees( math.atan2( self.points[1].y()-self.points[0].y(),
                                                   self.points[1].x()-self.points[0].x() ) )
            
            self.width = math.sqrt( ((self.points[1].x()-self.points[0].x())**2) + 
                              ((self.points[1].y()-self.points[0].y())**2) )
            self.height = math.sqrt( ((self.points[2].x()-self.points[1].x())**2) + 
                              ((self.points[2].y()-self.points[1].y())**2) )
    

    def updatePointsFromOBBInfo(self, canvas_width, canvas_height):

        x_1, y_1 = self.rotate_point(self.origin[0]-self.width/2, self.origin[1]-self.height/2, self.origin[0], self.origin[1], math.radians(self.angle))
        x_2, y_2 = self.rotate_point(self.origin[0]+self.width/2, self.origin[1]-self.height/2, self.origin[0], self.origin[1], math.radians(self.angle))
        x_3, y_3 = self.rotate_point(self.origin[0]+self.width/2, self.origin[1]+self.height/2, self.origin[0], self.origin[1], math.radians(self.angle))
        x_4, y_4 = self.rotate_point(self.origin[0]-self.width/2, self.origin[1]+self.height/2, self.origin[0], self.origin[1], math.radians(self.angle))

        p = [x_1, y_1, x_2, y_2, x_3, y_3, x_4, y_4]
           
        # Make sure that all vertices are inside the canvas area
        if (all([ (p[i]>0 and p[i]<canvas_width) for i in range(0,8,2) ]) and all([ (p[i]>0 and p[i]<canvas_height) for i in range(1,8,2) ])):
            self.addPoint(QPointF(p[0], p[1]))
            self.addPoint(QPointF(p[2], p[3]))
            self.addPoint(QPointF(p[4], p[5]))
            self.addPoint(QPointF(p[6], p[7]))
            return True
        else:
            return False
        
    def highlightVertex(self, i, action):
        self._highlightIndex = i
        self._highlightMode = action

    def highlightClear(self):
        self._highlightIndex = None

    def copy(self):
        shape = Shape("%s" % self.label)
        shape.points = [p for p in self.points]
        shape.origin = [p for p in self.origin]
        shape.fill = self.fill
        shape.selected = self.selected
        shape._closed = self._closed
        if self.line_color != Shape.line_color:
            shape.line_color = self.line_color
        if self.fill_color != Shape.fill_color:
            shape.fill_color = self.fill_color
        shape.difficult = self.difficult
        return shape

    def __len__(self):
        return len(self.points)

    def __getitem__(self, key):
        return self.points[key]

    def __setitem__(self, key, value):
        self.points[key] = value
