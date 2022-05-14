import constant
import shutil

def change(inputfile, outputfile, category, idname, pos, val):
    try:
        fileobj = open(inputfile, 'r')
        lines = fileobj.readlines()
        fileobj.close()
    except:
        print('Input file open error')
    try:
        fileout = open(outputfile, 'w')
    except:
        print('Output file open error ')

    incategory = False
    nl = len(lines)
    for i in range(0, nl):
        sss = lines[i].split(' ')
        ss = list(filter(lambda x: x != '', sss))

        if (incategory):
            if (len(ss) == 1):
                incategory = False
            else:
                if ((ss[0] == idname) or (idname == '*' and ss[0][0] != ';')):
                    ss[pos] = val
                    sep = "    "
                    lines[i] = sep.join(ss)

        if (ss[0].find(category) > -1):
            incategory = True
        fileout.write(lines[i])

    fileout.close()


def changeroughness2(pp, rp, r):
    infilename = constant.INPUT_FILE
    finaloutputfile = constant.OUTPUT_DIRECTORY + 'tmp-PP-' + pp + '-r-' + str(r) + '.inp'
    change(infilename, finaloutputfile, 'PIPES', pp, 5, rp + ' ')
    print(f'Created: {finaloutputfile}')
    return finaloutputfile