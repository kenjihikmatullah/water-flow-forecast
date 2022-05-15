def getflows(linkfile):
    try:
        fileobj = open(linkfile, 'r')
        lines = fileobj.readlines()
        fileobj.close()
    except:
        print('Link file open error')

    nl = len(lines)
    np = nl - 2
    flows = []

    for i in range(0, np):
        ss = lines[i + 2].split('\t')
        flows.append(ss[5])

    return flows


def getpressures(nodefile):
    try:
        fileobj = open(nodefile, 'r')
        lines = fileobj.readlines()
        fileobj.close()
    except:
        print('Node file open error')

    nl = len(lines)
    np = nl - 2
    pressures = []

    for i in range(0, np):
        ss = lines[i + 2].split('\t')
        pressures.append(ss[4])

    return pressures


def getheads(nodefile):
    try:
        fileobj = open(nodefile, 'r')
        lines = fileobj.readlines()
        fileobj.close()
    except:
        print('Node file open error')

    nl = len(lines)
    np = nl - 2
    heads = []

    for i in range(0, np):
        ss = lines[i + 2].split('\t')
        heads.append(ss[5])

    return heads


def getdemands(nodefile):
    try:
        fileobj = open(nodefile, 'r')
        lines = fileobj.readlines()
        fileobj.close()
    except:
        print('Node file open error')

    nl = len(lines)
    np = nl - 2
    demands = []

    for i in range(0, np):
        ss = lines[i + 2].split('\t')
        demands.append(ss[6].replace("\n", ""))

    return demands


def getdata(finaloutputfile):
    flows = getflows(finaloutputfile+'.links.out')
    pressures = getpressures(finaloutputfile+'.nodes.out')
    heads = getheads(finaloutputfile+'.nodes.out')
    demands = getdemands(finaloutputfile+'.nodes.out')
    return flows + pressures + heads + demands