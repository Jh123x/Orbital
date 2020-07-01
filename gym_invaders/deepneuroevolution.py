import gym
import numpy as np
import torch
import matplotlib.pyplot as plt
import os
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
import copy
import gym
import multiprocessing as mp
from joblib import Parallel, delayed, parallel_backend
# from gym import wrappers

# In house dependencies
import gym_game
from ai_invader.util import stack_frame,preprocess_frame
from ai_invader.model import EvolutionaryAI

def init_weights(m):
    if ((type(m) == nn.Linear)| (type(m)== nn.Conv2d)):
        torch.nn.init.xavier_uniform(m.weight)
        m.bias.data.fill_(0.00)

env = gym.make("Classic-v0")

def return_random_agent(num_agents, input_shape, num_actions):
    agents = []
    global device
    for _ in range(num_agents):
        agent = EvolutionaryAI(input_shape,num_actions).to(device)
        for param in agent.parameters():
            param.requires_grad = False
        init_weights(agent)
        agents.append(agent)
    return agents

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

def run_env(agent):
    global env
    env.render(True)
    agent.eval()
    state = stack_frames(None,env.reset(),True)
    r = 0
    s = 0
    done = False

    #Plays 1 game
    while not done:
        input = torch.from_numpy(state).unsqueeze(0).type('torch.FloatTensor').to(device)
        output_probs = agent(input).detach().cpu().numpy()[0]
        action = np.random.choice(range(game_actions), 1, p = output_probs).item()
        next_state, reward, done, info = env.step(action)
        next_state = stack_frames(state, next_state, False)
        state = next_state
        r = r+reward
    return r

def run_agents(agents):
    reward_agents = []
    for agent in agents:
        r = run_env(agent)
        reward_agents.append(r)
    return reward_agents

    # for i_episode in range(start_epoch + RUNS + 1, n_episodes + RUNS + 1):
    #     RUNS += 1
    #     state = stack_frames(None, env.reset(), True)
    #     score = 0
    #     eps = epsilon_delta(RUNS)
    #     while True:
    #         action = agent.action(state, eps)
    #         next_state, reward, done, info = env.step(action)
    #         #if not score:
    #             #print(next_state)
    #         # if score:
    #             # plt.imshow(preprocess_frame(next_state,84),interpolation='none')
    #             # plt.show()
    #         score += reward
    #         next_state = stack_frames(state, next_state, False)
    #         agent.step(state, action, reward, next_state, done)
    #         state = next_state
    #         if done:
    #             break
def return_avg_score(agent, runs):
    score = 0.
    for _ in range(runs):
        score += run_agents([agent])[0]
    return score/runs

def run_agents_n_runs(agents, runs):
    avg_scores = []
    for agent in agents:
        avg_scores.append(return_avg_score(agent,runs))
    return avg_scores

def process_param(param, mutation_power):
    if (len(param.shape)==4): # Mutating weights of Conv2D
        for i in range(param.shape[0]):
            for j in range(param.shape[1]):
                for k in range(param.shape[2]):
                    for l in range(param.shape[3]):
                        param[i][j][k][l] += mutation_power*np.random.randn()

    elif len(param.shape) == 2: # Linear layer
        for i in range(param.shape[0]):
            for j in range(param.shape[1]):
                param[i][j] += mutation_power*np.random.randn()

    elif len(param.shape) == 1:
        for i in range(param.shape[0]):
            param[i] += mutation_power*np.random.randn()

def mutation(agent):
    child = copy.deepcopy((agent))
    mutation_power = 0.02
    for param in child.parameters():
        process_param(param, mutation_power)

    return child

def return_children(agents, sorted_parent_index, elite_index):

    # child_agents = list(
    #                 map(
    #                     mutation(
    #                     agents[
    #                         sorted_parent_index[
    #                             np.random.randint(
    #                                 len(sorted_parent_index))
    #                             ]
    #                         ]
    #                     ), 
    #                     range(len(agents)-1)))

    child_agents = []
    for i in range(len(agents)-1):
        selected_agent_index = sorted_parent_index[np.random.randint(len(sorted_parent_index))]
        child_agents.append(mutation(agents[selected_agent_index]))

    elite_child = add_elite(agents, sorted_parent_index,elite_index)
    child_agents.append(elite_child)
    elite_index = len(child_agents) -1 # the last child
    return child_agents, elite_index

def add_elite(agents, sorted_parent_index, elite_index= None, top_k = 10, num_runs = 5):
    candidate = sorted_parent_index[:top_k]
    if elite_index != None:
        candidate = np.append(candidate,[elite_index])
    top_score = None
    top_elite = None

    for i in candidate:
        score = return_avg_score(agents[i], runs= num_runs)
        print('Score ', i, ' is ',score,end= ' ' )
        if top_score is None:
            top_score = score
            top_elite = i
        elif score > top_score:
            top_score = score
            top_elite = i
    print("Elite selected with index", top_elite, ' score ', top_score)
    elite_agent = copy.deepcopy(agents[top_elite])
    return elite_agent

def softmax(x):
    '''Compute softmax values for each set of scores in x'''
    return np.exp(x)/np.sum(np.exp(x), axis=0)

device = 'cuda' if torch.cuda.is_available() else 'cpu'
game_actions = env.action_space.n
num_agents = 15
input_shape = (4, 84, 84)
elites = 3 #Top k
generations = 50

def survival_of_fittest(action_space, num_agents, input_dim, top_k, generations):
    elite_index = None
    torch.set_grad_enabled(False)
    agents = return_random_agent(num_agents, input_dim, action_space)
    for gen in range(generations):
        rewards = run_agents_n_runs(agents,5)

        sorted_parent_index = np.argsort(rewards)[::-1][:top_k]
        top_reward = []

        for best in sorted_parent_index:
            top_reward.append((rewards[best]))

        print("Generation ", gen, " | Mean rewards: ", np.mean(rewards), " | Mean of top 5: ",np.mean(top_reward[:5]))
        print("Top ", elites, " scores", sorted_parent_index)
        print('Rewards for top ', top_reward)

        child_agents, elite_index = return_children(agents,sorted_parent_index,elite_index)
        agents = child_agents

    #Return last agent
    return agents[-1]

#Start evolution
ag = survival_of_fittest(game_actions,num_agents,input_shape,elites,generations)
torch.save(ag, os.path.join("obj","gene_algo","survival.pth"))
