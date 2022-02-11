from svgelements import *
from svgcode.core import *

file = open('gcodes/voronoi.gcode', 'w')
source = './svg/voronoi.svg'
feedrate = 2550
fastfeedrate = 6000
pathwidth = 0.5
coff = calculateEcoff(pathwidth)

h, f = preset('./presets/composer_anisoprint.json')

elements = readSVG(source)
path = elements[0]
subpaths = parseSubPaths(path)
print(len(subpaths))
#perm = sortPaths(subpaths)
start = parge([10, 10], [60, 10], coff*10)

file.write(h)
file.writelines(start)
file.write(setZlevel(0.25))
for i in range(len(subpaths)):
    code = codeblock(subpaths[i], coff, feedrate, fastfeedrate)
    file.writelines(code)
file.write(f)
file.close()