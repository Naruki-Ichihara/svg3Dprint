from svgelements import *
from svgcode.core import *

file = open('gcodes/mantis.gcode', 'w')
source = './svg/mantis.svg'
feedrate = 2550
fastfeedrate = 6000
pathwidth = 0.5
coff = calculateEcoff(pathwidth)

h, f = preset('./presets/composer_anisoprint.json')

elements = readSVG(source)
path = elements[0]
subpaths = parseSubPaths(path)
perm = sortIsland(subpaths)
start = parge([10, 10], [60, 10], coff*10)

file.write(h)
file.writelines(start)
file.write(setZlevel(0.0))
for i in range(len(subpaths)):
    j = perm[i]
    code = codeblock(subpaths[j], coff, feedrate, fastfeedrate)
    file.writelines(code)
    file.write(setZlevel(0.2*i))
file.write(f)
file.close()