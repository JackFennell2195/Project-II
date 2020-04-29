from __future__ import print_function

import csv
import numpy as np
import tflearn
    

# Load CSV file, indicate that the first column represents labels
from tflearn.data_utils import load_csv
data, labels = load_csv('dataset.csv',categorical_labels=True, n_classes=2)
          
# Build neural network 
input_data = tflearn.input_data(shape=[None, 3])
hidden_layer = tflearn.fully_connected(input_data, 32)
output = tflearn.fully_connected(hidden_layer,2,activation='softmax')

network = tflearn.regression(output)
# Define model
model = tflearn.DNN(network)

weights = model.get_weights(output.W)
with model.session.as_default():
    bias = model.get_weights(output.b)
    
model.fit(data, labels , n_epoch=10, batch_size=16, show_metric=True)

model.save("Model_1.tfl")

print("saved model to disk")


#with open('weights.csv','w',newline='') as file:
            #writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
           # writer.writerow(weights) 
           # writer.writerow(bias) 


index=0
with open('weights.csv', mode='w') as file:
    writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    for item in weights:   
        for item2 in item:   
            writer.writerow(item2.flatten())
    for item3 in bias:
        writer.writerow(item3.flatten())
    index = index+1


#print("loaded model")