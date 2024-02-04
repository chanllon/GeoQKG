import re
import networkx as nx
import matplotlib.pyplot as plt
import sys



problem_list = ['Find']

point_list = ['G', 'C', 'Z', 'S', 'K', 'W', 'O', 'V', 'R', 'P', 'X', 'Y', 'L', 'A', 'D', 'Q', 'H', 'F', 'E', 'I', 'T', 'B', 'U', 'M', 'J', 'N','$']

shape_list = ["Point","Line", "Angle", "Triangle", "Quadrilateral", "Parallelogram", "Square", "Rectangle", "Rhombus", "Trapezoid", "Kite", "Polygon",
              "Pentagon", "Hexagon", "Heptagon", "Octagon", "Circle", "Arc", "Sector", "Shape"]

relation_list = ['PointLiesOnLine', 'PointLiesOnCircle', 'Parallel', 'Perpendicular', 'IntersectAt', 'BisectsAngle', 'Tangent', 'CircumscribedTo', 'InscribedIn',
                 'Congruent', 'Similar','IsMidpointOf', 'IsCentroidOf', 'IsIncenterOf', 'IsRadiusOf', 'IsDiameterOf', 'IsMidsegmentOf', 'IsChordOf',
                 'IsHypotenuseOf', 'IsPerpendicularBisectorOf', 'IsAltitudeOf', 'IsMedianOf', 'IsDiagonalOf']
relation_second_list = ['Equals']

calculate_first_list= ['AreaOf', 'PerimeterOf', 'RadiusOf', 'DiameterOf', 'AltitudeOf', 'CircumferenceOf', 'HypotenuseOf', 'SideOf', 'WidthOf', 'HeightOf', 'LegOf', 'BaseOf',
                       'MedianOf', 'MeasureOf', 'LengthOf','ScaleFactorOf']

calculate_second_list= ['SinOf', 'CosOf', 'TanOf', 'HalfOf',  'RatioOf', 'SumOf',  'Add', 'Mul']


delete_first_list = ['RightAngle','Right','Isosceles','Equilateral','Regular', 'Red','Blue','Green','Shaded']

delete_second_list = ['UseTheorem']


#Formal language segmentation
def split_formal(formal_language):
    # print('aaa',formal_language)
    segments = re.findall(r'\(|\)|[^,()]+', formal_language)
    segments = [segment.strip() for segment in segments if segment.strip() != '']
    return segments

##图生成
def create_graph(id,text):
    property_dict = {}
    G = nx.DiGraph()
    if type(text) == str:
        text = eval(text)

    for i in range(len(text)):
        if 'Find' in text[i]:

            element_to_move = text.pop(i)
            text.append(element_to_move)
    for element in text:
        G,property_dict = complete_graph(id,[element],G,property_dict)

    nodes_to_update = []
    sign_node = []
    target_node = None
    for node in G.nodes():
        predecessors = list(G.predecessors(node))
        successors = list(G.successors(node))
        connected_nodes = list(set(predecessors + successors))
        if len(connected_nodes) == 0:
            target_node = node
        else:

            if 'Value' in node:
                neighbors = list(G.successors(node))
                for neighbor in neighbors:
                    if G.edges[node, neighbor]['relation'] == 'Equals' and 'Generate' in neighbor:
                            node_to_update = (node, neighbor)
                            nodes_to_update.append(node_to_update)
            elif 'Generate' in node:
                neighbors = list(G.successors(node))
                for neighbor in neighbors:
                    if G.edges[node, neighbor]['relation'] == 'Equals' and 'Generate' in neighbor:
                            if neighbor not in sign_node and  node not in sign_node:
                                sign_node.append(node)
                                node_to_update=(node, neighbor)
                                nodes_to_update.insert(0,node_to_update)
    if target_node != None:
        G.remove_node(target_node)
    delete_list = []
    o = 0
    for node_list in nodes_to_update:
        node = node_list[0]
        neighbor = node_list[1]

        if node in delete_list or neighbor in delete_list:
            o += 1
            continue
        attributes = G.nodes[neighbor]
        G.nodes[node].update(attributes)
        # print('xa',neighbor,G.nodes[neighbor])
        for other_node in G.nodes:
            if other_node != node and G.has_edge(neighbor, other_node) and other_node != neighbor:
                G.add_edge(other_node, node, relation=G.edges[(neighbor, other_node)]['relation'])
                G.add_edge(node, other_node, relation=G.edges[(neighbor, other_node)]['relation'])
                # 删除相连节点
        delete_list.append(neighbor)
        G.remove_node(neighbor)

    return G,property_dict


