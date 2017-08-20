#!/usr/bin/env python3

# TkInter is a Python interface for Tk
from tkinter import *
from tkinter import ttk
import time
import random
start_time = time.time()

import math
import copy

from a_fit_box_1_read_svg import *
from a_fit_box_2_reorder_pts import *
from a_fit_box_3_make_pixel import *
# CALVIN NOTE:

# Summary:
# this file is supposed to conduct 2d bin packing, where it takes
# a polygon to serve as a bin and try to fit the other polygons into the bin
# in the most efficient way possible

# we use the word "container" instead of bin

# This, thing, is supposed to read a .svg file, which is a vector based
# images file filled with coordinate points and whatnot
# we enter it under "target_file" below

# time to go to the final file - a_fit_box.py

# ////////////////////////////////////////////////////////////////////////
# This reads the svg file, and produces a list of coordinate points
#      PROCESS  1    ///////////////////////////////////////

target_file = "drawingtest7.svg"     ## THIS IS THE SVG FILE TO READ
target_file_cont = "container.svg"     ## THIS IS THE OTHER SVG FILE TO READ

path_list = P_final_all_convert_svg_to_list(target_file)
container_pts = P_final_all_convert_svg_to_list(target_file_cont)

# ////////////////////////////////////////////////////////////////////////
# ////////////////////////////////////////////////////////////////////////
#     CREATE CANVAS    /////////////////////////////////
master = Tk()
CANVAS_LENGTH = 800
PIXEL_SIZE = 20
canvas_width = CANVAS_LENGTH  # max([max(i) for i in path_list])
canvas_height = CANVAS_LENGTH  # max([max(i) for i in path_list])
w = Canvas(master, width=canvas_width, height=canvas_height)
w.pack(side="left", padx=20, pady=20)

# DISPLAY BACKGROUND
w.create_rectangle(0, 0, CANVAS_LENGTH, CANVAS_LENGTH, outline="#476042", fill="white", width=1)

# ////////////////////////////////////////////////////////////////////////
# ////////////////////////////////////////////////////////////////////////
#     SET SCALE FOR ALL IMAGES    /////////////////////////////////
IMAGE_SIZE = CANVAS_LENGTH - (PIXEL_SIZE)

def set_image_size(orig_points2, IMAGE_SIZE):
    largest_coord = max(container_pts[0])
    IMAGE_SIZE = CANVAS_LENGTH - (PIXEL_SIZE)
    scal_factor = IMAGE_SIZE/largest_coord

    # SCALES image to fit within constraints
    # ALL RASTERIZED IMAGES WILL BE THE SAME SIZE (IMAGE_SIZE)
    CUR_MAX = max(path_list[0])
    orig_points2 = [i*scal_factor for i in orig_points2]
    return orig_points2

# largest_coord = max(container_pts[0])
# IMAGE_SIZE = CANVAS_LENGTH - (PIXEL_SIZE)
# scal_factor = IMAGE_SIZE/largest_coord
#
# # SCALES image to fit within constraints
# # ALL RASTERIZED IMAGES WILL BE THE SAME SIZE (IMAGE_SIZE)
# CUR_MAX = max(path_list[0])
# orig_points = [i*scal_factor for i in path_list[0]]
# cont_points = [i*scal_factor for i in container_pts[0]]

orig_points = path_list[0]
cont_points = container_pts[0]
orig_points = set_image_size(path_list[0], IMAGE_SIZE)
cont_points = set_image_size(container_pts[0], IMAGE_SIZE)


# ////////////////////////////////////////////////////////////////////////
# make cont_points go the bottom of the screen
# MIN_Y2 = max([i for i in cont_points if cont_points.index(i)%2 == 1])
MIN_Y2 = max(cont_points[::2])
y_offset = IMAGE_SIZE - MIN_Y2
for i22 in range(len(cont_points)):
   if i22 % 2 == 1:
       cont_points[i22] += y_offset
# cont_points = [(i + y_offset) if  for i in cont_points]
# (cont_points)

# ////////////////////////////////////////////////////////////////////////
# ////////////////////////////////////////////////////////////////////////
#      PROCESS  2    ///////////////////////////////////////
# This takes the coords taken from PROCESS 1 and rasterizes

