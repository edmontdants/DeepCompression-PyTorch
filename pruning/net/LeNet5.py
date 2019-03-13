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
        self.drop_rate = [0.5, 0.5]


    def forward(self, x):
        x = F.relu(self.conv1(x))
        x = F.max_pool2d(x, 2, 2)
        x = F.relu(self.conv2(x))
        x = F.max_pool2d(x, 2, 2)
        x = x.view(-1, 4 * 4 * 50)
        x = F.relu(self.fc1(x))
        x = self.fc2(x)
        return x


    def num_flat_features(self, x):
        size = x.size()[1:]
        num_features = 1
        for s in size:
            num_features *= s
        return num_features
