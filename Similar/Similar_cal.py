import ast
import csv
import math
from decimal import Decimal
import networkx as nx



def cosine_sim1(list1,list2):
    # print(list1)
    # print(list2)
    if len(list1) == 0 and len(list2) == 0:
        return 1
    elif len(list1) == 0 or len(list2) == 0:
        return 0
    set1 = set(list1)
    set2 = set(list2)
    intersection = len(set1.intersection(set2))
    union = len(set1.union(set2))
    similarity = intersection / union
    # print(similarity)
    return similarity


def node_similarity(graph1, graph2):
    lst1_property = []
    lst1_shape = []
    lst1_line_angle = []
    lst1_cal = []
    lst2_property = []
    lst2_shape = []
    lst2_line_angle = []
    lst2_cal = []
    for node in graph1.nodes:
        lst = ast.literal_eval(graph1.nodes[node]['property'])
        if lst[0] == 'Value' or lst[0] == 'Point' or lst[0] == 'Generate':
            lst1_property.append(lst[0])
        elif lst[0] == 'Shape'and 'Line' not in node and 'Angle' not in node:
            lst1_shape.append(node)
        elif 'Line' in node or 'Angle' in node:
            lst1_line_angle.append(node)
        elif lst[0] == 'Calculate':
            lst1_cal.append(node)
    for node in graph2.nodes:
        lst = ast.literal_eval(graph2.nodes[node]['property'])
        if lst[0] == 'Value' or lst[0] == 'Point':
            lst2_property.append(lst[0])
        elif lst[0] == 'Shape' and 'Line' not in node and 'Angle' not in node:
            lst2_shape.append(node)
        elif 'Line' in node :
            lst2_line_angle.append(node)
        elif 'Angle' in node:
            lst2_line_angle.append(node)
        elif lst[0] == 'Calculate':
            lst2_cal.append(node)
    # Gra1_property = sorted(lst1_property)
    Gra1_shape = sorted(lst1_shape)
    Gra1_cal = sorted(lst1_cal)
    Gra1_line_angle = sorted(lst1_line_angle)
    Gra2_shape = sorted(lst2_shape)
    Gra2_cal = sorted(lst2_cal)
    Gra2_line_angle = sorted(lst2_line_angle)

    cosine_shape = cosine_sim1(Gra1_shape,Gra2_shape)
    cosine_cal = cosine_sim1(Gra1_cal,Gra2_cal)
    cosine_line_angle = cosine_sim1(Gra1_line_angle, Gra2_line_angle)
    # print(cosine_shape,cosine_cal,cosine_line_angle)
    cosine = cosine_shape +cosine_cal+ cosine_line_angle
    return cosine /3

def pure_node_similarity(graph1, graph2):
    lst1= []
    lst2 = []

    for node in graph1.nodes:
        lst1.append(node)

    for node in graph2.nodes:
        lst2.append(node)
    Gra1 = sorted(lst1)
    Gra2 = sorted(lst2)

    cosine = cosine_sim1(Gra1,Gra2)


    return cosine


def relationship_similarity(graph1, graph2):
    edge1=[]
    edge2=[]
    for source, target, data in graph1.edges(data=True):
        if data['relation'] == 'Find':
            continue
        edge1.append(data['relation'])
    for source, target, data in graph2.edges(data=True):
        if data['relation'] == 'Find':
            continue
        edge2.append(data['relation'])

    CS=cosine_sim1(edge1, edge2)

    return CS


def sim_cal(fliemame,source_id,target_id):
    source_id = str(source_id)
    target_id = str(target_id)

    with open(fliemame, 'r',encoding='latin-1') as csv_file:

        csv_reader = csv.reader(csv_file)
        G_1 = nx.DiGraph()
        G_2 = nx.DiGraph()

        for row in csv_reader:

            graph_id = row[0]
            if graph_id == source_id:

                G_1.add_node(row[1],property =row[4])
                G_1.add_node(row[3], property=row[5])

                G_1.add_edge(row[1], row[3],relation=row[2])
                continue
            elif graph_id == target_id:

                G_2.add_node(row[1], property=row[4])
                G_2.add_node(row[3], property=row[5])

                G_2.add_edge(row[1], row[3], relation=row[2])
                continue

        return G_1,G_2

def sim_cal_one(fliemame,id):
    id = str(id)

    with open(fliemame, 'r',encoding='latin-1') as csv_file:
        csv_reader = csv.reader(csv_file)
        G = nx.DiGraph()
        for row in csv_reader:

            graph_id = row[0]
            if graph_id == id:

                G.add_node(row[1],property =row[4])
                G.add_node(row[3], property=row[5])

                G.add_edge(row[1], row[3],relation=row[2])
                continue

        # print(G_1.nodes(),G_1.edges())
        # print(G_2.nodes(),G_2.edges())
        return G

def sim_cal_two(fliemame1,fliemame2,source_id,target_id):
    source_id = str(source_id)
    target_id = str(target_id)
    with open(fliemame1, 'r',encoding='latin-1') as csv_file1:

        csv_reader1 = csv.reader(csv_file1)
        G_1 = nx.DiGraph()

        is_true = 0
        for row in csv_reader1:

            graph_id1 = row[0]

            if graph_id1 == source_id:

                is_true = 1
                G_1.add_node(row[1],property =row[4])
                G_1.add_node(row[3], property=row[5])

                G_1.add_edge(row[1], row[3],relation=row[2])
                continue
            if is_true == 1 and graph_id1 != source_id:
                break
    with open(fliemame2, 'r', encoding='latin-1') as csv_file2:

        csv_reader2 = csv.reader(csv_file2)
        G_2 = nx.DiGraph()
        is_true = 0
        for row in csv_reader2:

            graph_id2 = row[0]
            if graph_id2 == target_id:
                is_true = 1

                G_2.add_node(row[1], property=row[4])
                G_2.add_node(row[3], property=row[5])

                G_2.add_edge(row[1], row[3], relation=row[2])
                continue
            if is_true == 1 and graph_id1 != target_id:
                break
        # print(G_1.nodes(),G_1.edges())
        # print(G_2.nodes(),G_2.edges())
        return G_1,G_2