def complete_graph(id,text,G,property_dict):
    for q in range(len(text)):
        # print('text',text[q])
        lst = split_formal(text[q])
        # print('len',lst)
        num = len(lst)
        if lst[0] in delete_second_list:
            continue
        for i in range(len(lst)-1, -1, -1):
            node_name = lst[i]
            num -= 1
            if node_name == '(' or node_name == ')':
                continue

            # Values and unknowns
            elif is_variable(node_name):
                value = property_dict.get('Value')
                if value is None:
                    # If the value does not exist, create a key-value pair with the value 1
                    value = 0
                property_dict['Value'] = value + 1
                ##Add entity
                Num_entity = 'Value' + str(value + 1)
                G.add_node(Num_entity, property='Value')
                G.add_node(Num_entity, sign=node_name)
                continue
            # PointA-Z
            elif node_name in point_list or 'radius' in node_name or 'A_' in node_name or "'" in node_name or '$' in node_name or 'point_' in node_name:
                G.add_node(node_name, property="Point")
                G.add_node(node_name, sign=None)
                continue

            ####Entities of graphics collections
            elif node_name in shape_list:
                shape_node(G, property_dict, lst, i)
                continue

            ####Entities of relationship 1 collection
            elif node_name in relation_list:
                relation_node(G, property_dict, lst, i)
                continue
            ####Entities of relationship 2 collection Equals
            elif node_name in relation_second_list:
                Equals_node(G, property_dict, lst, i)
                continue
            ###Calculate set 1
            elif node_name in calculate_first_list:
                calculate_first_node(G, property_dict, lst, i)
                continue
            ###Calculate set 2
            elif node_name in calculate_second_list:
                calculate_second_node(G, property_dict, lst, i)
                continue
            ##Delete collection 1
            elif node_name in delete_first_list:
                # Needs to be deleted from the source formal language list and the brackets removed
                # First determine the sequence number of the back bracket. The parameters of this set are all in the shape set, and there is only one parameter.
                j = i + 2
                _,j = extract_characters(lst,j)
                j += 1
                del lst[j]
                del lst[i : i + 2]
                continue

            #Delete collection 2
            elif node_name in delete_second_list:
                continue
            # Find
            elif node_name in problem_list:
                Find_node(G,property_dict,lst,i)
                continue

            else:
                try:
                    result = 10 / 0
                except ZeroDivisionError as e:
                    print(id,',',num ,"ERROR!!!")
                continue

        print(id,'Successful!')
    return G,property_dict



def extract_characters(lst, i):
    stack = []
    j = i + 2
    while lst[j] != ')':
        stack.append(lst[j])
        j += 1
    return stack,j


##Find node
def find_target_node(property_dict, G, lst, i,tar):
    if i == 'Value':
        value = property_dict.get('Value')
        node = 'Value'
    elif i == 'Generate':

        value = property_dict.get('Generate')
        node = 'Generate'
    else:
        value = property_dict.get(lst[i])
        node = lst[i]
    if value is None:
        return None

    if i != 'Value' and i != 'Generate' and ('Angle' in lst[i] or 'Arc' in lst[i]):
        while value > 0:
            if G.nodes[node + str(value)]['sign'] == tar:
                entity1 = node + str(value)
                return entity1
            value -= 1
    else:
        set1 = set(tar)
        while value > 0:
            set2 = set(G.nodes[node + str(value)]['sign'])
            if set1 == set2:
                entity1 = node + str(value)

                return entity1
            value -= 1
    if value == 0:
        return None


#Whether the node is standardized (a combination of unknown numbers and numbers)
def is_variable(input_str):

    combined_pattern = r'^([a-z]+|\d+\.\d+|\d+|Π|[a-z\dΠ\+\-\*\/\.\^]+|\d+√\d+|\√\d+)$'
    if re.match(combined_pattern, input_str):
        return True
    else:
        return False

####Graphics Collection
def shape_node(G,property_dict,lst,i):
    node_name = lst[i]
    stack, j = extract_characters(lst, i)
    entity = find_target_node(property_dict, G, lst, i, stack)
    if entity is None:
        value = property_dict.get(node_name)
        if value is None:
            value = 0
        property_dict[node_name] = value + 1

        Num_entity = node_name + str(value + 1)
        G.add_node(Num_entity, property='Shape')
        ##Establish a relationship with the parameters of this entity
        # Determine whether it is Angle(a)
        G.add_node(Num_entity, sign=stack)
        for element in stack:
            G.add_edge(element, Num_entity, relation="Com")
    else:
        Num_entity = entity
    return j,Num_entity


