import sys

NUM_TEST_FILES = 5
NUM_TO_GET = 5

t = 0
s = None



def DFS_loop(graph):
    global t
    t = 0
    global s
    s = None
    #iterate through the graph in reverse order
    for nodeIndex in graph.keys()[::-1]:
        #print("node index " + str(nodeIndex))
        try:
            node = graph[nodeIndex]
            if not node['explored']:
                s = node
                DFS(graph, node)
        except:
            pass



def DFS(graph, startNode):
    startNode['explored'] = True
    startNode['leader'] = s['nodeNum']
    for neighborNum in s['neighbors']:
        try:
            node = graph[neighborNum]
            if not node['explored']:
                DFS(graph, node)
        except:
            pass

    global t
    t+=1
    startNode['finishTime'] = t
    return


def buildGraph(reverseGraph, f):
    graph = {}
    #get all the nodes from the reverse graph and put them in the forward graph in the 'magic order' in which we want to review them for the second pass
    for item in reverseGraph:
        #leader will but updated in each of the nodes in the second pass in order to have all nodes that are in the same SSC have the same 'leader' number
        if reverseGraph[item]['finishTime'] in graph:
            print('overwrite')
        graph[reverseGraph[item]['finishTime']] = {'nodeNum':reverseGraph[item]['nodeNum'],
                                    'neighbors':[],
                                    'explored':False,
                                    'finishTime':reverseGraph[item]['finishTime'],
                                    'leader':reverseGraph[item]['nodeNum']}

    #read from the file to get all the relationships in the correct order
    for line in f:
        nodeNum = int(line.split()[0])
        neighborNum = int(line.split()[1])

        #reverseGraph is still indexed by nodeNums (unlike graph, which is indexed by finishing time)
        #so, look for node in reverseGraph and lookup its finishing time in forward graph to figure out where that node is in forward graph
        #check first to make sure there is something at the position in reverseGraph.. if there isn't initialize that slot in forward graph at slot zero cuz it means that it had no outgoing connections in the reverse, so its finishing time would be 0
        if nodeNum not in reverseGraph:
            graph[1] = {'nodeNum':nodeNum,
                        'neighbors':[neighborNum],
                        'explored':False,
                        'finishTime':1,
                        'leader':nodeNum}
        else:
            #look for node in reverseGraph to find its position in forward graph by its finishing time
            nodeNum = reverseGraph[nodeNum]['finishTime']
            graph[nodeNum]['neighbors'].append(neighborNum)
    return graph

#builds a reverse graph even if the file has nodes not in order
def buildReverseGraph(f):
    #create an empty dict to contain the graph
    reverseGraph = {}
    for line in f:
        nodeNum = int(line.split()[1])
        neighborNum = int(line.split()[0])
        if nodeNum not in reverseGraph:
            reverseGraph[nodeNum] = {'nodeNum':nodeNum, 'neighbors':[neighborNum], 'explored':False, 'finishTime':0, 'leader':nodeNum}
        else:
            reverseGraph[nodeNum]['neighbors'].append(neighborNum)
    return reverseGraph



def getLargestSCCs(graph, numToGet):
    countTable = [0] * max(graph.keys())
    #get count of all possible leaders
    for index in graph:
        #print(max(graph.keys()))
        #print(graph[index]['leader'])
        countTable[graph[index]['leader']] += 1

    output = getNLargestIndices(countTable, numToGet)
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




#test on each of the test case files
for i in range(0,NUM_TEST_FILES):
    filename = 'test' + str(i) + '.txt'
    f = open(filename)
    print("file is " + filename)

    t = 0
    s = None

    #edges = getEdges(f)


    reverseGraph = buildReverseGraph(f)
    f.close()

    #print("reverse graph before dfs")
    #printGraph(reverseGraph)
    DFS_loop(reverseGraph)
    #print("reverse graph after dfs")
    #printGraph(reverseGraph)
    f = open(filename)
    graph = buildGraph(reverseGraph, f)
    #print("graph before dfs second")
    #printGraph(graph)
    #testing to make sure graph ended up in order of finishing time
    failed = False
    for item in graph:
        if graph[item]['finishTime'] != item:
            failed = True
    # if failed:
    #     print('finishing time ordering failed')
    # else:
    #     print('finishing time ordering success')


    DFS_loop(graph)
    #print("graph after dfs second")
    #printGraph(graph)
    f.close()

    print(getLargestSCCs(graph, NUM_TO_GET))
