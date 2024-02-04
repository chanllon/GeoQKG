import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, TensorDataset
from sklearn.preprocessing import StandardScaler
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import pearsonr
from tqdm import tqdm

data = pd.read_csv('Geo_sorted_file.csv')


x = data[['Pure_Node_Similarity', 'Edge_Similarity']].values
y = data['Similarity'].values
y_other = data[['Batch','sort']].values
batch = data['Batch'].values

ss = StandardScaler(with_mean=True, with_std=True)
xs = ss.fit_transform(x)

all_batches = np.unique(batch)
print('all_len:',len(all_batches))

train_batches = np.random.choice(all_batches, size=int(len(all_batches) * 0.64), replace=False)
all_batches = np.setdiff1d(all_batches, train_batches)

val_batches = np.random.choice(all_batches, size=int(len(all_batches) * 0.5), replace=False)
test_batches = np.setdiff1d(all_batches, val_batches)
print('len:',len(train_batches),len(val_batches),len(test_batches))

train_indices = np.isin(batch, train_batches)
val_indices = np.isin(batch, val_batches)
test_indices = np.isin(batch, test_batches)

train_x = xs[train_indices]
train_y = y[train_indices]
train_y_other = y_other[train_indices]

val_x = xs[val_indices]
val_y = y[val_indices]
val_y_other = y_other[val_indices]

test_x = xs[test_indices]
test_y = y[test_indices]
test_y_other = y_other[test_indices]



train_xt = torch.from_numpy(train_x.astype(np.float32))
train_yt = torch.from_numpy(train_y.astype(np.float32))
val_xt = torch.from_numpy(val_x.astype(np.float32))
val_yt = torch.from_numpy(val_y.astype(np.float32))
test_xt = torch.from_numpy(test_x.astype(np.float32))
test_yt = torch.from_numpy(test_y.astype(np.float32))
test_yt_other = torch.from_numpy(test_y_other.astype(np.float32))



train_data = TensorDataset(train_xt, train_yt)
val_data = TensorDataset(val_xt, val_yt)
test_data = TensorDataset(test_xt, test_yt, test_yt_other)


train_loader = DataLoader(dataset=train_data, batch_size=32, shuffle=True, num_workers=0)
val_loader = DataLoader(dataset=val_data, batch_size=32, shuffle=False, num_workers=0)
test_loader = DataLoader(dataset=test_data, batch_size=32, shuffle=False, num_workers=0)




class MLPmodel(nn.Module):
    def __init__(self):
        super(MLPmodel, self).__init__()
        self.hidden1 = nn.Linear(2, 10)
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
optimizer = optim.SGD(model.parameters(), lr=0.001)
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
    actuals_other = []
    for step, (b_x, b_y,b_y_other) in enumerate(test_loader):
        output = model(b_x).flatten()
        preds.extend(output.detach().numpy())
        actuals.extend(b_y.numpy())
        actuals_other.extend(b_y_other.numpy())

        test_loss = loss_func(output, b_y)
        total_test_loss += test_loss.item()
    print('pre',preds[:32])
    print('sim',actuals[:32])
    print('batch', actuals_other[:32])
    avg_test_loss = total_test_loss / len(test_loader)
    rmse_test = np.sqrt(avg_test_loss)


corr, _ = pearsonr(preds, actuals)
print(f'RMSE on test set: {rmse_test}, Pearson correlation: {corr}')

radio_1 = 1/3
radio_2 = 1/5
radio_3 = 1/2

batches = np.unique([item[0] for item in actuals_other])
count_1 = 0
count_2 = 0
count_3 = 0

for batch in tqdm(batches):
    preds_value =[]
    actuals_sort = []
    batch_count = 0
    indices = [i for i, item in enumerate(actuals_other) if item[0] == batch]
    for i in indices:
        preds_value.append(preds[i])
        actuals_sort.append(np.array([item[1] for item in actuals_other])[i])
    preds_sorted =list(np.array(preds_value).argsort().argsort() + 1)
    for j in range(len(preds_sorted)):
        if abs(preds_sorted[j] - actuals_sort[j]) <= 1:
            batch_count += 1

    if batch_count/len(indices) > radio_1:
        count_1 += 1
    if batch_count/len(indices) > radio_2:
        count_2 += 1
    if batch_count/len(indices) > radio_3:
        count_3 += 1
Sorting_consistency_1 = count_1 / len(test_batches)
Sorting_consistency_2 = count_2 / len(test_batches)
Sorting_consistency_3 = count_3 / len(test_batches)

# print('50% Sorting consistency:',Sorting_consistency_3)
print('30% Sorting consistency:',Sorting_consistency_1)
print('20% Sorting consistency:',Sorting_consistency_2)



