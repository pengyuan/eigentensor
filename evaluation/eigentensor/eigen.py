#!/usr/bin/env python
# coding: UTF-8
from __future__ import division
import numpy as np
# from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
from build.multivariate_transition_tensor import mtt
import settings
from utils.sequence import init_data, init_data_by_user
from utils.tensor import tensor_three_mode_product, delta_tensor_norm, get_check_tensor, inreducible_tensor
import matplotlib.cm as cmx
from mpl_toolkits.mplot3d import Axes3D

import matplotlib.cm as cmx
from mpl_toolkits.mplot3d import Axes3D
def scatter3d(x,y,z, cs, colorsMap='jet'):
    cm = plt.get_cmap(colorsMap)
    print min(cs), max(cs)
    # cNorm = plt.matplotlib.colors.Normalize(vmin=min(cs), vmax=max(cs))
    cNorm = plt.matplotlib.colors.Normalize(vmin=0, vmax=0.00005)
    scalarMap = cmx.ScalarMappable(norm=cNorm, cmap=cm)
    fig = plt.figure()
    ax = Axes3D(fig)
    ax.scatter(x, y, z, c=scalarMap.to_rgba(cs))
    scalarMap.set_array(cs)
    fig.colorbar(scalarMap)
    plt.show()

if __name__ == '__main__':
    # beijing = (39.433333, 41.05, 115.416667, 117.5)
    # haidian = (39.883333, 40.15, 116.05, 116.383333)
    region = (39.883333, 40.05, 116.05, 116.383333)
    filter_count = 0
    time_num = settings.TIME_SLICE
    train_percent = 0.95
    alpha = 0.95
    split_percent = 0.5
    filter_poi_count = 0

    x_values = []
    y_values1 = []
    y_values2 = []
    y_values3 = []
    #
    # # data, axis_users, axis_pois, check_data = init_data(region, filter_count, train_percent)
    data, axis_users, axis_pois, check_data = init_data_by_user(tuple([0, 3]), filter_count, train_percent, split_percent, filter_poi_count)
    user_num = len(axis_users)
    poi_num = len(axis_pois)

    init_tensor = [[[1/(poi_num * time_num * user_num) for i in range(poi_num)] for j in range(time_num)] for k in range(user_num)]
    transition_tensor = inreducible_tensor(mtt(data, user_num, poi_num), user_num, time_num, poi_num, alpha)
    res, iterator_values = tensor_three_mode_product(transition_tensor, init_tensor)

    x = []
    y = []
    z = []
    value = []
    for i in range(user_num):
        for j in range(time_num):
            for k in range(poi_num):
                x.append(i)
                y.append(j)
                z.append(k)
                value.append(res[i][j][k])


    # cm = plt.get_cmap("RdYlGn")
    # x = np.random.rand(30)
    # y = np.random.rand(30)
    # z = np.random.rand(30)
    # #col = [cm(float(i)/(29)) for i in xrange(29)] # BAD!!!
    # col = [float(i)/(30) for i in xrange(30)]

    # x = [i for i in range(30)]
    # y = [i for i in range(30)]
    # z = [i for i in range(30)]
    # value = [i/30 for i in range(30)]
    scatter3d(x, y, z, value)
    # def randrange(n, vmin, vmax):
    #     return (vmax-vmin)*np.random.rand(n) + vmin
    #
    # fig = plt.figure()
    # ax = fig.add_subplot(111, projection='3d')
    # n = 100
    # for c, m, zl, zh in [('r', 'o', 0, 100), ('b', '^', 0, 30)]:
    #     xs = randrange(n, 23, 32)
    #     ys = randrange(n, 0, 100)
    #     zs = randrange(n, zl, zh)
    #     ax.scatter(xs, ys, zs, c=c, marker=m)
    #
    # ax.set_xlabel(u'用户')
    # ax.set_ylabel(u'时间')
    # ax.set_zlabel(u'地点')
    #
    # plt.show()