###Relationship collection
def relation_node(G,property_dict,lst,i):
    node_name = lst[i]
    # The first parameter of the relationship collection
    ##The first parameter of the relationship collection is the shape
    if lst[i + 2] in shape_list:
        stack1, j = extract_characters(lst, i + 2)
        j += 1

        entity1 = find_target_node(property_dict, G, lst, i + 2, stack1)
    elif lst[i + 2] in calculate_first_list:
        j,entity1 = calculate_first_node(G,property_dict,lst,i+2)
        j += 1
    ##The first parameter of the relationship collection is point
    else:
        entity1 = lst[i + 2]
        j = i + 3

    ##The second parameter of the relationship collection
    # The second parameter of the relationship collection is the shape
    if lst[j] in shape_list:
        z = j
        stack2, j = extract_characters(lst, z)
        j += 1
        entity2 = find_target_node(property_dict, G, lst, z, stack2)
    elif lst[j] in calculate_first_list:
        j,entity2 = calculate_first_node(G,property_dict,lst,j)
        j += 1
    # The second parameter of the relationship collection is the point
    else:
        while lst[j] == ')':
            j += 1
        entity2 = lst[j]
        j += 1
    G.add_edge(entity1, entity2, relation=node_name)
    G.add_edge(entity2, entity1, relation=node_name)
    return j


#Calculate 1 set
def calculate_first_node(G,property_dict,lst,i):
    node_name = lst[i]
    ##Establish a relationship with the parameters of this entity, and calculate the parameters of the relationship set as shape set and point set.
    sign_list = []
    ##First parameter
    if lst[i + 2] in shape_list:
        stack1, j = extract_characters(lst, i + 2)
        j += 1

        entity1 = find_target_node(property_dict, G, lst, i + 2, stack1)
    #The first parameter is calculated 1
    elif lst[i + 2] in calculate_first_list:
        sign_list_para = []

        j = i + 4
        if lst[j] in shape_list:
            stack1, j = extract_characters(lst, j)
            j += 1
            entity1_1 = find_target_node(property_dict, G, lst, i + 4, stack1)
        else:
            entity1_1 = lst[i + 4]
            j += 1
        j += 1
        sign_list_para.append(entity1_1)
        entity1 = find_target_node(property_dict, G, lst, 'Generate', sign_list_para)
    else:
        entity1 = find_target_node(property_dict, G, lst, 'Value',  lst[i +2])
        j = i + 3

    ## Determine whether there is a second parameter, that is, whether it is ScaleFactorOf
    ##No second parameter
    if lst[j] == ')':
        sign_list.append(entity1)
    # has a second parameter
    else:
        if lst[j] in shape_list:
            z = j
            stack2, j = extract_characters(lst, j)
            entity2 = find_target_node(property_dict, G, lst, z, stack2)
            j += 1
        elif lst[j] in calculate_first_list:
            sign_list_para_2 = []
            j += 2
            if lst[j] in shape_list:
                z = j
                stack2, j = extract_characters(lst, j)
                entity2_2 = find_target_node(property_dict, G, lst, z, stack2)
            else:
                entity2_2 = find_target_node(property_dict, G, lst, 'Value',  lst[j])
            j += 1
            sign_list_para_2.append(entity2_2)
            entity2 = find_target_node(property_dict, G, lst, 'Generate', sign_list_para_2)
        else:
            entity2 = lst[j]
            j += 1
        sign_list.append(entity1)
        sign_list.append(entity2)
        j += 1

    ## Determine whether the entity already exists
    entity = find_target_node(property_dict, G, lst, 'Generate', sign_list)
    if entity is None:

        value = property_dict.get('Generate')
        if value is None:

            value = 0
        property_dict['Generate'] = value + 1

        Num_entity = 'Generate' + str(value + 1)
        G.add_node(Num_entity, property='Generate')
        G.add_node(Num_entity, sign = sign_list)
    else:
        relation = G.edges[(entity, entity1)]['relation']
        if relation != node_name:

            value = property_dict.get('Generate')
            if value is None:

                value = 0
            property_dict['Generate'] = value + 1

            Num_entity = 'Generate' + str(value + 1)
            G.add_node(Num_entity, property='Generate')
            G.add_node(Num_entity, sign=sign_list)
        else:
            Num_entity = entity
    for entity in sign_list:

        G.add_edge(entity, Num_entity, relation=node_name)
        G.add_edge(Num_entity, entity, relation=node_name)
    return j,Num_entity


