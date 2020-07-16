import numpy as np
import gym
import gym_invaders
from stable_baselines3 import PPO
from stable_baselines3.ppo import CnnPolicy

class PPOAgent():
    def __init__(self, mode):
        env = gym.make("Invader-v0")
        self.model = PPO(CnnPolicy, env, n_steps=5000, batch_size=64, n_epochs=10, gamma=0.99, gae_lambda=0.95,
                    clip_range=0.2,
                    ent_coef=0.0, vf_coef=0.5, max_grad_norm=0.5, verbose=2, tensorboard_log='./ppo')



    # Trains on a rollout batch
    def step(self, state, action, value, log_prob, reward, done, next):
        pass

    def action(self,state):
        '''Returns action, log_prob, value for given state via current policy'''
        action =

    def reset_memory(self):
        self.log_probs = []
        self.values = []
        self.states = []
        self.actions = []
        self.rewards = []
        self.masks = []
        self.entropies = []

    def learn(self, state):
        state = torch.FloatTensor(state).to(self.device)
        dist = self.actor(state)

        action = dist.sample()
        value = self.critic(state)


    # def learn(self, next_state):
    #     next_state = torch.from_numpy(next_state).unsqueeze(0).to(self.device)
    #     next_value = self.critic(next_state)
    #     returns = torch.cat(self.compute_gae(next_value)).detach()
    #     self.log_probs = torch.cat(self.log_probs).detach()
    #     self.values = torch.cat(self.values).detach()
    #     self.states = torch.cat(self.states)
    #     self.actions = torch.cat(self.actions)
    #     advantages = returns - self.values
    #
    #     for _ in range(self.ppo_epoch):
    #         for state, action, old_log_prob, return_, advantage in self.ppo_iter(returns,advantages):
    #             dist = self.actor(state)
    #             value = self.critic(state)
    #
    #             entropy = dist.entropy().mean()
    #             new_log_probs = dist.log_prob(action)
    #
    #             ratio = (new_log_probs - old_log_prob).exp()
    #             surr1 = ratio * advantage
    #             surr2 = torch.clamp(ratio,1.0-self.clip_param, 1.0 + self.clip_param) * advantage
    #
    #             actor_loss = -torch.min(surr1,surr2).mean()
    #             critic_loss = (return_ - value).pow(2).mean()
    #
    #             loss = actor_loss + 0.5 * critic_loss - 0.001 * entropy
    #             self.actor_optimizer.zero_grad()
    #             self.critic_optimizer.zero_grad()
    #             loss.backward()
    #             self.actor_optimizer.step()
    #             self.critic_optimizer.step()
    #
    #     self.reset_memory()
    def compute_gae(self, next_val):
        gae = 0
        returns = []
        values = self.values + [next_val]
        for step in reversed(range(len(self.rewards))):
            delta = self.rewards[step] + self.gamma * values[step+1]*self.masks[step] - values[step]
            gae = delta + self.gamma * self.tau * self.masks[step] * gae
            returns.insert(0,gae+values[step])
        return returns

    def compute_returns(self,next_value, rewards, mask):
        R = next_value
        returns = []
        for step in reversed(range(len(rewards))):
            R = rewards[step] + self.gamma * R * mask[step]
            returns.insert(0,R)
        return returns


    def ppo_iter(self,returns, advantages):
        memory_size = self.states.size(0)
        for _ in range(memory_size//self.batch_size):
            rand_ids = np.random.randint(0,memory_size,self.batch_size)
            yield self.states[rand_ids,:], self.actions[rand_ids],self.log_probs[rand_ids],returns[rand_ids,:]\
                    , advantages[rand_ids,:]