# def calculate_complexity(G):
#     nodes = set()
#     edges = set()
#
#     for u, v in G.edges():
#         nodes.add(u)
#         nodes.add(v)
#         edges.add((u, v))
#
#     node_count = len(nodes)
#     edge_count = len(edges)
#     complexity = edge_count / node_count
#
#     return node_count, edge_count, complexity

import ast
from collections import defaultdict

import networkx as nx
import numpy as np
from sklearn.preprocessing import MinMaxScaler


def graph_complexity(graph):
    """
    计算图的复杂度
    :param graph: 输入的知识图谱图
    :return: 复杂度值
    """
    num_nodes = graph.number_of_nodes()
    num_edges = graph.number_of_edges()
    num_components = nx.number_strongly_connected_components(graph)

    return num_nodes +num_edges +num_components




def graph_difficult(graph):
    #计算图的困难度
    # graph: 输入的知识图谱图
    # :return: 困难度值

    num_components = nx.number_strongly_connected_components(graph)
    edge_counts = {}
    edge_count = 0
    node_counts ={}
    node_count = 0
    for source, target, data in graph.edges(data=True):
        if data['relation'] == 'Find':
            continue
        if data['relation'] in edge_counts:
            edge_counts[data['relation']] += 1
        else:
            edge_counts[data['relation']] = 1
    for node in graph.nodes:
        lst = graph.nodes[node]['property']
        if 'Line' in node:
            if 'Line' in node_counts:
                node_counts['Line'] += 1
            else:
                node_counts['Line'] = 1
        elif 'Angle' in node:
            if 'Angle' in node_counts:
                node_counts['Angle'] += 1
            else:
                node_counts['Angle'] = 1

        elif lst in node_counts:
            node_counts[lst] += 1
        else:
            node_counts[lst] = 1

    num_nodes = graph.number_of_nodes()
    num_edges = graph.number_of_edges()
    if num_nodes > 0:
        average_degree = num_edges / num_nodes
    else:
        average_degree = 0
    return num_components,len(edge_counts),len(node_counts),average_degree