from svgelements import *
import re
import os
import numpy as np
from python_tsp.distances import great_circle_distance_matrix
from python_tsp.heuristics import solve_tsp_local_search
from halo import Halo

def codeblock(subpath, extruder_coff=0.06):
    x, y = extractCoords(subpath)
    e = calculateDisplacement(x, y, extruder_coff)
    code = subpath2gcode(x, y, e)
    return code

def readSVG(source):
    svg = SVG.parse(source)
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

def subpath2gcode(x, y, e, feed_rate=2550, high_feed=6000):
    codelist = []
    initial_feed = 'G00'+' F{}\n'.format(high_feed)
    initial = 'G00'+' X'+str(x[0])+' Y'+str(y[0])+' E'+str(e[0])+'\n'
    codelist.append(initial_feed)
    codelist.append(initial)
    set_feedrate = 'G00'+' F{}\n'.format(feed_rate)
    codelist.append(set_feedrate)
    for i in range(len(x)-1):
        element = 'G01'+' X'+str(x[i+1])+' Y'+str(y[i+1])+' E'+str(e[i+1])+'\n'
        codelist.append(element)
    return codelist

def startCoords(subpaths):
    coords = []
    for subpath in subpaths:
        x, y = extractCoords(subpath)
        coords.append([x[0], y[0]])
    return coords

def sortIsland(subpaths):
    spinner = Halo(text='Sorting subpaths by solving TSP.', spinner='dots')
    spinner.start()
    coords = np.array(startCoords(subpaths))
    distance_matrix = great_circle_distance_matrix(coords)
    permutation, distance = solve_tsp_local_search(
    distance_matrix,
    x0=None,
    perturbation_scheme="ps6",
    max_processing_time=None,
    log_file=None,
    )
    spinner.succeed(text='Succeeded: Sorting')
    spinner.stop()
    return permutation

def setZlevel(z, feed_rate=6000):
    codes = []
    codes.append('G00'+' Z{}'.format(z)+' F{}\n'.format(feed_rate))
    return codes

    





