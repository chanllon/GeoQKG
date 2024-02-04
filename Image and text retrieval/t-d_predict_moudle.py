





#
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, TensorDataset
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

data = pd.read_csv('Sim_d-t.csv')

x = data[['Pure_Node_Similarity','Node_Similarity', 'Edge_Similarity']].values
y = data['Is_Sim'].values.astype(np.float32)

ss = StandardScaler()
xs = ss.fit_transform(x)

# print(xs.shape)

train_x, test_x, train_y, test_y = train_test_split(xs, y, test_size=0.2, random_state=42)
train_x, val_x, train_y, val_y = train_test_split(train_x, train_y, test_size=0.2, random_state=42)


train_xt = torch.from_numpy(train_x.astype(np.float32))
train_yt = torch.from_numpy(train_y.astype(np.float32))
val_xt = torch.from_numpy(val_x.astype(np.float32))
val_yt = torch.from_numpy(val_y.astype(np.float32))
test_xt = torch.from_numpy(test_x.astype(np.float32))
test_yt = torch.from_numpy(test_y.astype(np.float32))


train_data = TensorDataset(train_xt, train_yt)
val_data = TensorDataset(val_xt, val_yt)
test_data = TensorDataset(test_xt, test_yt)

train_loader = DataLoader(dataset=train_data, batch_size=16, shuffle=True)
val_loader = DataLoader(dataset=val_data, batch_size=16, shuffle=False)
test_loader = DataLoader(dataset=test_data, batch_size=16, shuffle=False)


class MLPmodel(nn.Module):
    def __init__(self):
        super(MLPmodel, self).__init__()
        self.hidden1 = nn.Linear(3, 10)
        self.active1 = nn.ReLU()
        self.hidden2 = nn.Linear(10, 10)
        self.active2 = nn.ReLU()
        self.classification = nn.Linear(10, 1)

    def forward(self, x):
        x = self.hidden1(x)
        x = self.active1(x)
        x = self.hidden2(x)
        x = self.active2(x)
        return torch.sigmoid(self.classification(x))


model = MLPmodel()

optimizer = optim.SGD(model.parameters(), lr=0.005)
loss_func = nn.BCELoss()

train_losses = []
val_losses = []
for epoch in range(20):
    model.train()
    total_train_loss = 0
    for b_x, b_y in train_loader:
        # print(b_x.shape)
        optimizer.zero_grad()
        output = model(b_x).flatten()
        loss = loss_func(output, b_y)
        loss.backward()
        optimizer.step()
        total_train_loss += loss.item()
    avg_train_loss = total_train_loss / len(train_loader)
    train_losses.append(avg_train_loss)

    model.eval()
    total_val_loss = 0
    with torch.no_grad():
        for b_x, b_y in val_loader:
            output = model(b_x).flatten()
            loss = loss_func(output, b_y)
            total_val_loss += loss.item()
    avg_val_loss = total_val_loss / len(val_loader)
    val_losses.append(avg_val_loss)

    print(f'Epoch {epoch + 1}, Training loss: {avg_train_loss:.4f}, Validation loss: {avg_val_loss:.4f}')

model.eval()
success_top_1 = 0
success_top_5 = 0
success_top_10 = 0
total_groups = 0

with torch.no_grad():
    for b_x, b_y in test_loader:
        output = model(b_x).flatten()
        top_10_indices = torch.topk(output, 10).indices
        top_5_indices = top_10_indices[:5]
        top_1_indices = top_10_indices[0]
        true_indices = (b_y == 1).nonzero(as_tuple=True)[0]
        total_groups += len(true_indices)

        for true_index in true_indices:
            if true_index in top_10_indices:
                success_top_10 += 1
            if true_index in top_5_indices:
                success_top_5 += 1
            if true_index == top_1_indices:
                success_top_1 += 1

success_rate_top_1 = success_top_1 / total_groups
success_rate_top_5 = success_top_5 / total_groups
success_rate_top_10 = success_top_10 / total_groups

print(f'Success Rate Top 1: {success_rate_top_1:.4f}')
print(f'Success Rate Top 5: {success_rate_top_5:.4f}')
print(f'Success Rate Top 10: {success_rate_top_10:.4f}')

plt.plot(range(1, len(train_losses) + 1), train_losses, label='Train Loss')
plt.plot(range(1, len(val_losses) + 1), val_losses, label='Validation Loss')
plt.xlabel('Epochs')
plt.ylabel('Loss')
plt.legend()
plt.show()

