#!/usr/bin/env python
# coding: UTF-8

# 1.MTT与DTA预测效果的对比
# 2.初始张量的对比
# 3.迭代方法的对比
# 4.训练集对效果的影响
# 5.时间片对效果的影响
# 6.mapreduce的效果：内存消耗


# from __future__ import division
import numpy
from mayavi import mlab
# def b(a):
#     for i in range(len(a)):
#         for j in range(len(a[0])):
#             a[i][j] = 0.1 * a[i][j]
#     return a
#
# a = [[1,2], [3,4]]
# print b(a)

#
# import settings
# from utils.sequence import init_data
#
# beijing = (39.433333, 41.05, 115.416667, 117.5)
# haidian = (39.883333, 40.15, 116.05, 116.383333)
# region = (39.883333, 40.05, 116.05, 116.383333)
# filter_count = 500
# time_num = settings.TIME_SLICE
# data, axis_users, axis_pois, check_data = init_data(haidian, filter_count)
# user_num = len(axis_users)
# poi_num = len(axis_pois)
#
# print "需要"+str(pow(poi_num*user_num*24,2)/(1024*1024*1024))+"GB内存"
#
#
# #x, y, z = numpy.mgrid[0:6:6j, 0:2:2j, 0:1033:1033j]
# x, y, z = numpy.mgrid[0:1000:6j, 0:1000:2j, 0:1000:1033j]
#
#
# val = numpy.random.random(z.shape)
# print type(val)
# print x.shape, y.shape, z.shape
# # Plot and show in mayavi2
# pts = mlab.points3d(x, y, z, val, scale_factor=10, transparent=True)
# mlab.show()



# # Create some random data
# N = 20
# # x, y, z = numpy.mgrid[-5:5:20j, -5:5:20j, -5:5:20j]
# # print x[2][1][1]
# # print y[1][2][1]
# # print z[1][1][2]
# x = numpy.mgrid[-5:5]
# y = numpy.mgrid[-5:5]
# z = numpy.mgrid[0:5]
#
# print x
# print y
# print z
# val = numpy.random.random(z.shape)
#
# print val.shape
# # Plot and show in mayavi2
# # pts = mlab.points3d(x, y, z, val, scale_factor=0.4, transparent=False)
# # mlab.show()


# tutorial1.py

# Created by RunningOn, 20091005

"""

本脚本是mayavi的最基本的入门教程

"""

import math

# from mayavi import mlab
#
# def main():
#
#      data = [[0 for y in xrange(100)] for x in xrange(100)] #data是一个100 * 100的二维数组
#
#      factor = math.pi / 100;
#
#      for x in xrange(100):
#
#          for y in xrange(100):
#
#              data[x][y] = 50 * math.cos((x+y) * factor)
#
#      mlab.surf(data)     #绘制3D数据图
#
#      mlab.show()         #显示出来
#
#      return 0
#
# if __name__ == '__main__':
#
#      main()
# print "需要"+str((8842*178*24)/(1024*1024*1024)) + "GB内存"
# print "需要"+str(pow(8842*178*24, 2)/(1024*1024*1024*1024)) + "TB内存"
# print "需要"+str((10000*10000*24)/(1024*1024*1024)) + "GB内存"

# import matplotlib.pyplot as plt
# from mpl_toolkits.mplot3d import Axes3D
# fig = plt.figure()
# ax = fig.add_subplot(111, projection='3d')
# X = [1, 1, 2, 2]
# Y = [3, 4, 4, 3]
# Z = [1, 2, 1, 1]
# ax.plot_trisurf(X, Y, Z)
# plt.show()

