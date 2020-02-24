from Game import GameView
import numpy as np
import tflearn

class GameNN:
  def __init__(self,
               initial_games = 100, 
               test_games = 100,
               goal_steps = 100,
               lr = 1e-2,
               filename = 'game_nn.tflearn'):
        self.initial_games = initial_games
        self.test_games = test_games
        self.goal_steps = goal_steps
        self.lr = lr
        self.filename = filename      
    
# Build neural network
  def model(self): 
      network = tflearn.input_data(shape=[None, 2, 1],name= 'input')
      network = tflearn.fully_connected(network, 1, activation='linear')
      network = tflearn.regression(network,optimizer='adam', 
                             learning_rate=self.lr,
                             loss='mean_square', name='target')
     # Define model
      model = tflearn.DNN(network)
      return model

  def population(self):
    training_data = []
    for _ in range(self.initial_games):
      game = GameView()
    return training_data

  def train(self):
    training_data = self.population()
  
if __name__=="__main__":
    GameNN().train()