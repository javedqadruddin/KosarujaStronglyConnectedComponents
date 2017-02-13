import sys
import threading

NUM_TEST_FILES = 5
NUM_TO_GET = 5

t = 0
s = None



def DFS_loop(graph):
    #print("dfs loop run")
    global t
    t = 0
    global s
    s = None
    #iterate through the graph in reverse order
    for nodeIndex in graph.keys()[::-1]:
        #print("node index " + str(nodeIndex) + " which is " + str(graph[nodeIndex]['nodeNum']))
        node = graph[nodeIndex]
        if not node['explored']:
            s = node
            #print("searching " + str(node['nodeNum']))
            DFS(graph, node)


def DFS(graph, startNode):
    startNode['explored'] = True
    #print("assigning " + str(startNode['nodeNum']) + " the group " + str(s['nodeNum']))
    startNode['leader'] = s['nodeNum']
    for neighborNum in startNode['neighbors']:
        node = graph[neighborNum]
        if not node['explored']:
            #print("searching " + str(node['nodeNum']))
            DFS(graph, node)

    global t
    t+=1
    #print("assigning " + str(startNode['nodeNum']) + " a finish time of " + str(t))
    startNode['finishTime'] = t
    return


def buildGraph(reverseGraph, edges):
    graph = {}
    #get all the nodes from the reverse graph and put them in the forward graph in the 'magic order' in which we want to review them for the second pass
    for item in reverseGraph:
        #leader will but updated in each of the nodes in the second pass in order to have all nodes that are in the same SSC have the same 'leader' number
        graph[reverseGraph[item]['finishTime']] = {'nodeNum':reverseGraph[item]['nodeNum'],
                                    'neighbors':[],
                                    'explored':False,
                                    'finishTime':reverseGraph[item]['finishTime'],
                                    'leader':reverseGraph[item]['nodeNum']}

    for edge in edges:
        nodeNum = edge[0]
        neighborNum = edge[1]
        #find the correct mapping from the original order of the nodes to the "magic ordering" found by the first pass
        nodeNum = reverseGraph[nodeNum]['finishTime']
        neighborNum = reverseGraph[neighborNum]['finishTime']
        graph[nodeNum]['neighbors'].append(neighborNum)
    return graph

#builds a reverse graph even if the file has nodes not in order
def buildReverseGraph(edges):
    #create an empty dict to contain the graph
    reverseGraph = {}

    #fill the dict with generic node entries, one for each node in the graph
    numNodes = max([i[0] for i in edges])
    for nodeIndex in range(1,numNodes+1):
        reverseGraph[nodeIndex] = {'nodeNum':nodeIndex,
                                    'neighbors':[],
                                    'explored':False,
                                    'finishTime':0,
                                    'leader':nodeIndex}

    #link up the nodes with their edges
    for edge in edges:
        nodeNum = edge[1]
        neighborNum = edge[0]
        reverseGraph[nodeNum]['neighbors'].append(neighborNum)

    return reverseGraph



def getLargestSCCs(graph, numToGet):
    countTable = [0] * (max(graph.keys())+1)
    #get count of all possible leaders
    for index in graph:
        #print(max(graph.keys()))
        #print(graph[index]['leader'])
        countTable[graph[index]['leader']] += 1

    output = [0] * numToGet
    for out in range(0,len(output)):
        temp = 0
        for index in range(0,len(countTable)):
            if countTable[index] > countTable[temp]:
                temp = index
        output[out] = countTable[temp]
        countTable[temp] = 0
    return output



def getNLargestIndices(inputList, n):
    output = [0] * n
    for out in range(0,len(output)):
        temp = 0
        for index in range(0,len(inputList)):
            if inputList[index] > inputList[temp]:
                temp = index
        output[out] = temp
        inputList[temp] = 0
    return output


def printGraph(graph):
    for item in graph:
        print(item)
        print(graph[item])


def getEdges(f):
    edges = []
    for line in f:
        nodeNum = int(line.split()[0])
        neighborNum = int(line.split()[1])
        edges.append([nodeNum, neighborNum])
    return edges



#test on each of the test case files
#for i in range(0,NUM_TEST_FILES):
with open('scc.txt') as f:
    #get the edges from the file
    #filename = 'test' + str(i) + '.txt'
    #f = open(filename)
    #print("file is " + filename)
    edges = getEdges(f)
    #f.close()

    t = 0
    s = None
    reverseGraph = buildReverseGraph(edges)

    #print("reverse graph before dfs")
    #printGraph(reverseGraph)
    DFS_loop(reverseGraph)
    #print("reverse graph after dfs")
    #printGraph(reverseGraph)
    # f = open(filename)
    graph = buildGraph(reverseGraph, edges)
    #print("graph before dfs second")
    #printGraph(graph)
    # #testing to make sure graph ended up in order of finishing time
    # failed = False
    # for item in graph:
    #     if graph[item]['finishTime'] != item:
    #         failed = True
    # # if failed:
    # #     print('finishing time ordering failed')
    # # else:
    # #     print('finishing time ordering success')
    #
    #
    DFS_loop(graph)
    #print("graph after dfs second")
    #printGraph(graph)
    # f.close()
    #
    print(getLargestSCCs(graph, NUM_TO_GET))
