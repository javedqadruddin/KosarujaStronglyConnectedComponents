import sys

NUM_TEST_FILES = 5

global t
t = 0
global s
s = None



def DFS_loop(graph):
    for node in graph[::-1]:
        if not node['explored']:
            s = node
            print(s['neighbors'][0])
            DFS(graph, node)
    return (0,0,0,0,0)


def DFS(graph, startNode):
    startNode['explored'] = True
    startNode['leader'] = s['num']
    for neighborNum in s['neighbors']:
        node = graph[neighborNum]
        if not node['explored']:
            DFS(graph, node)
    t+=1
    startNode['finishTime'] = t
    return


def buildGraph(f):
    graph = []
    for line in f:
        nodeNum = int(line.split()[0])
        neighborNum = int(line.split()[1])
        if nodeNum > len(graph):
            graph.append({'num':nodeNum, 'neighbors':[neighborNum], 'explored':False, 'finishTime':0, 'leader':nodeNum})
        else:
            graph[nodeNum-1]['neighbors'].append(neighborNum)
    return graph


def buildReverseGraph(graph, f):
    reverseGraph = [None] * len(graph)
    for line in f:
        nodeNum = int(line.split()[1])
        neighborNum = int(line.split()[0])
        if not reverseGraph[nodeNum-1]:
            reverseGraph[nodeNum-1] = {'num':nodeNum, 'neighbors':[neighborNum], 'explored':False, 'finishTime':0, 'leader':nodeNum}
        else:
            reverseGraph[nodeNum-1]['neighbors'].append(neighborNum)
    return reverseGraph



#test on each of the test case files
for i in range(0,NUM_TEST_FILES):
    filename = 'test' + str(i) + '.txt'
    f = open(filename)

    t = 0
    s = None


    graph = buildGraph(f)
    f.close()
    f = open(filename)
    reverseGraph = buildReverseGraph(graph, f)
    print(graph)
    print(reverseGraph)
    DFS_loop(graph)


# for line in f:
#     print(line)
