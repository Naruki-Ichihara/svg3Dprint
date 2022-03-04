from svgelements import *
from svgcode.core import *

file = open('gcodes/mbb_double.gcode', 'w')
source = '/workdir/svg/mbb_double.svg'
feedrate = 1200
fastfeedrate = 8000
pathwidth = 0.8
retraction = 0.5
coff = calculateEcoff(pathwidth, h=0.25, lamda=0.9)

h, f = preset('./presets/composer_anisoprint.json')

elements = readSVG(source)
path_1 = parseSubPaths(elements[0])
path_2 = parseSubPaths(elements[1])
path_3 = parseSubPaths(elements[2])
path_4 = parseSubPaths(elements[3])
shield = parseSubPaths(elements[4])

print(len(elements))
permutation_1 = sortPaths(path_1)
permutation_2 = sortPaths(path_2)
permutation_3 = sortPaths(path_3)
permutation_4 = sortPaths(path_4)
file.write(h)
file.write(setZlevel(0.25))
zs = np.arange(0.25, 0.25+10, 0.25)
index = 0
for z in zs:
    file.write(setZlevel(z))
    for i in range(len(shield)):
        code = codeblock(shield[i], coff, feedrate, fastfeedrate, 5.0)
        file.writelines(code)
    if index % 2 == 0:
        for i in range(len(path_1)):
            j = permutation_1[i]
            code = codeblock(path_1[j], coff, feedrate, fastfeedrate, retraction)
            file.writelines(code)
        for i in range(len(path_3)):
            j = permutation_3[i]
            code = codeblock(path_3[j], coff, feedrate, fastfeedrate, retraction)
            file.writelines(code)
    else:
        for i in range(len(path_2)):
            j = permutation_2[i]
            code = codeblock(path_2[j], coff, feedrate, fastfeedrate, retraction)
            file.writelines(code)
        for i in range(len(path_4)):
            j = permutation_4[i]
            code = codeblock(path_4[j], coff, feedrate, fastfeedrate, retraction)
            file.writelines(code)
            pass
    index += 1
file.write(f)
file.close()