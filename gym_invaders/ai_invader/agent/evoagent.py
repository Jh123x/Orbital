import os
import random
import copy

import numpy as np
import torch
import torch.nn as nn
from . import TrainingAgent
from ..model import EvolutionaryAI
from .. import ReplayMemory, get_filename

class EvoAgentTrainer(TrainingAgent):
    '''
    Wrapper class for Evo Agent Trainer
    '''
    def __init__(self,input_space, action_space , num_agents, top_k, num_trials, path = 'model', mutation_power = 0.02, seed = 0, device = 'cpu',model =EvolutionaryAI,
                 gamma = 0.99,alpha = 0.0,tau = 0, batch_size = 0,  env= None, num_epochs = 0, max_step = 50000):
        '''
        EvoAgentTrainer trains Evolutionary AIs
        num_agents: Number of AIs trained per generation.
        top_k: top_k AI models to keep
        generations: Number of generations
        num_trials: Number of trials per generation for selection.
        '''
        super(EvoAgentTrainer, self).__init__(input_space, action_space, seed, device, model,
                                       gamma, alpha, tau, batch_size, max_step, env, num_epochs, path)


        self.top_k = top_k
        self.num_agents = num_agents
        self.num_trials = num_trials
        self.mutation_power = mutation_power
        self.agents = []
        self.current_agent = None
        self.filename = None

        self.elite_index = None


    def action(self,state):

        inp = torch.from_numpy(state).unsqueeze(0).type('torch.FloatTensor').to(self.device)
        output_probs = self.current_agent(inp).detach().cpu().numpy()[0]
        action = np.random.choice(range(self.action_space), 1, p=output_probs).item()
        return action

    def init_weights(self,model):
        '''
        Randomly initialise weights of the nn model
        '''
        if ((type(model) == nn.Linear) | (type(model) == nn.Conv2d)):
            torch.nn.init.xavier_uniform(model.weight)
            model.bias.data.fill_(0.00)

    def initialise_random_agent(self):
        self.agents = []

        for _ in range(self.num_agents):
            agent = self.model(self.input_shape, self.action_space).to(self.device)
            for param in agent.parameters():
                param.requires_grad = False
            self.init_weights(agent)
            self.agents.append(agent)


    def run_env(self):
        # Set Model to evaluation mode.
        self.current_agent.eval()
        state = self.stack_frames(None, self.env.reset(), True)
        r = 0
        done = False

        # Plays 1 game
        while not done:
            action = self.action(state)
            next_state, reward, done, info = self.env.step(action)
            next_state = self.stack_frames(state, next_state, False)
            state = next_state
            r = r + reward
        return r

    def run_agents(self,agents):
        reward_agents = []
        for agent in agents:
            self.current_agent = agent
            r = self.run_env()
            reward_agents.append(r)
        return reward_agents

    def return_avg_score(self,agent, runs):
        score = 0.
        for _ in range(runs):
            score += self.run_agents([agent])[0]
        return score / runs

    def run_agents_n_trials(self):
        avg_scores = []
        for agent in self.agents:
            avg_scores.append(self.return_avg_score(agent, self.num_trials))
        return avg_scores

    def process_param(self, param, mutation_power):
        if (len(param.shape) == 4):  # Mutating weights of Conv2D
            for i in range(param.shape[0]):
                for j in range(param.shape[1]):
                    for k in range(param.shape[2]):
                        for l in range(param.shape[3]):
                            param[i][j][k][l] += mutation_power * np.random.randn()

        elif len(param.shape) == 2:  # Linear layer
            for i in range(param.shape[0]):
                for j in range(param.shape[1]):
                    param[i][j] += mutation_power * np.random.randn()

        elif len(param.shape) == 1:
            for i in range(param.shape[0]):
                param[i] += mutation_power * np.random.randn()

    def mutation(self,agent):
        child = copy.deepcopy((agent))
        for param in child.parameters():
            self.process_param(param, self.mutation_power)
        return child

    def add_elite(self, sorted_parent_index, elite_index=None):
        candidate = sorted_parent_index[:self.top_k]
        if elite_index != None:
            candidate = np.append(candidate, [elite_index])
        top_score = None
        top_elite = None
        print(len(candidate))
        print(len(self.agents))
        for i in range(len(candidate)):
            score = self.return_avg_score(self.agents[i], runs=self.num_trials)
            print('Score ', i, ' is ', score, end=' ')
            if top_score is None:
                top_score = score
                top_elite = i
            elif score > top_score:
                top_score = score
                top_elite = i
            print('done ',i)
        print("Elite selected with index", top_elite, ' score ', top_score)
        elite_agent = copy.deepcopy(self.agents[top_elite])
        print('saved to :', os.path.join(self.path, self.filename))
        self.save_obj(elite_agent.state_dict(),
                      os.path.join(self.path, self.filename))
        return elite_agent

    def return_children(self, sorted_parent_index, elite_index):

        child_agents = []
        for i in range(len(self.agents) - 1):
            selected_agent_index = sorted_parent_index[np.random.randint(len(sorted_parent_index))]
            child_agents.append(self.mutation(self.agents[selected_agent_index]))

        elite_child = self.add_elite(self.agents, sorted_parent_index)
        child_agents.append(elite_child)
        elite_index = len(child_agents) - 1  # the last child
        self.elite_index = elite_index
        self.agents = child_agents

    def train(self,num_generations= 20):
        self.filename = get_filename()
        elite_index = None
        torch.set_grad_enabled(False)
        agents = self.initialise_random_agent()
        for gen in range(num_generations):
            rewards = self.run_agents_n_trials()

            sorted_parent_index = np.argsort(rewards)[::-1][:self.top_k]
            top_reward = []

            for best in sorted_parent_index:
                top_reward.append((rewards[best]))

            print("Generation ", gen, " | Mean rewards: ", np.mean(rewards), " | Mean of top 5: ",
                  np.mean(top_reward[:5]))
            print("Top ", self.top_k, " scores", sorted_parent_index)
            print('Rewards for top ', top_reward)

            self.return_children(sorted_parent_index, elite_index)

        # Return last agent
        return self.agents[-1]
