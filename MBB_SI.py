from svgelements import *
from svgcode.core import *

file = open('gcodes/shell_infill_simp_and_50percent.gcode', 'w')
source = '/workdir/svg/shell_infill/simp_and_50percent.svg'
feedrate = 1800
feedrate_init = 800
fastfeedrate = 8000
pathwidth = 0.5
retraction = 2.0
initial_mul = 1.0
thickness = 10
coff = calculateEcoff(pathwidth, h=0.2, lamda=1.1, D=1.75)

h, f = preset('./presets/composer_anisoprint.json')

elements = readSVG(source)
path_shell_1 = parseSubPaths(elements[0])
path_shell_2 = parseSubPaths(elements[2])
path_1 = parseSubPaths(elements[3])
path_2 = parseSubPaths(elements[4])
path_3 = parseSubPaths(elements[1])
shield = parseSubPaths(elements[5])

print(len(elements))
'''
permutation_shell_1 = range(len(path_shell_1))#sortPaths(path_shell_1)
permutation_shell_2 = range(len(path_shell_2))#sortPaths(path_shell_2)
permutation_1 = range(len(path_1))#sortPaths(path_1)
permutation_2 = range(len(path_2))#sortPaths(path_2)
permutation_3 = range(len(path_3))#sortPaths(path_3)
'''

permutation_shell_1 = sortPaths(path_shell_1)
permutation_shell_2 = sortPaths(path_shell_2)
permutation_1 = sortPaths(path_1)
permutation_2 = sortPaths(path_2)
permutation_3 = sortPaths(path_3)

file.write(h)
file.write(setZlevel(0.20))
zs = np.arange(0.2, thickness+0.6+0.8, 0.2)
index = 0
print(len(zs))

for z in zs:
    if index < 2 or index > 53:
        if index == 1:
            file.writelines('M106 P1 S255\n')
            file.write(setZlevel(z))
        if index % 2 == 0:
            for i in range(len(shield)):
                code = codeblock(shield[i], coff*initial_mul, feedrate_init, fastfeedrate, retraction)
                file.writelines(code)
            for i in range(len(path_3)):
                j = permutation_3[i]
                code = codeblock(path_3[j], coff*initial_mul, feedrate_init, fastfeedrate, retraction)
                file.writelines(code)
            for i in range(len(path_shell_1)):
                j = permutation_shell_1[i]
                code = codeblock(path_shell_1[j], coff*initial_mul, feedrate_init, fastfeedrate, retraction)
                file.writelines(code)
        else:
            for i in range(len(shield)):
                code = codeblock(shield[i], coff*initial_mul, feedrate_init, fastfeedrate, retraction)
                file.writelines(code)
            for i in range(len(path_3)):
                j = permutation_3[i]
                code = codeblock(path_3[j], coff*initial_mul, feedrate_init, fastfeedrate, retraction)
                file.writelines(code)
            for i in range(len(path_shell_2)):
                j = permutation_shell_2[i]
                code = codeblock(path_shell_2[j], coff*initial_mul, feedrate_init, fastfeedrate, retraction)
                file.writelines(code)

    elif index < len(zs) // 2:
        
        file.write(setZlevel(z))
        for i in range(len(shield)):
            code = codeblock(shield[i], coff, feedrate, fastfeedrate, retraction)
            file.writelines(code)
        for i in range(len(path_3)):
            code = codeblock(path_3[i], coff, feedrate, fastfeedrate, retraction)
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
    else:
        file.write(setZlevel(z))
        for i in range(len(shield)):
            code = codeblock(shield[i], coff, feedrate, fastfeedrate, retraction)
            file.writelines(code)
        for i in range(len(path_3)):
            code = codeblock(path_3[i], coff, feedrate, fastfeedrate, retraction)
            file.writelines(code)
        if index < len(zs) // 2:
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
        else:
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

    index += 1
file.write(f)
file.close()