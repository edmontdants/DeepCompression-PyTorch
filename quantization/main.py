
import torch
import numpy as np
from sklearn.cluster import KMeans
from scipy.sparse import csr_matrix
from pruning.net.LeNet5 import LeNet5
from quantization.weight_share import share_weight
before_path = '../pruning/result/LeNet_retrain.npy'
net = LeNet5()
share_weight(net, before_path, 8, 5)