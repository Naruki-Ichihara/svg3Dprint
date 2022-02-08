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

file.write(h)
for i in range(len(subpaths)):
    i = perm[i]
    code = codeblock(subpaths[i], coff, feedrate, fastfeedrate)
    file.writelines(code)
file.write(f)
file.close()