#Calculate 2 sets
def calculate_second_node(G,property_dict,lst,i):
    node_name = lst[i]
    # The parameters of this set include 1. Calculation set 1, 2. Value and 3. Shape set
    ##Judge parameters, starting with i+2, starting with each parameter j and ending with j
    j = i + 2
    entity_list = []
    while lst[j] != ')':
        # 1
        if lst[j] in shape_list:
            j,entity = shape_node(G,property_dict,lst,j)
            entity_list.append(entity)
            j += 1
        # 2
        elif is_variable(lst[j]):
            entity =  find_target_node(property_dict, G, lst, 'Value',  lst[j])
            entity_list.append(entity)
            j += 1
        # 3
        elif lst[j] in calculate_first_list:
            j,entity = calculate_first_node(G,property_dict,lst,j)
            entity_list.append(entity)
            j += 1
        # 4
        elif lst[j] in calculate_second_list:
            j,entity = calculate_second_node(G,property_dict,lst,j)
            entity_list.append(entity)
            j += 1

    ## Determine whether the entity already exists
    entity = find_target_node(property_dict, G, lst, i, entity_list)
    if entity is None:
        value = property_dict.get(node_name)
        if value is None:
            value = 0
        property_dict[node_name] = value + 1
        Num_entity = node_name + str(value + 1)
        G.add_node(Num_entity, property='Calculate')
        G.add_node(Num_entity, sign=entity_list)
    else:
        Num_entity = entity
    for entity in entity_list:
        G.add_edge(entity, Num_entity, relation='Cal')
        G.add_edge(Num_entity, entity, relation='Cal')
    return j,Num_entity


#Equals
def Equals_node(G,property_dict,lst,i):
    node_name = lst[i]
    # The parameters of Equals are all numerical values and calculate 1, calculate 2
    j = i + 2
    # The first parameter of the relationship collection
    ##The first parameter of the Equals relationship collection is the shape
    if lst[j] in shape_list:
        j, entity1 = shape_node(G, property_dict, lst, j)
        j += 1
    ##The first parameter of the Equals relationship collection is calculation 1--->Equals
    elif lst[j] in calculate_first_list:
        j, entity1 = calculate_first_node(G, property_dict, lst, j)
        j += 1
    ##The first parameter of the Equals relationship collection is a numerical value
    elif is_variable(lst[j]):
        entity1 = find_target_node(property_dict, G, lst, 'Value', lst[j])
        j += 1
    ##Equals calculates 2 when the first parameter of the relationship collection
    elif lst[j] in calculate_second_list:
        j, entity1 = calculate_second_node(G, property_dict, lst, j)
        j += 1

    ##The second parameter of the relationship collection
    #The second parameter of the Equals relationship collection is calculated 11
    if lst[j] in calculate_first_list:
        _,entity2 = calculate_first_node(G,property_dict,lst,j)

    elif lst[j] in calculate_second_list:
        _,entity2 = calculate_second_node(G,property_dict,lst,j)

    elif lst[j] in shape_list:
        _,entity2 = shape_node(G,property_dict,lst,j)

    elif is_variable(lst[j]):
        entity2 = find_target_node(property_dict, G, lst, 'Value',  lst[j])


    G.add_edge(entity1, entity2, relation=node_name)
    G.add_edge(entity2, entity1, relation=node_name)
    return


#Find
def Find_node(G,property_dict,lst,i):
    G.add_node('?', property='Generate')
    G.add_node('?', sign='Find')

    j = i + 2

    if is_variable(lst[j]):

        for node in G.nodes():
            if 'Value' in node:
                if lst[j] == G.nodes[node]['sign'] or lst[j] in G.nodes[node]['sign']:
                    entity = node
                    break

    elif lst[j] in calculate_first_list:
        _,entity = calculate_first_node(G,property_dict,lst,j)


    elif lst[j] in calculate_second_list:
        _,entity = calculate_second_node(G,property_dict,lst,j)

    G.add_edge('?', entity, relation='Find')
    G.add_edge(entity, '?', relation='Find')
    return



