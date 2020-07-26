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
#create a local directory to store pickle files from training
PATH = os.getcwd()+'/obj'
os.makedirs('obj', exist_ok=True)
RENDER = True
'''
Example of training script
'''
#Retrieve Training Environment
# env = gym.make("Invader-v0")
def make_env():
    envir = gym.make("Classic-v0")
    return envir
#Initialise the DQNagent
if __name__ == '__main__':
    print("The size of frame is: ", make_env().observation_space.shape)
    print("No. of Actions: ", make_env().action_space.n)

    # Initialise device (Uses cuda if possible to speed up training)
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

    # Print cuda
    print('Device:', device)

    # Shape of nn
    INPUT_SHAPE = (4, 84, 84)

    # Determine rendering of GUI
    RENDER = True

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
    EPS_START = 0.99  # starting value of epsilon
    EPS_END = 0.01  # Ending value of epsilon
    EPS_DECAY = 200  # 200 #500         # Rate by which epsilon to be decayed
    RUNS = 0

    agent = DQNAgent(INPUT_SHAPE, ACTION_SIZE, SEED, device, DQNCNN, GAMMA, LR, TAU, BATCH_SIZE,
                     UPDATE_EVERY, REPLAY,BUFFER_SIZE, make_env, path = 'model', num_epochs = 0)
    statedict = load_obj(os.path.join(agent.get_path(),'test.pth'),device)
    agent.load_model(statedict)
    agent.eval()

