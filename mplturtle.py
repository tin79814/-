#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec 27 21:22:27 2019

@author: npchen

v3: 修正了 circle 的 extent 與 steps 參數的表現
    修正了換顏色、style時會漏掉一個點的缺失
    修正了 backward 沒有倒退反而前進的缺失
    增加了 dot 的操作方法。
v4: 增加了簡寫的指令，例如 .fd(), .bk(), .up(), .down()
        .setpos(), setposition(), .lt(), .rt()
    增加了 .position(), .pos()
    增加了 .heading()
    增加了 .setheading(), 以及簡寫的 .seth()
    改寫了 .dot(size, color) 增加了第二個參數 color

"""

from math import cos, sin, pi, acos


class MplTurtle(object):
    
    def __init__(self):
        self.current_xy = (0.0,0.0)
        self.x_list = [self.current_xy[0] ]
        self.y_list = [self.current_xy[1] ]
        self.pen_status = True
        self.heading_angle = 0.0
        self.line_que = []
        self.color = "k"
        self.style = "-"
        self.penwidth = 1
    
    def position(self):
        return self.current_xy
    
    def pos(self):
        # alias of position
        return self.position()
    
    def setheading(self, angle):
        self.heading_angle = angle
        
    def seth(self, angle):
        # alias of setheading
        self.setheading(angle)
        
    def heading(self):
        return self.heading_angle
        
    def pendown(self):
        # action only when pen is up
        if self.pen_status == False:
            self.pen_status = True
            self.x_list.append(self.current_xy[0])
            self.y_list.append(self.current_xy[1])
    
    def pd(self):
        # alias of pendown
        self.pendown()
        
    def down(self):
        # alias of pendown
        self.pendown()
    
    def dump_xylist(self):
        # color=self.color, linestyle= "-",\
        #            linewidth=self.penwidth
        if len(self.x_list) > 0:
            line_param_dict={"color": self.color, "style": self.style, "width": self.penwidth}
            self.line_que.append([self.x_list, self.y_list, line_param_dict] )
            if self.pen_status:
                # pendown and dump point list
                # this must be the cases of changing color or style
                # add the current point as the starting point for the next new
                # line segment
                self.x_list = [self.current_xy[0] ]
                self.y_list = [self.current_xy[1] ]
            else:
                # pen up and dump poin list
                # normal case of line ending
                self.x_list = []
                self.y_list = []
        
    
    def penup(self):
        # action only when pen is down
        if self.pen_status == True:
            self.pen_status = False
            self.dump_xylist()

    def pu(self):
        # alias of penup
        self.penup()
        
    def up(self):
        # alias of penup
        self.penup()
        
    def isdown(self):
        return self.pen_status
        
    def goto(self,x,y):
        self.current_xy = (x, y)
        if self.pen_status:
            # pendown
            self.x_list.append(self.current_xy[0])
            self.y_list.append(self.current_xy[1])
    
    def setpos(self,x,y):
        # alias of goto
        self.goto(x,y)
        
    def setposition(self,x,y):
        # alias of goto
        self.goto(x,y)

    def home(self):
        self.goto(0,0)
        self.heading_angle= 0.0

    def forward(self,dist):
        theta_rad = self.heading_angle * pi / 180
        delta_r = (dist * cos(theta_rad), dist * sin(theta_rad ) )
        new_x = self.current_xy[0] + delta_r[0]
        new_y = self.current_xy[1] + delta_r[1]
        
        self.goto(new_x, new_y)

    def fd(self,dist):
        # alias of forward
        self.forward(dist)        
            
    def backward(self, dist):
        theta_rad = self.heading_angle * pi / 180
        delta_r = (dist * cos(theta_rad), dist * sin(theta_rad ) )
        new_x = self.current_xy[0] - delta_r[0]
        new_y = self.current_xy[1] - delta_r[1]
        
        self.goto(new_x, new_y)    

    def bk(self,dist):
        # alias of backward
        self.backward(dist)
        
    def back(self,dist):
        # alias of backward
        self.backward(dist)
        
    def right(self,angle):
        self.heading_angle -= angle
        if self.heading_angle < 0:
            self.heading_angle += 360
            
    def rt(self, angle):
        # alias of right
        self.right(angle)
            
    def left(self, angle):
        self.heading_angle += angle
        if self.heading_angle > 360:
            self.heading_angle -= 360
            
    def lt(self, angle):
        # alias of left
        self.left(angle)
    
    def circle(self, radius, extent=None, steps=None):
        if extent == None:
            extent = 360
        
        if steps == None:
            # default (draw a circle);  a polygon with enough sides (steps)
            # each step is approximately forward(1)
            apex_angle_rad = acos(1- 0.5* (1.0/(radius * radius)))
            apex_angle = apex_angle_rad / pi * 180
            
            # takes the value of rounding off 
            # i.e., take the integer value less than the ratio (float)
            # so that each step is about forward(1.x)
            steps = int(extent / apex_angle )
            
            # re-calculate the apex_angle in the following block of code
            
            
        if steps >= 1:
            # for the case of steps == None, since it is re-assigned w/ value
            # as well as steps with value when this method is called
            # the only case cannot get here is steps = 0
            apex_angle = extent / steps
            apex_angle_rad = apex_angle * pi / 180
            each_step = (2 * (1 - cos(apex_angle_rad))) ** 0.5 * abs(radius)

            if radius < 0:
                apex_angle = - apex_angle
                apex_angle_rad = - apex_angle_rad
            
            # draw a polygon
            # imagine the lines connecting each turning point to the center
            # each piece of pie is an isosceles triangle
            
            # first turn requires only (extent/steps) * 0.5
            self.left(apex_angle * 0.5)
            
            
            self.forward(each_step)
            
            for i in range(steps - 1):
                # the turns after the first require apex_angle
                self.left(apex_angle)
                self.forward(each_step)
                
            self.left(apex_angle * 0.5)
                
            
        
    def pencolor(self, color_str):
        self.dump_xylist()
        self.color = color_str        
        
    def penstyle(self, style_str):
        self.dump_xylist()
        self.style = style_str        
        
    def dot(self, size, color_name="default"):        
        
        # add the current point (and only one point) into tmp x_list, y_list
        tmp_x_list = [self.current_xy[0] ]
        tmp_y_list = [self.current_xy[1] ]    
        
        if color_name == "default":
            color_name = self.color
        
        # add to line_que with marker parameter setting
        line_param_dict={"color": color_name, "style": "o", "size": size}
        self.line_que.append([tmp_x_list, tmp_y_list, line_param_dict] )
        

        


        
        
    def show(self, ax):
        if len(self.x_list) != 0:
            # did not penup to have a member in line_que
            self.dump_xylist()
            
        for i in range(len(self.line_que)):
            a_line_x = self.line_que[i][0]
            a_line_y = self.line_que[i][1]
            a_line_style = self.line_que[i][2]
            
            # check if the style is for a marker (dot)
            if a_line_style["style"] == "o":
                # this is from dot method
                ax.plot(a_line_x, a_line_y, color=a_line_style["color"], \
                        marker="o",\
                        markersize=a_line_style["size"] )
            else:
                # regular line segment
                ax.plot(a_line_x, a_line_y, color=a_line_style["color"], \
                    linestyle= a_line_style["style"],\
                    linewidth=a_line_style["width"] )
            

        ax.set_aspect(aspect = "equal")
        
            
    
        
    
        
        