# import numpy as np
# from mpl_toolkits.mplot3d import Axes3D
# import matplotlib.pyplot as plt
#
# def randrange(n, vmin, vmax):
#     return (vmax-vmin)*np.random.rand(n) + vmin
#
# fig = plt.figure()
# ax = fig.add_subplot(111, projection='3d')
# n = 100
# for c, m, zl, zh in [('r', 'o', -50, -25), ('b', '^', -30, -5)]:
#     xs = randrange(n, 23, 32)
#     ys = randrange(n, 0, 100)
#     zs = randrange(n, zl, zh)
#     ax.scatter(xs, ys, zs, c=c, marker=m)
#
# ax.set_xlabel('X Label')
# ax.set_ylabel('Y Label')
# ax.set_zlabel('Z Label')
#
# plt.show()
#
#
#
# '''
# Created on 18 Jun 2013
# @author: M. Arzul
#      ____   ____    ___        _    ____    ___   _______
#     |    \ |    \  / _ \      | |  /    |  / __\ |__   __|
#     | ()_/ | () / | | | |  _  | | | _()_/ | /       | |
#     | |    | |\ \ | |_| | | |_/ | | \__   | \___    | |
#     |_|    |_| \_\ \___/   \___/   \____|  \___/    |_|
#      ______   _____   _   ______   ____    ___    ___    _
#     / __   / /     \ \ \ \   ___| |    \  / _ \  |   \  | |
#    / /  / / / /| |\ \ \ \ \ \     | () / | | | | | |\ \ | |
#   / /__/ / / / | | \ \ \ \ \ \___ | |\ \ | |_| | | | \ \| |
#  /______/ /_/  |_|  \_\ \_\ \___/ |_| \_\ \___/  |_|  \___|
# A general-purpose plotter for heatmaps in any of the following coordinate systems:
#     > Geographic
#     > Projected
#     > Pixel
# CAVEAT: the random point generator makes tuples which matplotlib can interpret as (X, Y) which
#     makes sense on a Euclidean plane or projected system, but LAT/LON is in the reverse order!!!
#     Therefore, specify bounds as follows:
#         > [min_x, max_x, min_y, max_y] (l,r,b,t) when working in (X, Y)
#         > [min_lat, max_lat, min_lon, max_lon] (s,n,w,e) when working in LAT/LON
# '''
#
# def random_coords(num, bounds):
#     '''
#     Returns random points.
#     @param num: The number of points to generate.
#     @type num: Integer
#     @param bounds: The bounding coordinates of the points to generate, in the form [left, right, bottom, top].
#     @type bounds: List of 4 ints
#     @return: List of 2-tuples of floats that represents a set of X, Y coordinates.
#     @rtype: List of 2-tuples of floats
#     '''
#     from random import random as r
#     points = []
#     xdim = bounds[1] - bounds[0]
#     ydim = bounds[3] - bounds[2]
#     for _ in xrange(num):
#         x = r() * xdim + bounds[0]
#         y = r() * ydim + bounds[2]
#         points.append((x, y))
#     return points
#
# def heatmap_tile(level=0, x=0, y=0, coords=[]):
#     '''
#     Creates a 256x256 heatmap tile for the specified zoom level and location for the given coordinates.
#     @param level: The zoom level of the tile, between 0 and 21.
#     @type level: Integer
#     @param x: The X coordinate of the tile.
#     @type x: Integer
#     @param y: The Y coordinate of the tile.
#     @type y: Integer
#     @param coords: The X, Y coordinates of points.
#     @type coords: List of 2-tuples of floats
#     @return: A pixel matrix heatmap for the given points.
#     @rtype: Rectangular numpy matrix of floats
#     '''
#
#     import numpy as np
#     from time import time
#     import globalmaptiles as gmt
#
#     print "Requesting tile ("+str(x)+", "+str(y)+") for level "+str(level)+"..."
#     y = 2** level - y -1
#
#     world = gmt.GlobalMercator()
#     bounds = world.TileBounds(x, y, level) # ( minx, miny, maxx, maxy )
#
#     limx = (bounds[2]-bounds[0]) / 4
#     limy = (bounds[3]-bounds[1]) / 4
#
#     print "\tBounds of tile: "+str(bounds)
#
#     tileTop = 256 * y
#     tileLeft = 256 * x
#
#     if len(coords) == 0:
#         print "No points provided. Returned blank."
#         return np.array([[0.] * 256] * 256)
#
#     print "\t"+str(len(coords)), "points provided."
#     coords_proj = []
#     coords_pyra = []
#     coords_tile = []
#     for point in coords:
#         point_proj = world.LatLonToMeters(point[0],point[1])
#         if (bounds[0]-limx <= point_proj[0] <= bounds[2]+limx) and (bounds[1]-limy <= point_proj[1] <= bounds[3]+limy):
#             coords_proj.append(point_proj)
#             point_pyra = world.MetersToPixels(point_proj[0], point_proj[1], level)
#             coords_pyra.append(point_pyra)
#             coords_tile.append((point_pyra[0]-tileLeft, point_pyra[1]-tileTop))
#     n = len(coords_proj)
#     print "\tTrimmed to "+str(n)+" points."
#     if n == 0:
#         print "No points close enough to tile. Returned blank."
#         return np.array([[0.] * 256] * 256)
#
#     print "\t\tLAT/LON points:"
#     print "\t\t"+str(coords)
#     print "\t\tProjected points:"
#     print "\t\t"+str(coords_proj)
#     print "\t\tPyramid points:"
#     print "\t\t"+str(coords_pyra)
#     print "\t\tTile points:"
#     print "\t\t"+str(coords_tile)
#
#     print "\tStarting raster generation..."
#     s = time()
#     heatmap = np.array([[0.] * 512] * 512)
#     from scipy import ndimage
#     for point_tile in coords_tile:
#         heatmap[point_tile[1]+128,point_tile[0]+128] += 1000.
#     heatmap = ndimage.gaussian_filter(heatmap, sigma=15)
#     heatmap = heatmap[128:384,128:384]
#
#     e = time()
#     print "\tDone."
#     print "\tTime: " + str(e - s)
#     print "\tAverage time per point: " + str((e - s) / n)
#     print "Returning tile."
#     return heatmap
#
# def show_heatmap(heatmap):
#     '''
#     Displays a heatmap using matplotlib.pyplot.
#     @param heatmap: A pixel matrix heatmap.
#     @type heatmap: Rectangular numpy matrix of floats
#     @rtype: Void
#     '''
#     import matplotlib.pyplot as plt
#
#     print "Displaying heat map..."
#     plt.xlim(0, 256)
#     plt.ylim(0, 256)
#     plt.imshow(heatmap, cmap='hot', origin='lower', extent=[0,256,0,256])
#     plt.show()
#     print "Done."
#
# def show_3D_heatmap(heatmap):
#     '''
#     Displays a heatmap in 3D using MayaVi.
#     @param heatmap: A pixel matrix heatmap.
#     @type heatmap: Rectangular numpy matrix of floats
#     @rtype: Void
#     '''
#     print "Loading 3D modules..."
#     from mayavi import mlab
#     print "Done."
#     print "Displaying 3D heatmap..."
#     rescale = heatmap * 255. / heatmap.max()
#     rescale = rescale[::-1]
#     mlab.surf(rescale, colormap='hot', vmin=0, vmax=255)
#     mlab.show()
#     print "Done."
#
# def save_heatmap(heatmap, path='./image.png', colour=False):
#     '''
#     Saves a heatmap to the specified path, in colour if colour is True, or in greyscale if colour is False.
#     @param heatmap: A pixel matrix heatmap.
#     @type heatmap: Rectangular numpy matrix of floats
#     @param path: The file path to save the file into.
#     @type path: String
#     @param colour: Whether or not the heatmap should be saved in colour.
#     @type colour: Boolean
#     @rtype: Void
#     '''
#     from scipy import misc
#     import numpy as np
#     from time import time
#     import Image
#     heatmap = heatmap[::-1]
#     if colour:
#         #from matplotlib import colors
#         from matplotlib.pyplot import cm
#
#         print "Saving colour heatmap to " + path + "..."
#
#         print "\tMapping to colour scale..."
#         s = time()
#         print "\t\tRescaling..."
#         heatmap = heatmap / 5.
#         print"\t\tDone."
#
#         # excerpt from the registered 'hot' colormap:
#         # '_segmentdata': {'blue': ((0.0, 0.0, 0.0), (0.746032, 0.0, 0.0), (1.0, 1.0, 1.0)),
#                         # 'green': ((0.0, 0.0, 0.0), (0.365079, 0.0, 0.0), (0.746032, 1.0, 1.0), (1.0, 1.0, 1.0)),
#                         # 'red': ((0.0, 0.0416, 0.0416), (0.365079, 1.0, 1.0), (1.0, 1.0, 1.0))}
#         #cdict = [(0.0,      (1.0, 0.0, 0.0, 0.0)),
#         #         (0.365079, (1.0, 0.0, 0.0, 0.5)),
#         #         (0.746032, (1.0, 1.0, 0.0, 0.5)),
#         #         (1.0,      (1.0, 1.0, 1.0, 0.5))]
#         #cmap_hot = colors.LinearSegmentedColormap.from_list(name='yes', colors=cdict)
#         #heatmap_color = Image.fromarray(np.uint8(cmap_hot(heatmap, bytes=True)))
#
#         heatmap_color = Image.fromarray(np.uint8(cm.hot(heatmap, alpha=0.5, bytes=True)))
#         e = time()
#
#         print "\tTime to convert to colour: " + str(e - s)
#         misc.imsave(path, heatmap_color)
#         print "Done."
#     else:
#         print "Saving greyscale heatmap to " + path + "..."
#         misc.imsave(path, heatmap)
#         print "Done."
#
# def coords_to_geojson(coords):
#     '''
#     Converts a set of coordinate pairs to a GeoJSON object.
#     @param coords: An array of coordinate pairs.
#     @type coords: Array of 2-tuples or length-2 arrays.
#     @rtype: GeoJSON object
#     '''
#     import json
#     obj = {u'type':u'FeatureCollection', u'features':[]}
#     for point in coords:
#         obj[u'features'].append({u'type':u'Feature', u'geometry':{u'type':u'Point',u'coordinates':[point[1],point[0]]}})
#     return json.dumps(obj)
#
# if __name__ == "__main__":
#
#     from time import time
#     s = time()
#
#     bounds_geo = [-85, 85, -180, 180]
#
#     #ten_random = random_coords(10, bounds_geo)
#     hundred_random = random_coords(100, bounds_geo)
#     #smiley = [[25,45], [25,35], [35,25], [45,15], [55,15], [65,25], [75,35], [75,45], [35,75], [35,65], [65,65], [75,65]]
#     #stellenbosch = [[-33.9200, 18.8600]]
#     #center = [[0,0]]
#     #square = [[45,45],[-45,45],[45,-45],[-45,-45]]
#     #technopark = [[-33.964807, 18.8372767]]
#     #madagascar = [[-20,47]]
#
#     tile = heatmap_tile(level = 0, x = 0, y = 0, coords=hundred_random)
#     #show_heatmap(tile)
#     #show_3D_heatmap(tile)
#     save_heatmap(tile, path="/home/marzul/test.png", colour=True)
#     #print coords_to_geojson(ten_random)
#     e = time()
#     print "total time: "+str(e-s)