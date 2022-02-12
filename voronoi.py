from select import select
import numpy as np
import numpy.random as npr
from PIL import Image, ImageOps, ImageDraw
import scipy.interpolate as s
from scipy.spatial import Voronoi, voronoi_plot_2d, Delaunay, delaunay_plot_2d
import matplotlib.pyplot as plt
from svgtrace import trace

points_count = 10000

im = Image.open('./img/newton.jpeg')
im_g = im.convert(mode='L')
im_i = ImageOps.invert(im_g)
im_f = ImageOps.flip(im_i)
im_n = np.array(im_f)/256

Ny, Nx = im_n.shape

Lx, Ly = 340.3, 138.8
x = np.linspace(0, Lx, Nx)
y = np.linspace(0, Ly, Ny)
f = s.interp2d(x, y, im_n)
f_numpy = np.frompyfunc(lambda x, y: f(x, y).astype(float)[0], 2, 1)

seeds_x = npr.rand(points_count)*Lx
seeds_y = npr.rand(points_count)*Ly
seeds_xy = np.stack([seeds_x, seeds_y], axis=1)
probs = f_numpy(seeds_xy[:, 0], seeds_xy[:, 1])

def sigmoid(x, a):
    return 1.0/(1.0+np.exp(-a*x))

def selection(xy, probabilities, p=1):
    random_vector = npr.rand(len(probabilities))
    indices = probabilities > random_vector
    return xy[indices]

for i in range(5):
    selected = selection(seeds_xy, probs, p=5)
    seeds_xy = selected
    probs = f_numpy(seeds_xy[:, 0], seeds_xy[:, 1])

vor = Delaunay(selected)
fig = voronoi_plot_2d(vor, show_points=False, show_vertices=False, line_width=2.0)
plt.axis("off")
plt.xlim([0, Lx])
plt.ylim([0, Ly])
fig.savefig('test.png', dpi=360, bbox_inches='tight')