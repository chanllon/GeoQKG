import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, TensorDataset
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import pearsonr

data = pd.read_csv('Inter-GPS/dif.csv')

x = data[['Edge_types', 'Node_types','Average_degree']].values
y = data['Difficult'].values

ss = StandardScaler(with_mean=True, with_std=True)
xs = ss.fit_transform(x)

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

train_loader = DataLoader(dataset=train_data, batch_size=16, shuffle=True, num_workers=0)
val_loader = DataLoader(dataset=val_data, batch_size=16, shuffle=False, num_workers=0)
test_loader = DataLoader(dataset=test_data, batch_size=16, shuffle=False, num_workers=0)

class MLPmodel(nn.Module):
    def __init__(self):
        super(MLPmodel, self).__init__()
        self.hidden1 = nn.Linear(3, 10)
        self.active1 = nn.ReLU()
        self.hidden2 = nn.Linear(10, 10)
        self.active2 = nn.ReLU()
        self.regression = nn.Linear(10, 1)

    def forward(self, x):
        x = self.hidden1(x)
        x = self.active1(x)
        x = self.hidden2(x)
        x = self.active2(x)
        output = self.regression(x)
        return output

model = MLPmodel()
optimizer = optim.SGD(model.parameters(), lr=0.5)
loss_func = nn.MSELoss()

train_losses=[]
val_losses=[]
for epoch in range(50):
    model.train()
    total_train_loss=0
    for step, (b_x, b_y) in enumerate(train_loader):
        output = model(b_x).flatten()
        train_loss = loss_func(output, b_y)
        optimizer.zero_grad()
        train_loss.backward()
        optimizer.step()
        total_train_loss += train_loss.item()
    avg_train_loss=total_train_loss/len(train_loader)
    train_losses.append(avg_train_loss)

    model.eval()
    with torch.no_grad():
        total_val_loss = 0
        for step, (b_x, b_y) in enumerate(val_loader):
            output = model(b_x).flatten()
            val_loss = loss_func(output, b_y)
            total_val_loss += val_loss.item()
        avg_val_loss = total_val_loss / len(val_loader)
    val_losses.append(avg_val_loss)

    print(f'Epoch: {epoch+1}, Avg Train Loss: {avg_train_loss}, Avg Val Loss: {avg_val_loss}')

plt.plot(range(1,len(train_losses)+1),train_losses,label='Train Loss')
plt.plot(range(1,len(val_losses)+1),val_losses,label='Validation Loss')
plt.xlabel('Epochs')
plt.ylabel('Loss')
plt.legend()
plt.show()


model.eval()
with torch.no_grad():
    total_test_loss = 0
    preds = []
    actuals = []
    for step, (b_x, b_y) in enumerate(test_loader):
        output = model(b_x).flatten()
        preds.extend(output.detach().numpy())
        actuals.extend(b_y.numpy())
        test_loss = loss_func(output, b_y)
        total_test_loss += test_loss.item()
    avg_test_loss = total_test_loss / len(test_loader)
    rmse_test = np.sqrt(avg_test_loss)

corr, _ = pearsonr(preds, actuals)
print(f'RMSE on test set: {rmse_test}, Pearson correlation: {corr}')