import networkx as nx
import matplotlib.pyplot as plt
from networkx.drawing.nx_agraph import graphviz_layout
#创建知识图谱例题2
G = nx.DiGraph()

#添加实体节点
G.add_node("A")
G.add_node("B")
G.add_node("L1")
G.add_node("L2")
G.add_node("L2")
G.add_node("L4")
G.add_node("L5")
G.add_node("L6")
G.add_node("32")
G.add_node("D")
G.add_node("C")
G.add_node("A1")
G.add_node("54")
G.add_node("x")
G.add_node("y")

#添加关系边
#1
G.add_edge("A", "L1", relation="Com")
G.add_edge("B", "L1", relation="Com")
G.add_edge("L1", "32", relation="LenOf")
G.add_edge("32", "L1", relation="LenOf")
#2
G.add_edge("B", "L2", relation="Com")
G.add_edge("D", "L2", relation="Com")
G.add_edge("L2", "y", relation="LenOf")
G.add_edge("y", "L2", relation="LenOf")
#3
G.add_edge("A", "A1", relation="Com")
G.add_edge("C", "A1", relation="Com")
G.add_edge("B", "A1", relation="Com")
G.add_edge("A1", "54", relation="MeaOf")
G.add_edge("54", "A1", relation="MeaOf")
#4
G.add_edge("D", "L3", relation="Comp")
G.add_edge("A", "L3", relation="Comp")
G.add_edge("L3", "x", relation="LenOf")
G.add_edge("x", "L3", relation="LenOf")
#5
G.add_edge("A", "L4", relation="Com")
G.add_edge("C", "L4", relation="Com")
G.add_edge("D", "L4",  relation="POL")
#6
G.add_edge("C", "L5", relation="Com")
G.add_edge("D", "L5", relation="Com")
G.add_edge("L2", "L5", relation="Perp")
G.add_edge("L5", "L2", relation="Perp")
#6
G.add_edge("B", "L6", relation="Com")
G.add_edge("C", "L6", relation="Com")
G.add_edge("L1", "L6", relation="LenOf")
G.add_edge("L6", "L1", relation="LenOf")

# 设置节点和边的样式
node_color = 'lightblue'
node_size = 500
edge_color = 'gray'
edge_width = 2.0
arrow_size = 20

# 将知识图谱显示为树状布局
pos = nx.nx_pydot.graphviz_layout(G, prog='dot')


# 绘制图形
labels = nx.get_edge_attributes(G, 'relation')
nx.draw_networkx_nodes(G, pos, node_color='lightblue', node_size=node_size)
nx.draw_networkx_edges(G, pos, edge_color='gray')
nx.draw_networkx_labels(G, pos)
nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)
plt.axis('off')
plt.show()

