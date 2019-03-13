import math
import torch.nn as nn
import torch.nn.functional as F
from pruning.function.Prune import MaskLinearModule, PruneModule


class LeNet5(PruneModule):
    def __init__(self):
        super(LeNet5, self).__init__()
        self.conv1 = nn.Conv2d(1, 20, 5, 1)
        self.conv2 = nn.Conv2d(20, 50, 5, 1)
        self.fc1 = MaskLinearModule(4 * 4 * 50, 500)
        self.fc2 = MaskLinearModule(500, 10)
        self.fc1_drop = self.compute_dropout_rate(self.fc1)
        print('==========================')
        print('fc1 dropout rate: ', self.fc1_drop)
        self.fc2_drop = self.compute_dropout_rate(self.fc2)
        print('fc2 dropout rate: ', self.fc2_drop)


    def forward(self, x):
        x = F.relu(self.conv1(x))
        x = F.max_pool2d(x, 2, 2)
        x = F.relu(self.conv2(x))
        x = F.max_pool2d(x, 2, 2)
        x = x.view(-1, 4 * 4 * 50)
        x = nn.functional.dropout(x, p=self.fc1_drop, training=True, inplace=False)
        x = F.relu(self.fc1(x))
        x = nn.functional.dropout(x, p=self.fc2_drop, training=True, inplace=False)
        x = self.fc2(x)
        return x

    def compute_dropout_rate(self, layer):
        prune_num = 0
        basic = 0
        if layer.bias is not None:
            bias_arr = (layer.bias_mask.data.cpu().numpy())
            prune_num = bias_arr.sum()
            basic = bias_arr.size
        weight_arr = (layer.weight_mask.data.cpu().numpy())
        prune_num = prune_num + weight_arr.sum()
        basic = basic + weight_arr.size
        p = 0.5 * math.sqrt(prune_num / basic)
        return p

    def num_flat_features(self, x):
        size = x.size()[1:]
        num_features = 1
        for s in size:
            num_features *= s
        return num_features
