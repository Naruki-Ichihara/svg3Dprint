from svgelements import *
from svgcode.core import *

file = open('gcodes/test/test.gcode', 'w')
source = '/workdir/svg/test/test.svg'
feedrate = 1200
fastfeedrate = 8000
pathwidth = 0.8
retraction = 0.5
coff = calculateEcoff(pathwidth, h=0.25, lamda=0.9)

h, f = preset('./presets/composer_anisoprint.json')

elements = readSVG(source)
path_1 = parseSubPaths(elements[0])
path_2 = parseSubPaths(elements[1])

print(len(elements))
permutation_1 = sortPaths(path_1)
permutation_2 = sortPaths(path_2)
start = parge([10, 10], [120, 10], coff)
file.write(h)
file.write(setZlevel(0.25))
file.writelines(start)
zs = np.arange(0.25, 0.25+5, 0.25)
index = 0
for z in zs:
    file.write(setZlevel(z))
    for i in range(len(path_1)):
        j = permutation_1[i]
        code = codeblock(path_1[j], coff, feedrate, fastfeedrate, retraction)
        file.writelines(code)
    for i in range(len(path_2)):
        j = permutation_2[i]
        code = codeblock(path_2[j], coff, feedrate, fastfeedrate, retraction)
        file.writelines(code)
        pass
    index += 1
file.write(f)
file.close()