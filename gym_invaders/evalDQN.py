#Python Modules
import os
# Neural Network Modules
import torch
#Gym Environment Dependencies
import gym

# In house dependencies
import gym_game
from ai_invader.agent import DQNAgent
from ai_invader.model import DQNCNN
from ai_invader.util import load_obj


'''
Example of training script
'''
#Retrieve Training Environment
# gym.make("Classic-v0")
# env = gym.make("Invader-v0")
def make_env():
    envir = gym.make("Invader-v0")
    return envir
def main():
    print("The size of frame is: ", make_env().observation_space.shape)
    print("No. of Actions: ", make_env().action_space.n)

    # Initialise device (Uses cuda if possible to speed up training)
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

    # Print cuda
    print('Device:', device)

    # Shape of nn
    INPUT_SHAPE = (4, 84, 84)

    # Determine rendering of GUI

    # AI vars
    ACTION_SIZE = 6
    SEED = 0
    GAMMA = 0.99  # discount factor
    BUFFER_SIZE = 10000  # replay buffer size
    BATCH_SIZE = 64  # Update batch size
    LR = 0.0001  # learning rate
    TAU = 1e-3  # for soft update of target parameters
    UPDATE_EVERY = 100  # how often to update the network
    REPLAY = 6 * BATCH_SIZE  # After which thershold replay to be started

    agent = DQNAgent(INPUT_SHAPE, ACTION_SIZE, SEED, device, DQNCNN, GAMMA, LR, TAU, BATCH_SIZE,
                     UPDATE_EVERY, REPLAY,BUFFER_SIZE, make_env, path = 'model', num_epochs = 0)
    statedict = load_obj(os.path.join(agent.get_path(), 'test.pth'), device)
    agent.load_model(statedict)
    agent.random_play(True)

#Initialise the DQNagent
if __name__ == '__main__':
    main()
