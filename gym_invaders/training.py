#Python Modules
import os
from math import exp
import sys
from collections import deque
import datetime

# Numeric Computation Module
import numpy as np

# Neural Network Modules
import torch

# Image Processing
import matplotlib.pyplot as plt

#Gym Environment Dependencies
import gym
# from gym import wrappers

# In house dependencies
import gym_game
from ai_invader.agent import DQNAgent
from ai_invader.model import DQNCNN
from ai_invader.util import stack_frame,preprocess_frame

#np.set_printoptions(threshold=sys.maxsize)

#create a local directory to store pickle files from training
PATH = os.getcwd()+'/obj'
os.makedirs('obj', exist_ok=True)
RENDER = True

#Retrieve Training Environment
# env = gym.make("Invader-v0")
env = gym.make("Classic-v0")
print("The size of frame is: ", env.observation_space.shape)
print("No. of Actions: ", env.action_space.n)
env.reset()
# plt.figure()
# plt.imshow(env.reset())
# plt.title('Original Frame')
# plt.show()

def random_play():
    """Let the ai play randomly"""
    score = 0

    #Reset environment
    env.reset()

    #Game loop
    while True:

        #Render graphics if applicable
        env.render(RENDER)

        #Sample from action space
        action = env.action_space.sample()

        #Do the action and obtain vars
        state, reward, done, _ = env.step(action)

        #Increment score
        score += reward

        #If game is done break out of loop
        if done:
            print("Your Score at end of game is: ", env.get_score())
            break

    #Close the env
    env.close()

# random_play()

def frame_preprocess(frame):
    """Plot the preprocessed frame"""
    env.reset()

    #Plot the figure
    plt.figure()

    #Show the pre processed frame
    plt.imshow(preprocess_frame(env.reset(), (0, 0, 0, 0), 84), cmap="gray")

    #Add title
    plt.title('Pre Processed image')

    #Show the plot
    plt.show()

def stack_frames(frames, state, is_new=False):
    '''
    Function combine of utility functions to preprocess the frames
    '''

    #Preprocess the frame
    frame = preprocess_frame(state, 84)

    #Stack the frame
    frames = stack_frame(frames,frame, is_new)

    #Return stacked frames
    return frames

#Initialise device (Uses cuda if possible)
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

#Print cuda
print('Device:', device)

#Shape of nn
INPUT_SHAPE = (4, 84, 84)

#Determine rendering of GUI
RENDER = False

#AI vars
ACTION_SIZE = env.action_space.n
SEED = 0
GAMMA = 0.99           # discount factor
BUFFER_SIZE = 10000    # replay buffer size
BATCH_SIZE = 64        # Update batch size
LR = 0.0001            # learning rate
TAU = 1e-3             # for soft update of target parameters
UPDATE_EVERY = 7       # how often to update the network
UPDATE_TARGET = 6*BATCH_SIZE   # After which thershold replay to be started
EPS_START = 0.99       # starting value of epsilon
EPS_END = 0.01         # Ending value of epsilon
EPS_DECAY = 200        #200 #500         # Rate by which epsilon to be decayed
RUNS = 0

#Initialise the DQNagent
agent = DQNAgent(INPUT_SHAPE, ACTION_SIZE, SEED, device, BUFFER_SIZE, BATCH_SIZE, GAMMA, LR, TAU, UPDATE_EVERY, UPDATE_TARGET, DQNCNN)

#Defining vars
start_epoch = 0

#Scores to keep track of all scores
scores = []

#Deque of max size 20 (will push out left most element when adding new ones when len=maxlen)
scores_window = deque(maxlen=20)

epsilon_delta = lambda frame_idx: EPS_END + (EPS_START-EPS_END) * exp(-1. *frame_idx/EPS_DECAY)

def save_obj(obj, name):
    '''Saves the state dictionary int obj path'''
    print('Saving..')
    torch.save(obj, os.path.join(PATH,name))
    print('Saved')

def load_obj(agent, path):
    '''Calls the agent to load the pytorch model'''
    global RUNS
    d = torch.load(path)
    RUNS = d.get('epsilon', 0)
    agent.load_model(d)

def get_filename() -> str:
    #Ask for file to be saved
    filename = input(f'Please input the filename to save: ')

    #Check if it has the correct extension
    if filename[-4:] != '.pth':
        filename += '.pth'
    return filename
        

print('Begin training')
def train(n_episodes=1000, filename = None):
    """
    n_episodes: maximum number of training episodes
    Saves Model every 100 Epochs
    """
    #Get global vars
    global RUNS, agent, scores, scores_window

    #Store current time
    t = datetime.datetime.now()
    if filename:
        loc = os.path.join(PATH, filename)
        try:
            load_obj(agent,loc)
        except FileNotFoundError as exp:
            print(f"Error:{exp}")
            filename = get_filename()
    else:
        filename = get_filename()

    #Toggles the render on
    env.render(RENDER)
    for i_episode in range(start_epoch + RUNS + 1, n_episodes + RUNS + 1):
        RUNS += 1
        state = stack_frames(None, env.reset(), True)
        score = 0
        eps = epsilon_delta(RUNS)
        while True:
            action = agent.action(state, eps)
            next_state, reward, done, info = env.step(action)
            #if not score:
                #print(next_state)
            # if score:
                # plt.imshow(preprocess_frame(next_state,84),interpolation='none')
                # plt.show()
            score += reward
            next_state = stack_frames(state, next_state, False)
            agent.step(state, action, reward, next_state, done)
            state = next_state
            if done:
                break
        scores_window.append(score) # save most recent score
        scores.append(score)        # save most recent score
        t1 = datetime.datetime.now()
        taken = t1 - t
        t = t1
        print(f'\rEpisode {i_episode}\tAverage Reward: {np.mean(scores_window)}\nGame Score:{env.get_score()}\nTime:{taken}\nEPS:{eps}')
        # if i_episode==1:
        #     # Testing code for
        #     #print(agent.model_dict(epsilon))
        save_obj(agent.model_dict(RUNS),os.path.join(PATH, filename))

        #Every 100 training
        if i_episode % 100 == 0:

            print(f"Creating plot")
            #Plot a figure
            fig = plt.figure()

            #Add a subplot
            # ax = fig.add_subplot(111)

            #Plot the graph
            plt.plot(np.arange(len(scores)), scores)

            #Add labels
            plt.xlabel('Episode #')
            plt.ylabel('Score')

            #Save the plot
            plt.savefig(f'{i_episode} plot.png')
            print(f"Plot saved")

    #Return the scores
    return scores

scores = train(5000,'sample.pth')
#load_obj(agent,path=PATH+'/model.pth')
def trained_agent(agent):
    '''
    Takes a trained agent and plays a game using the trained agent
    '''
    score = 0
    state = stack_frames(None, env.reset(), True)
    while True:
        env.render(RENDER)
        action = agent.action(state)
        next_state, reward, done, _ = env.step(action)
        score += reward
        state = stack_frames(state, next_state, False)
        if done:
            print("You Final score is:", score)
            break
    # env.close()
###
# To view Trained Agent after a checkpoint
load_obj(agent, path=os.path.join(PATH,'sample.pth'))
trained_agent(agent)

# To resume training from a previous checkpoint to train for x number of epochs
# model = torch.load(PATH+'/model.pth')
# scores = train(n_episodes = 100, load = model)

# Standard Training:
# Trains Model for 1000 games, recommended to train ~ 5000 games +
# scores = train(5000)
