import networkx as nx
import Create_Graph

first_class = ['AreaOf','PerimeterOf','CircumferenceOf','MeasureOf','Cal', 'ScaleFactorOf']
second_class = ['Equals']
third_class = ['LengthOf','RadiusOf','DiameterOf', 'SideOf','BaseOf','HeightOf','MedianOf']

def Next(Graph,node):
    edge_list = []
    for edge in Graph.edges(data=True):
        source, target = edge[0], edge[1]
        if source == node and target != '?':
            relationship = edge[2].get('relation', 'Unknown')
            edge_list.append((source,relationship,target))
            print(edge_list,edge_list[0])
    edge_top = []
    edge_end = []
    for edge in edge_list:
        if edge[1] in first_class:
            edge_top.append(edge)
        elif edge[1] in third_class:
            edge_end.append(edge)
            # edge_list.insert(len(edge_list)-1,edge)
    for edge in edge_top:
        edge_list.insert(0, edge)
    for edge in edge_end:
        edge_list.insert(len(edge_list) - 1, edge)
    return edge_list

def Area(node):
    G = nx.DiGraph()
    if 'Circle' in node :
        G.add_node('Π',property = 'Value')
        G.add_node('r**2',property = 'Value')
        G.add_node('*',property = 'Calculate')
        G.add_edge('Π','*',relation = 'Factor')
        G.add_edge('r**2', '*', relation='Factor')
        return G,'*'
    elif 'Sector'in node:
        G.add_node('Π',property = 'Value')
        G.add_node('r**2',property = 'Value')
        G.add_node('n/360', property='Value')
        G.add_node('*',property = 'Calculate')
        G.add_edge('Π','*',relation = 'Factor')
        G.add_edge('r**2', '*', relation='Factor')
        G.add_edge('n/360', '*', relation='Factor')
        return G,'*'
    elif 'Triangle' in node:
        G.add_node('1/2',property = 'Value')
        G.add_node('Base',property = 'Value')
        G.add_node('Height', property='Value')
        G.add_node('*',property = 'Calculate')
        G.add_edge('1/2','*',relation = 'Factor')
        G.add_edge('Base', '*', relation='Factor')
        G.add_edge('Height', '*', relation='Factor')
        return G,'*'
    elif 'Trapezoid' in node:
        G.add_node('1/2',property = 'Value')
        G.add_node('Base',property = 'Value')
        G.add_node('Top', property='Value')
        G.add_node('Height', property='Value')
        G.add_node('*',property = 'Calculate')
        G.add_node('+', property='Calculate')
        G.add_edge('Base', '+', relation='Addend')
        G.add_edge('Top', '+', relation='Addend')
        G.add_edge('1/2','*',relation = 'Factor')
        G.add_edge('+', '*', relation='Factor')
        G.add_edge('Height', '*', relation='Factor')
        return G,'*'
    else:
        G.add_node('Base',property = 'Value')
        G.add_node('Height', property='Value')
        G.add_node('*',property = 'Calculate')
        G.add_edge('Base', '*', relation='Factor')
        G.add_edge('Height', '*', relation='Factor')
        return G, '*'

def Perimeter(node):
    G = nx.DiGraph()
    if 'Circle' in node:
        G.add_node('Π', property='Value')
        G.add_node('r', property='Value')
        G.add_node('2', property='Value')
        G.add_node('*', property='Calculate')
        G.add_edge('Π', '*', relation='Factor')
        G.add_edge('r', '*', relation='Factor')
        G.add_edge('2', '*', relation='Factor')
        return G, '*'
    elif 'Triangle' in node:
        G.add_node('E1', property='Value')
        G.add_node('E2', property='Value')
        G.add_node('E3', property='Value')
        G.add_node('+', property='Calculate')
        G.add_edge('E1', '+', relation='Addend')
        G.add_edge('E2', '+', relation='Addend')
        G.add_edge('E3', '+', relation='Addend')
        return G, '+'
    elif 'Trapezoid' in node:
        G.add_node('2',property = 'Value')
        G.add_node('Base',property = 'Value')
        G.add_node('Top', property='Value')
        G.add_node('Hypotenuse', property='Value')
        G.add_node('*',property = 'Calculate')
        G.add_node('+', property='Calculate')
        G.add_edge('2','*',relation = 'Factor')
        G.add_edge('Hypotenuse', '*', relation='Factor')
        G.add_edge('*', '+', relation='Addend')
        G.add_edge('Base', '+', relation='Addend')
        G.add_edge('Top', '+', relation='Addend')
        return G,'+'
    elif 'Sector' in node:
        G.add_node('Π', property='Value')
        G.add_node('n/360', property='Value')
        G.add_node('d', property='Value')
        G.add_node('*', property='Calculate')
        G.add_node('+', property='Calculate')
        G.add_edge('Π', '*', relation='Factor')
        G.add_edge('r', '*', relation='Factor')
        G.add_edge('n/360', '*', relation='Factor')
        G.add_edge('*', '+', relation='Addend')
        G.add_edge('d', '+', relation='Addend')
        return G, '+'
    else:
        G.add_node('E1', property='Value')
        G.add_node('E2', property='Value')
        G.add_node('E3', property='Value')
        G.add_node('En', property='Value')
        G.add_node('+', property='Calculate')
        G.add_edge('E1', '+', relation='Addend')
        G.add_edge('E2', '+', relation='Addend')
        G.add_edge('E3', '+', relation='Addend')
        G.add_edge('En', '+', relation='Addend')
        return G, '+'

