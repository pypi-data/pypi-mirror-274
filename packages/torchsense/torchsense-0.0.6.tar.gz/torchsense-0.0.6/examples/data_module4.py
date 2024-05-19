from torchsense.datasets.custom import SensorFolder
from torch.utils.data import DataLoader

input_keys = ["acc", "mix_mic"]  #, "sisnr", "speakernum", "text"]
label_keys = ["mic"]
list2 = ["PY_orbit2_RTN"]
data = SensorFolder(root="data1", params=(input_keys, label_keys))
train_set, test_set = data.train_test_split(0.5)
train_loader = DataLoader(train_set, batch_size=1, shuffle=True)
test_loader = DataLoader(test_set, batch_size=1, shuffle=False)

for i, batch in enumerate(train_loader):
    acc, mix = batch[0]
    mic = batch[1]

    print(f"Index: {i}, Acc: {acc},\nshape:{acc.shape}")

    break
