#Python Modules
import os
# Neural Network Modules
import torch
#Gym Environment Dependencies
import gym
from ai_invader.util import load_obj
from ai_invader.agent import EvoAgentTrainer
from ai_invader.model import DQNCNN

def main():
    device = 'cuda' if torch.cuda.is_available() else 'cpu'

    # Get the game_actions from the env
    action_space = 6

    # Get the number of agents per generation
    num_agents = 2

    # Get the input shape (No of frames, x pixels, y pixels)
    # No of frames is to let AI to perceive motion
    input_shape = (4, 160, 120)

    # Get the Top k scores
    elites = 1

    # Number of generations to train the AI
    generations = 2

    # Start evolution (Uncomment to start training)
    ag = EvoAgentTrainer(input_shape,action_space, num_agents, elites, 1, env = make_env)
    ag.train(generations)

    # Load the model to evaluate


if __name__ == '__main__':
    main()