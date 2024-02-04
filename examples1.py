import networkx as nx
import matplotlib.pyplot as plt
from networkx.drawing.nx_agraph import graphviz_layout
#创建知识图谱
G = nx.DiGraph()

# 添加实体节点
G.add_node("A")
G.add_node("B")
G.add_node("C")
G.add_node("D")
G.add_node("L1")
G.add_node("L2")
G.add_node("L3")
G.add_node("L4")
G.add_node("L5")
G.add_node("L6")
G.add_node("T1")
G.add_node("T2")
G.add_node("T2")
G.add_node("3")
G.add_node("14")

# 添加关系边
G.add_edge("A", "T1", relation="Com")
G.add_edge("B", "T1", relation="Com")
G.add_edge("C", "T1", relation="Com")

G.add_edge("A", "T2", relation="Com")
G.add_edge("D", "T2", relation="Com")
G.add_edge("C", "T2", relation="Com")

G.add_edge("D", "T3", relation="Com")
G.add_edge("B", "T3", relation="Com")
G.add_edge("C", "T3", relation="Com")

G.add_edge("A", "L1", relation="Com")
G.add_edge("B", "L1", relation="Com")
G.add_edge("L1", "D", relation="POnL")
G.add_edge("D", "L1", relation="POnL")

G.add_edge("C", "L2", relation="Com")
G.add_edge("A", "L2", relation="Com")
G.add_edge("C", "L3", relation="Com")
G.add_edge("B", "L3", relation="Com")
G.add_edge("L3", "L2", relation="Perp")
G.add_edge("L2", "L3", relation="Perp")

G.add_edge("C", "L4", relation="Com")
G.add_edge("D", "L4", relation="Com")
G.add_edge("L1", "L4", relation="Perp")
G.add_edge("L4", "L1", relation="Perp")

G.add_edge("A", "L5", relation="Com")
G.add_edge("D", "L5", relation="Com")
G.add_edge("L5", "3", relation="LenOf")
G.add_edge("3", "L5", relation="LenOf")

G.add_edge("B", "L6", relation="Com")
G.add_edge("D", "L6", relation="Com")
G.add_edge("L6", "14", relation="LenOf")
G.add_edge("14", "L6", relation="LenOf")

G.add_edge("L4", "?", relation="LenOf")
G.add_edge("?", "L4", relation="LenOf")


# 设置节点和边的样式
node_color = 'lightblue'
node_size = 200
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