# PIXEL_RES = 100  # every 20 real pixels make 1 Display Pixel Cell
PIXEL_RES = PIXEL_SIZE
# the actual size of the image is still the same
orig_points = [i/PIXEL_RES for i in orig_points]

orig_points = C_final_rearrange_points(orig_points)

approx_points = E_final_generate_approx(orig_points)

orig_points = [i*PIXEL_RES for i in orig_points]

approx_points = [i*PIXEL_RES for i in approx_points]

# ////////////////////////////////////////////////////////////////////////
# ////////////////////////////////////////////////////////////////////////
#    DISPLAY APPROX  POINTS      ////////////////////////////////////////

# DIPLAY APPROX IN PIXELS
for i3 in range(int(len(approx_points)/2)):
   i = 2*i3
   r_size = PIXEL_RES/2  # 10
   [x1, x2] = [approx_points[i] - r_size, approx_points[i+1] - r_size]
   # x2 = approx_points[i+1] - r_size
   x3 = approx_points[i] + r_size
   x4 = approx_points[i+1] + r_size
   w.create_rectangle(x1,x2,x3,x4, outline="#476042", fill="blue", width=1)

# DIPLAY APPROX AS POLYGON
# w.create_polygon(approx_points,fill="",outline="#476042",  width=1)

# # DISPLAY ORIGINAL
# w.create_polygon(points,fill="",outline="red",  width=1)

# DISPLAY GRID
s = 1
for i7 in range(10):
   for j7 in range(10):
       w.create_rectangle((100*i7)-s,(100*j7)-s,(100*i7)+s,(100*j7)+s, fill="gray", width=1)

# ////////////////////////////////////////////////////////////////////////
# ////////////////////////////////////////////////////////////////////////
#    DISPLAY ORIGINAL POINTS      ////////////////////////////////////////
colors = ["yellow", "red", "blue", "green"]
for j in range(len(path_list)):  # can change this to just path_list

   # OUTPUT ACTUAL POLYGON
   w.create_polygon(orig_points,fill="",outline="red",  width=1)

   # OUTPUT INDIVIDUAL POINTS OF POLYGON
   c_size = 3
   for ii4 in range(int((len(orig_points)/2))):
       ii4 *= 2
       x11 = orig_points[ii4] - c_size
       x12 = orig_points[ii4+1] - c_size
       x21 = orig_points[ii4] + c_size
       x22 = orig_points[ii4+1] + c_size
       w.create_oval(x11,x12,x21,x22,fill="grey", width=0.25)
   w.create_oval(orig_points[0] - c_size, orig_points[1] - c_size,
                 orig_points[0] + c_size, orig_points[1] + c_size,
                 fill = "red", width = 0.25)  # first point
   w.create_oval(orig_points[-2]-c_size,orig_points[-1]-c_size,orig_points[-2]+c_size,orig_points[-1]+c_size,fill="black", width=0.25)  # final point

w.create_text(20, 20, text="0,0")
w.create_text(120, 20, text="100,0")
w.create_text(20, 120, text="0,100")

# ////////////////////////////////////////////////////////////////////////
# ////////////////////////////////////////////////////////////////////////
#    DISPLAY CONTAINER      ////////////////////////////////////////
w.create_polygon(cont_points,fill="",outline="green",  width=1)


# ////////////////////////////////////////////////////////////////////////
# ////////////////////////////////////////////////////////////////////////
mainloop()
print("Time Taken is %f seconds" % (time.time() - start_time))

# ////////////////////////////////////////////////////////////////////////
# ////////////////////////////////////////////////////////////////////////
# ////////////////////////////////////////////////////////////////////////

# for each point in points:
#     line segment = get line segment ( pairs)
#     if there are whole numbers within the line segment, get them
#         == list of y's
#     with the list of y's = get the exes that are on the other side of line
#         = get equation of line, find points that intersect with integer y
#         = this is done by, extending x++, and making a line, taking cross product
#             = depending on which quadrant, we say that the the y-value is the corner
#                 #    Q2  |   Q1
#                 #------------------
#                 #    Q3  |   Q4
#
#             = Q3 - the y-value is every other half, and is bottom right
#             = also the last point get the Q2
#         = get all points that are closest to line segment with different y-value
#         = do this for next line segment
