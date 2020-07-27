import gym
import torch
import os

# In house dependencies
from ai_invader.agent import EvoAgentTrainer
from ai_invader.agent import EvoAgent
from ai_invader.util import load_obj,get_filename

def make_env():
    envir = gym.make("Classic-v0")
    return envir

def main():
    """"""
    #Select device to be used
    device = 'cuda' if torch.cuda.is_available() else 'cpu'

    #Get the game_actions from the env
    action_space = 6

    #Get the number of agents per generation
    num_agents = 2

    #Get the input shape (No of frames, x pixels, y pixels)
    #No of frames is to let AI to perceive motion
    input_shape = (4, 160, 120)

    #Load the model to evaluate
    ag = EvoAgent()
    ag.load_model(load_obj(os.path.join(os.path.basename(__file__),'model',get_filename()), device))
    print(ag.model)


if __name__ == "__main__":
    main()