def Calculate(Graph,node):
    G = nx.DiGraph()
    if 'SinOf' in node or 'CosOf' in node or 'TanOf' in node:
        G.add_node(node, property='Value')
        G.add_node('angle', property='Value')
        G.add_node('*', property='Calculate')
        G.add_edge(node, '*', relation='Factor')
        G.add_edge('angle', '*', relation='Factor')
        return G, '*'
    elif 'RatioOf' in node or 'Add' in node:
        ###FIND NEXT
        edges = Next(Graph, node)
        next_node = edges[0][2]
        if 'SinOf' in next_node or 'CosOf' in next_node or 'TanOf' in next_node:
            G,node = Calculate(Graph, next_node)
            return G,node
        elif 'Value' in next_node:
            edges = Next(Graph, next_node)
            relation = edges[0][1]
            next_node = edges[0][2]
            if relation == 'MeasureOf':
                G,node = Angle(Graph,next_node)
            elif relation == 'AreaOf':
                G, node = Area(Graph, next_node)
            return G,node
        else:
            return  None,None

def Angle(node):
    G = nx.DiGraph()
    if 'Arc'in node:
        G.add_node('Π', property='Value')
        G.add_node('r', property='Value')
        G.add_node('l', property='Value')
        G.add_node('180', property='Value')
        G.add_node('*1', property='Calculate')
        G.add_node('*2', property='Calculate')
        G.add_node('/', property='Calculate')
        G.add_edge('Π', '*1', relation='Factor')
        G.add_edge('r', '*1', relation='Factor')
        G.add_edge('l', '*2', relation='Factor')
        G.add_edge('180', '*2', relation='Factor')
        G.add_edge('*1', '/', relation='Divisor')
        G.add_edge('*2', '/', relation='Dividend')
        return G,'/'
    elif 'Angle' in node:
        G.add_node('A1',property = 'Value')
        G.add_node('A2',property = 'Value')
        G.add_node('180', property='Value')
        G.add_node('+',property = 'Calculate')
        G.add_node('-', property='Calculate')
        G.add_edge('A1','+',relation = 'Addend')
        G.add_edge('A2', '+', relation='Addend')
        G.add_edge('+', '-', relation='Subtrahend')
        G.add_edge('180', '-', relation='Minuend')
        return G,'-'

def Equals(Graph,node):
    for edge in Graph.edges(data=True):
        source, target = edge[0], edge[1]
        if source == node and Create_Graph.is_variable(source) and Create_Graph.is_variable(target):
            G = nx.DiGraph()
            G.add_node(source,property='Value')
            G.add_node(target, property='Value')
            G.add_node('=', property='Calculate')
            G.add_edge(source, '=', relation='Equation')
            G.add_edge(target, '=', relation='Equation')
            return G,'='
        else:
            return None,None

def Logic_Formula_Match(Graph):
    for edge in Graph.edges(data=True):
        n = 0
        source, target = edge[0], edge[1]
        if source == '?':
            neighbors = list(Graph.successors(target))
            neighbor = neighbors[n]
            if n < len(neighbors) and neighbor == '?':
                n += 1
                neighbor = neighbors[n]
            relation = Graph.edges[target, neighbor]['relation']
            if relation == 'AreaOf' or relation == 'ScaleFactorOf':
                Slove_G,Slove_node = Area(neighbor)
            elif relation == 'PerimeterOf' or relation == 'CircumferenceOf':
                Slove_G, Slove_node = Perimeter(neighbor)
            elif relation == 'MeasureOf':
                Slove_G, Slove_node = Angle(neighbor)
            elif relation == 'Cal':
                Slove_G, Slove_node = Calculate(Graph,target)
            elif relation == 'Equals':
                Slove_G, Slove_node = Equals(Graph,target)

            else:Slove_G, Slove_node = None,None


    if Slove_G == None:
        print('None')
        return Graph
    for edge in Slove_G.edges(data=True):
        source, target = edge[0], edge[1]
        relationship = edge[2].get('relation', 'Unknown')
        source_property = Slove_G.nodes[source].get('property')
        target_property = Slove_G.nodes[target].get('property')
        Graph.add_node(source,property = source_property)
        Graph.add_node(target,property = target_property)
        Graph.add_edge(source,target,relation = relationship)
    Graph.add_edge(Slove_node, '?', relation='Slove')
    print('Com Successful!')
    return Graph