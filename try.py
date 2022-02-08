from svgelements import *
import svgcode as s
from svgcode.core import *

file = open('test.gcode', 'w')

source = './svg/sample.svg'

elements = s.readSVG(source)
path = elements[0]
subpaths = parseSubPaths(path)
perm = sortIsland(subpaths)
for i in range(len(subpaths)):
    i = perm[i]
    code = codeblock(subpaths[i])
    file.writelines(code)
file.close()

"""
dwg = s.Drawing('test.svg', size=(297, 200))
dwg.add(s.path.Path(d=sub.d(), stroke=s.utils.rgb(0, 0, 205)))
dwg.save()
"""