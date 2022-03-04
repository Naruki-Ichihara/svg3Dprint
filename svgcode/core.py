from svgelements import *
import re
import os
import json
import numpy as np
from python_tsp.distances import great_circle_distance_matrix
from python_tsp.heuristics import solve_tsp_local_search
from halo import Halo

def codeblock(subpath, extruder_coff, feed_rate=2550, high_feed=6000, retraction=1.0):
    x, y = extractCoords(subpath)
    e = calculateDisplacement(x, y, extruder_coff)
    code = subpath2gcode(x, y, e, extruder_coff, feed_rate, high_feed, retraction)
    return code

def readSVG(source, ppi=25.4):
    svg = SVG.parse(source, ppi=25.4)
    elements = []
    for element in svg.elements():
        try:
            if element.values['visibility'] == 'hidden':
                continue
        except (KeyError, AttributeError):
            pass
        if isinstance(element, SVGText):
            pass
        elif isinstance(element, Path):
            if len(element) != 0:
                elements.append(element)
        elif isinstance(element, Shape):
            e = Path(element)
            e.reify()  # In some cases the shape could not have reified, the path must.
            if len(e) != 0:
                elements.append(e)
        elif isinstance(element, SVGImage):
            try:
                element.load(os.path.dirname(source))
                if element.image is not None:
                    pass
            except OSError:
                pass
    return elements

def parseSubPaths(path):
    subpaths = []
    for i in range(path.count_subpaths()):
        subpaths.append(path.subpath(i))
    return subpaths

def extractCoords(subpath):
    x = []
    y = []
    for i in range(len(subpath)-1):
        splited = re.split('[ ,]', subpath[i].d())
        x.append(float(splited[1]))
        y.append(float(splited[2]))
    return x, y

def calculateDisplacement(x, y, coff):
    disp = []
    disp.append(0.0)
    l = 0.0
    for i in range(len(x)-1):
        dx = x[i+1] - x[i]
        dy = y[i+1] - y[i]
        l += np.sqrt(dx**2 + dy**2)*coff
        disp.append(l)
    return disp

def subpath2gcode(x, y, e, coff, feed_rate, high_feed, retraction=1.0):
    codelist = []
    def_origin = 'G92 E0\n'
    initial_feed = 'G00'+' E{}'.format(retraction)+' F{}\n'.format(high_feed)
    initial = 'G00'+' X'+str(x[0])+' Y'+str(y[0])+' E'+str(e[0]+retraction)+'\n'
    codelist.append(def_origin)
    codelist.append(initial_feed)
    codelist.append(initial)
    set_feedrate = 'G00'+' F{}\n'.format(feed_rate)
    codelist.append(set_feedrate)
    for i in range(len(x)-1):
        element = 'G01'+' X'+str(x[i+1])+' Y'+str(y[i+1])+' E'+str(e[i+1]+retraction)+'\n'
        codelist.append(element)
    dx = x[-1] - x[0]
    dy = y[-1] - y[0]
    r = np.sqrt(dx**2+dy**2)
    e_close = e[-1]+r*coff+retraction
    close = 'G00'+' X'+str(x[0])+' Y'+str(y[0])+' E'+str(e_close)+'\n'
    codelist.append(close)
    retract = 'G00'+' E{}'.format(e_close - retraction)+'\n'
    codelist.append(retract)
    return codelist

def startCoords(subpaths):
    coords = []
    for subpath in subpaths:
        x, y = extractCoords(subpath)
        coords.append([x[0], y[0]])
    return coords

def sortPaths(subpaths):
    spinner = Halo(text='Sorting subpaths by solving TSP.', spinner='dots')
    spinner.start()
    coords = np.array(startCoords(subpaths))
    distance_matrix = great_circle_distance_matrix(coords)
    permutation, distance = solve_tsp_local_search(
    distance_matrix,
    x0=None,
    perturbation_scheme="two_opt",
    max_processing_time=None,
    log_file=None,
    )
    spinner.succeed(text='Succeeded: Sorting')
    spinner.stop()
    return permutation

def setZlevel(z):
    return 'G00'+' Z{}\n'.format(z)

def preset(source):
    f = open(source, 'r')
    elements = json.load(f)
    head = elements['header']
    foot = elements['footer']
    return head, foot

def calculateEcoff(w, lamda=1.00, h=0.2, D=1.75):
    return lamda*4*h*w/np.pi/D**2

def parge(start, stop, coff, feed_rate=1200):
    codes = []
    dx = stop[0] - start[0]
    dy = stop[1] - start[1]
    distance = np.sqrt(dx**2+dy**2)
    e = distance*coff
    codes.append('G00'+' X{}'.format(start[0])+' Y{}'.format(start[1])+' F{}\n'.format(feed_rate))
    codes.append('G01'+' X{}'.format(stop[0])+' Y{}'.format(stop[1])+' E{}\n'.format(e))
    return codes
