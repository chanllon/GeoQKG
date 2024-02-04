import csv
import os.path
import networkx as nx
import os
import pandas as pd
from sklearn.preprocessing import MinMaxScaler

import Create_Graph
from tools import logic_formula

csv_file_path = "Inter-GPS/Logic_form_language.csv"

def get_csv_row_data(csv_file_path, row_number):
    try:
        with open(csv_file_path, "r", newline="") as csv_file:
            csv_reader = csv.reader(csv_file)
            rows = list(csv_reader)
            if row_number < 0 or row_number >= len(rows):
                return None
            else:

                corrected_row = [rf"{cell}" for cell in rows[row_number]]
                return corrected_row
    except FileNotFoundError:
        return None







def save_graph_to_csv(graph, graph_id, filename):
    file_exists = os.path.isfile(filename)
    existing_edges = set()
    try:
        # if file_exists:
        #
        #     with open(filename, 'r', newline='') as csvfile:
        #         reader = csv.reader(csvfile)
        #         next(reader)
        #         for row in reader:
        #             if len(row) >= 4:
        #                 source, relationship, target = row[1], row[2], row[3]
        #                 existing_edges.add((source, relationship, target))
        #             else:
        #                 print("Skipping row with insufficient columns:", source, relationship, target)


        with open(filename, 'a', newline='') as csvfile:
            writer = csv.writer(csvfile)

            if not file_exists:
                writer.writerow(['Graph_id', 'Source_node', 'Relationship', 'Target_node', 'Source_Property', 'Target_Property'])

            for edge in graph.edges(data=True):
                source, target, data = edge[0], edge[1], edge[2]
                relationship = data.get('relation', 'Unknown')
                source_property = [graph.nodes[source].get('property'), graph.nodes[source].get('sign')]
                target_property = [graph.nodes[target].get('property'), graph.nodes[target].get('sign')]


                # if (source, relationship, target) not in existing_edges:
                writer.writerow([graph_id, source, relationship, target, source_property, target_property])


                # if graph.has_edge(target, source) and (target, relationship, source) not in existing_edges:
                #     writer.writerow([groaph_id, target, relationship, source, target_property, source_property])

    except Exception as e:
        print(f"An error occurred: {e}")




def find_question_second_type(graph,graph_id,filename):
    file_exists = os.path.isfile(filename)

    try:
        with open(filename, 'a', newline='') as csvfile:
            writer = csv.writer(csvfile)
            if not file_exists:
                writer.writerow(
                ['Graph_id', 'Find_Relationship', 'Find_first_node', 'First_node_Property', 'Second_Relationship',
                 'Find_second_node', 'Second_node_Property'])
            for edge in graph.edges(data=True):
                source, target = edge[0], edge[1]
                if source == '?':
                    Find_first_node = target
                    Find_Relationship = edge[2].get('relation', 'Unknown')
                    First_node_Property = [graph.nodes[Find_first_node].get('property'),
                                           graph.nodes[Find_first_node].get('sign')]

                    for edge_in in graph.edges(data=True):
                        source_in, target_in = edge_in[0], edge_in[1]
                        if source_in == target and target_in != '?':
                            Find_second_node = target_in
                            Second_Relationship = edge_in[2].get('relation', 'Unknown')
                            Second_node_Property = [graph.nodes[Find_second_node].get('property'),
                                                    graph.nodes[Find_second_node].get('sign')]
                            writer.writerow(
                                [graph_id, Find_Relationship, Find_first_node, First_node_Property, Second_Relationship,
                                 Find_second_node, Second_node_Property])

    except Exception as e:
        print(f"An error occurred: {e}")
    return

def find_question_thrid_type(graph,graph_id,filename):
    file_exists = os.path.isfile(filename)

    try:
        with open(filename, 'a', newline='') as csvfile:
            writer = csv.writer(csvfile)
            if not file_exists:
                writer.writerow(
                ['Graph_id', 'Find_first_node', 'First_node_Property', 'Second_Relationship',
                 'Find_second_node', 'Second_node_Property','Thrid_Relationship',
                 'Find_thrid_node', 'Thrid_node_Property'])
            for edge in graph.edges(data=True):
                source, target = edge[0], edge[1]
                if source == '?':
                    Find_first_node = target
                    First_node_Property = [graph.nodes[Find_first_node].get('property'),
                                           graph.nodes[Find_first_node].get('sign')]

                    for edge_in in graph.edges(data=True):
                        source_in, target_in = edge_in[0], edge_in[1]
                        if source_in == Find_first_node and target_in != '?':
                            Find_second_node = target_in
                            Second_Relationship = edge_in[2].get('relation', 'Unknown')
                            Second_node_Property = [graph.nodes[Find_second_node].get('property'),
                                                    graph.nodes[Find_second_node].get('sign')]

                            for edge_out in graph.edges(data=True):
                                source_out, target_out = edge_out[0], edge_out[1]
                                if source_out == Find_second_node and target_out != Find_first_node:
                                    Find_third_node = target_out
                                    Third_Relationship = edge_out[2].get('relation', 'Unknown')
                                    Third_node_Property = [graph.nodes[Find_third_node].get('property'),
                                                            graph.nodes[Find_third_node].get('sign')]

                                    writer.writerow([graph_id,Find_first_node,First_node_Property, Second_Relationship,Find_second_node,
                                                     Second_node_Property,Third_Relationship,Find_third_node,Third_node_Property])
    except Exception as e:
        print(f"An error occurred: {e}")
    return

filename = 'Graph_data.csv'
filename_Com = 'Com_Graph_data.csv'
#
dif_list = []
ls = []
with open(csv_file_path, 'r') as csvfile:
    reader = csv.reader(csvfile)
    row_count = sum(1 for row in reader)
for i in range(row_count):
    row_data = get_csv_row_data(csv_file_path, i + 1)
    if row_data is not None:
        # print(row_data[0],row_data[1])
        G ,_ = Create_Graph.create_graph(row_data[0], row_data[1])
        save_graph_to_csv(G, row_data[0], filename)

        # Add logic_formula
        G_com = logic_formula.Logic_Formula_Match(G)
        save_graph_to_csv(G_com, row_data[0],filename_Com)









