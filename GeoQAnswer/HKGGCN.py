import dgl
import torch
import dgl.function as fn
import torch.nn.functional as F
import torch.nn as nn
import dgl.nn as dgl_nn

# 定义节点和边类型
user_nodes = torch.tensor([0, 1, 2, 3])
item_nodes = torch.tensor([10, 11, 12])
user_follows_edges = (torch.tensor([0, 1, 2]), torch.tensor([1, 2, 3]))
user_likes_item_edges = (torch.tensor([0, 2, 3]), torch.tensor([10, 11, 12]))
item_has_feature_edges = (torch.tensor([10, 11, 12]), torch.tensor([100, 101, 102]))

hetero_graph = dgl.heterograph({
    ('user', 'follows', 'user'): user_follows_edges,
    ('user', 'likes', 'item'): user_likes_item_edges,
    ('item', 'has', 'feature'): item_has_feature_edges,
    ('user', 'self_loop', 'user'): (user_nodes, user_nodes),
    ('item', 'self_loop', 'item'): (item_nodes, item_nodes)
})

# 添加自环边
hetero_graph['user', 'self_loop', 'user'].add_edges(user_nodes, user_nodes)
hetero_graph['item', 'self_loop', 'item'].add_edges(item_nodes, item_nodes)

user_features = torch.randn(4, in_feats)  # 创建用户节点特征，假设in_feats为您想要的特征维度
item_features = torch.randn(3, in_feats)  # 创建物品节点特征
hetero_graph.nodes['user'].data['features'] = user_features
hetero_graph.nodes['item'].data['features'] = item_features

class HeteroGNN(nn.Module):
    def __init__(self, in_feats, hidden_dim, out_dim):
        super(HeteroGNN, self).__init__()
        self.conv1 = dgl_nn.GATConv(in_feats, hidden_dim, num_heads=2)
        self.conv2 = dgl_nn.GATConv(hidden_dim * 2, out_dim, num_heads=2)

    def forward(self, g):
        # 对'follows'边类型进行处理
        follows_edge_type = ('user', 'follows', 'user')
        h1_follows = self.conv1(g[follows_edge_type], g.nodes['user'].data['features'])
        # 对'likes'边类型进行处理
        likes_edge_type = ('user', 'likes', 'item')
        h1_likes = self.conv1(g[likes_edge_type], g.nodes['user'].data['features'])
        # 合并不同边类型的输出特征
        h1 = torch.cat([h1_follows, h1_likes], dim=1)
        # 对'follows'边类型进行处理
        h2_follows = self.conv2(g[follows_edge_type], h1)
        # 对'likes'边类型进行处理
        h2_likes = self.conv2(g[likes_edge_type], h1)
        # 合并不同边类型的输出特征
        h2 = torch.cat([h2_follows, h2_likes], dim=1)
        return h2

# 创建二元分类任务的标签
active_users = [0, 2]  # 例如，用户0和用户2是高度活跃的用户
labels = torch.zeros(hetero_graph.number_of_nodes('user'))  # 初始化标签
labels[active_users] = 1  # 将高度活跃用户的标签设置为1

# 划分训练集和验证集
train_mask = torch.randint(0, 2, (hetero_graph.number_of_nodes('user'),))  # 随机划分
valid_mask = ~train_mask

# 创建模型
in_feats = 32
hidden_dim = 64
out_dim = 1
model = HeteroGNN(in_feats, hidden_dim, out_dim)

# 定义损失函数和优化器
criterion = nn.BCEWithLogitsLoss()
optimizer = torch.optim.Adam(model.parameters(), lr=0.01)

# 训练模型
model.train()
for epoch in range(100):
    logits = model(hetero_graph)
    train_logits = logits['user'][train_mask]
    train_labels = labels[train_mask]
    loss = criterion(train_logits, train_labels.float())
    optimizer.zero_grad()
    loss.backward()
    optimizer.step()
    print(f'Epoch {epoch}: loss={loss.item()}')

# 在验证集上评估模型
model.eval()
with torch.no_grad():
    logits = model(hetero_graph)
    valid_logits = logits['user'][valid_mask]
    valid_labels = labels[valid_mask]
    valid_loss = criterion(valid_logits, valid_labels.float())
    valid_preds = (valid_logits > 0.5).float()  # 使用0.5作为阈值进行二元分类
    accuracy = (valid_preds == valid_labels).float().mean()
    print(f'Validation loss{valid_loss}')
