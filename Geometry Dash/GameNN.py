from __future__ import print_function

import numpy as np
import tflearn
    

# Load CSV file, indicate that the first column represents labels
from tflearn.data_utils import load_csv
data, labels = load_csv('dataset.csv', target_column=0,
                        categorical_labels=True, n_classes=2)

# Build neural network 
network = tflearn.input_data(shape=[None, 3])
network = tflearn.fully_connected(network,2,activation='softmax')
network = tflearn.regression(network)
# Define model
model = tflearn.DNN(network)

model.fit(data, labels, n_epoch=5, batch_size=4, show_metric=True)







