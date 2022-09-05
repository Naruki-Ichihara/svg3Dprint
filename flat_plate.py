from svgelements import *
from svgcode.core import *

file = open('gcodes/05mm_100percent_uni_90.gcode', 'w')
source = '/workdir/svg/flatplate/05mm_100percent_uni_90.svg'
feedrate = 1800
feedrate_init = 900
fastfeedrate = 8000
pathwidth = 0.5
retraction = 0.5
initial_mul = 1.0
thickness = 2.0
coff = calculateEcoff(pathwidth, h=0.2, lamda=1.1, D=1.75)

h, f = preset('./presets/composer_anisoprint.json')

elements = readSVG(source)
path_1 = parseSubPaths(elements[0])
path_2 = parseSubPaths(elements[2])
shield = parseSubPaths(elements[1])

print(len(elements))
permutation_1 = sortPaths(path_1)
permutation_2 = sortPaths(path_2)
file.write(h)
file.write(setZlevel(0.20))
zs = np.arange(0.2, thickness+0.6, 0.2)
index = 0
#start = parge([10, 10], [120, 10], coff*5)
#file.writelines(start)
for z in zs:
    if index == 1:
        file.writelines('M106 P1 S255\n')
    if index == 0:
        file.write(setZlevel(z))
        for i in range(len(shield)):
            code = codeblock(shield[i], coff*initial_mul, feedrate_init, fastfeedrate, .0)
            file.writelines(code)
        if index < len(zs) // 2:
            if index % 2 == 0:
                for i in range(len(path_1)):
                    j = permutation_1[i]
                    code = codeblock(path_1[j], coff*initial_mul, feedrate_init, fastfeedrate, retraction)
                    file.writelines(code)
            else:
                for i in range(len(path_2)):
                    j = permutation_2[i]
                    code = codeblock(path_2[j], coff*initial_mul, feedrate_init, fastfeedrate, retraction)
                    file.writelines(code)
                    pass
        else:
            if index % 2 == 0:
                for i in range(len(path_2)):
                    j = permutation_2[i]
                    code = codeblock(path_2[j], coff*initial_mul, feedrate_init, fastfeedrate, retraction)
                    file.writelines(code)
            else:
                for i in range(len(path_1)):
                    j = permutation_1[i]
                    code = codeblock(path_1[j], coff*initial_mul, feedrate_init, fastfeedrate, retraction)
                    file.writelines(code)
                    pass
    else:
        file.write(setZlevel(z))
        for i in range(len(shield)):
            code = codeblock(shield[i], coff, feedrate, fastfeedrate, .0)
            file.writelines(code)
        if index < len(zs) // 2:
            if index % 2 == 0:
                for i in range(len(path_1)):
                    j = permutation_1[i]
                    code = codeblock(path_1[j], coff, feedrate, fastfeedrate, retraction)
                    file.writelines(code)
            else:
                for i in range(len(path_2)):
                    j = permutation_2[i]
                    code = codeblock(path_2[j], coff, feedrate, fastfeedrate, retraction)
                    file.writelines(code)
                    pass
        else:
            if index % 2 == 0:
                for i in range(len(path_2)):
                    j = permutation_2[i]
                    code = codeblock(path_2[j], coff, feedrate, fastfeedrate, retraction)
                    file.writelines(code)
            else:
                for i in range(len(path_1)):
                    j = permutation_1[i]
                    code = codeblock(path_1[j], coff, feedrate, fastfeedrate, retraction)
                    file.writelines(code)
                    pass
    index += 1
file.write(f)
file.close()