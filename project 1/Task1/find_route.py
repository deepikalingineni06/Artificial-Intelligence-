import sys
from queue import PriorityQueue

if __name__ == '__main__':
    
    len_of_arguments = len(sys.argv)
    
    if len_of_arguments > 5:
        print('Incorrect number of arguments\n')
        sys.exit()
    
    if len_of_arguments < 4 :
        print('Incorrect number of arguments\n')
        sys.exit()    
    
    complete_network = dict()
    try:
        input = open(sys.argv[1], 'r')
        for line in input:
            temp_line = line.rstrip('\n')
            line = temp_line.rstrip('\r')
            end_str1 = 'END OF INPUT'
            if line == end_str1:
                input.close()
                break
            else:
                data = line
                data = data.split(' ')
                start = data[0]
                end = data[1]
                dist = float(data[2])
                complete_network.setdefault(start, {})[end] = dist
                complete_network.setdefault(end, {})[start] = dist
    except:
        print("File Not Found ....!")    
    
    start = sys.argv[2]
    goal = sys.argv[3]

    if start not in complete_network.keys():
        print('Starting Node is not present in given file.')
        sys.exit()
    
    if goal not in complete_network.keys():
        print('Destination node is not present in given file.')
        sys.exit()

    if len_of_arguments == 4:
        opped_noes_count = 0
        NodesGenerated = 0
        NodesExpanded = 0
        visited_nodes = set()
        queue = PriorityQueue()
        queue.put((0, [start]))
        NodesGenerated += 1
        dict_all_paths = dict()
    
        while queue:
            cost, path = queue.get()
            current = path[len(path) - 1]
            opped_noes_count = opped_noes_count + 1
            if current not in visited_nodes:
                visited_nodes.add(current)
                if current == goal:
                    NodesExpanded = NodesExpanded + 1
                    dict_all_paths['cost'] = cost
                    dict_all_paths['path'] = path
                    NodesExpanded = int((opped_noes_count+1)/2)
                    print("Nodes Popped:", opped_noes_count)
                    print('Nodes Expanded:',NodesExpanded)
                    print("Nodes Generated:", NodesGenerated)
                    print('Distance:', dict_all_paths['cost'],'km')
                    print('Route: ')
                    for i in range(len(dict_all_paths['path']) - 1):
                        start = dict_all_paths['path'][i]
                        end = dict_all_paths['path'][i + 1]
                        cost = complete_network[dict_all_paths['path'][i]][dict_all_paths['path'][i + 1]]
                        print(f'{start} to {end}, {cost} km')
                    sys.exit()
                for child in complete_network[current]:
                    temp = path[:]
                    temp.append(child)
                    NodesGenerated += 1
                    queue.put((float(cost) + float(complete_network[current][child]), temp))
            else:
              NodesExpanded +=1
            if queue.empty():
                NodesExpanded = int((opped_noes_count+1)/2)
                print("Nodes Popped:", opped_noes_count)
                print('Nodes Expanded:',NodesExpanded)
                print("Nodes Generated:", NodesGenerated)
                print("Distance: infinity \nRoute: \nNone")
                sys.exit()
        
    elif len_of_arguments == 5:
        heuristic_file = sys.argv[4]        
        heuristic = dict()
        try:
            HeuristicFile = open(heuristic_file, 'r')
            for line in HeuristicFile:
                line = line.rstrip('\n')
                line = line.rstrip('\r')
                if line == 'END OF INPUT':
                    HeuristicFile.close()
                    break
                else:
                    data = line.split(' ')
                    city = data[0]
                    hvalue = float(data[1])
                    heuristic[city] = hvalue
        except:
            print("No Input file found")        
        
        opped_noes_count = 0
        NodesGenerated = 0
        NodesExpanded = 0
        dict_all_paths = {}
        openSet = [start]
        cameFrom = {}
        gScore = {}
        fScore = {}
        
        for h in heuristic.keys():
            gScore[h] = float('inf')
            fScore[h] = float('inf')
    
        gScore[start] = 0
        fScore[start] = heuristic[start]
        fScore.values()
        while len(openSet) != 0:
            minim = float('inf')
            opped_noes_count += 1
            for node in openSet:
                if minim > fScore[node]:
                    current = node
                    minim = fScore[node]
            if current == goal:
                dict_all_paths['cost'] = 0
                dict_all_paths['path'] = []
                while current != "":
                    if current == start:
                        NodesExpanded+=1
                        dict_all_paths['path'].append(start)
                        dict_all_paths['path'].reverse()
                        NodesGenerated = NodesGenerated +1
                        NodesExpanded = int((opped_noes_count+1)/2)
                        print("Nodes Popped:", opped_noes_count)
                        print('Nodes Expanded:',NodesExpanded)
                        print("Nodes Generated:", NodesGenerated)
                        print('Distance:', dict_all_paths['cost'],'km')
                        print('Route: ')
                        for i in range(len(dict_all_paths['path']) - 1):
                            start = dict_all_paths['path'][i]
                            end = dict_all_paths['path'][i + 1]
                            cost = complete_network[dict_all_paths['path'][i]][dict_all_paths['path'][i + 1]]
                            print(f'{start} to {end}, {cost} km')                        
                        sys.exit()
                    dict_all_paths['path'].append(current)
                    dict_all_paths['cost'] += complete_network[current][cameFrom[current]]
                    current = cameFrom[current]
            openSet.remove(current)
            for neighbor in complete_network[current].keys():
                NodesGenerated += 1
                tentative_gScore = gScore[current] + complete_network[current][neighbor]
                if tentative_gScore < gScore[neighbor]:
                    cameFrom[neighbor] = current
                    gScore[neighbor] = tentative_gScore
                    fScore[neighbor] = gScore[neighbor] + heuristic[neighbor]
                    if neighbor not in openSet:
                        openSet.append(neighbor)
        NodesExpanded = int((opped_noes_count+1)/2)
        print("Nodes Popped:", opped_noes_count)
        print('Nodes Expanded:',NodesExpanded)
        print("Nodes Generated:", NodesGenerated)
        print("Distance: infinity \nRoute: \nNone")
        sys.exit()