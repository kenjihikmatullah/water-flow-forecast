#!/usr/bin/env python3

import pandas as pd
from graphviz import Digraph

csvData = pd.read_csv('../foss_varying_roughness/foss_varying_roughness.csv', header=None, index_col=0)
nodesData = pd.read_csv('../ipynb/coords.csv')
edgesData = pd.read_csv('../ipynb/edges.csv')

initialRoughness = 150   # Initial roughness value
roughnessStep = 50       # Added roughness value per-step
stepCount = 5            # Number of steps

beforeData = csvData[csvData[1] == 150]
flowBefore = beforeData[range(1, 60)]
headData = beforeData[range(97, 135)]

for s in range(1, stepCount + 1):
    afterRoughness = initialRoughness + roughnessStep*s
    afterData = csvData[csvData[1] == afterRoughness]
    flowAfter = afterData[range(1, 60)]

    flowDiff = flowAfter - flowBefore

    for i in flowDiff.index:
        g = Digraph(f'fossiron-p{i}-s{s}', filename=f'fossiron-p{i}-s{s}.gv',
                    engine='neato', format='pdf')
        g.attr(label=f'Parameters\\n\\nTarget: Pipe {i}\\nInitial roughness: {initialRoughness}\\nFinal roughness: {afterRoughness}')
        g.attr(fontsize='30')
        g.attr(lheight='4.0')

        for j in nodesData.index:
            node = nodesData.at[j, 'Node']
            head = headData.at[i, node+96]
            g.node(str(node), pos=f"{nodesData.at[j, 'X']},{nodesData.at[j, 'Y']}!", label=f"{node}", fontsize="24")

        for k in edgesData.index:
            flow = round(flowDiff.at[i, k+2], 3)
            nodeFrom = edgesData.at[k, 'From']
            nodeTo = edgesData.at[k, 'To']
            headFrom = headData.at[i, nodeFrom+96]
            headTo = headData.at[i, nodeTo+96]

            if headFrom < headTo:
                if flow < 0:
                    g.edge(str(nodeTo), str(nodeFrom), label=f"p{edgesData.at[k, 'Pipe']} ({flow})", color='red', fontsize="22")
                elif flow > 0:
                    g.edge(str(nodeTo), str(nodeFrom), label=f"p{edgesData.at[k, 'Pipe']} ({flow})", color='blue', fontsize="22")
                else:
                    g.edge(str(nodeTo), str(nodeFrom), label=f"p{edgesData.at[k, 'Pipe']} ({flow})", color='green', fontsize="22")
            else:
                if flow < 0:
                    g.edge(str(nodeFrom), str(nodeTo), label=f"p{edgesData.at[k, 'Pipe']} ({flow})", color='red', fontsize="22")
                elif flow > 0:
                    g.edge(str(nodeFrom), str(nodeTo), label=f"p{edgesData.at[k, 'Pipe']} ({flow})", color='blue', fontsize="22")
                else:
                    g.edge(str(nodeFrom), str(nodeTo), label=f"p{edgesData.at[k, 'Pipe']} ({flow})", color='green', fontsize="22")

        print(f"Generating graph for p{i}-s{s}...")
        g.render()
