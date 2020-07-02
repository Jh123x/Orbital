import random
from collections import namedtuple, deque
import numpy as np
import torch
from scipy.special import expit
import cv2

class ReplayMemory(object):

    def __init__(self, max_size, batch_size, seed, device):
        '''Initialise a Replay Buffer
        max_size: max size of buffer
        batch_size: size of each training batch
        seed: random seed
        device: GPU or CPU
        '''
        self.buffer = deque(maxlen = max_size)
        self.batch_size = batch_size
        self.transition = namedtuple('Transition' ,field_names=('st', 'act', 'r', 'n_s' ,'d'))
        self.seed = random.seed(seed)
        self.device = device
        self.orderfunc = [lambda x: torch.from_numpy(np.array(x)).float().to(self.device), 
                            lambda x: torch.from_numpy(np.array(x)).long().to(self.device), 
                            lambda x: torch.from_numpy(np.array(x)).float().to(self.device), 
                            lambda x: torch.from_numpy(np.array(x)).float().to(self.device), 
                            lambda x: torch.from_numpy(np.array(x).astype(np.uint8)).float().to(self.device)]

    def add(self, state, action, reward, next_state, done):
        """Add a new experience to memory."""
        e = self.transition(state, action, reward, next_state, done)
        self.buffer.append(e)

    def load(self, state):
        ''' Loads Memory from Prior Training'''
        b,bat,seed = state
        self.buffer=b
        self.batch_size = bat
        self.seed = seed

    def sample(self):
        ''' Randomly sample a batch of experiences from memory'''

        #Get a sample
        exp = random.sample(self.buffer ,k = self.batch_size)
        
        #Return the sample in the correct format
        return (self.orderfunc[i](v) for i,v in enumerate(zip(*exp)))

        # print(tuple(result))
        # states = torch.from_numpy(np.array([e.st for e in exp if e is not None])).float().to(self.device)
        # actions = torch.from_numpy(np.array([e.act for e in exp if e is not None])).long().to(self.device)
        # rewards = torch.from_numpy(np.array([e.r for e in exp if e is not None])).float().to(self.device)
        # next_states = torch.from_numpy(np.array([e.n_s for e in exp if e is not None])).float().to(self.device)
        # done = torch.from_numpy(np.array([e.d for e in exp if e is not None]).astype(np.uint8)).float().to(self.device)
        # result = (states, actions, rewards, next_states, done)
        # print(result)

    def __len__(self):
        '''Return the current size of memory'''
        return len(self.buffer)

def preprocess_frame(state, output):
    ''' Preprocessing the frame from RGB -> Greyscale'''
    state = cv2.cvtColor(state, cv2.COLOR_RGB2GRAY)
    state = np.ascontiguousarray(state, dtype=np.float32) / 255
    state = cv2.resize(state,output).T
    return state

def stack_frame(stacked_frames, frame, is_new):
    """Stacking Frames.
        Params
        ======
            stacked_frames (array): Four Channel Stacked Frame
            frame: Preprocessed Frame to be added
            is_new: Is the state First
        """
    if is_new:
        stacked_frames = np.stack(arrays=[frame, frame, frame, frame])
    else:
        stacked_frames[:-1] = stacked_frames[1:]
        stacked_frames[-1] = frame

    return stacked_frames


if __name__ == '__main__':
    mem = ReplayMemory(1000, 4, 123, 'cuda')

    for _ in range(1000):
        mem.add(1,2,3,4,5)
    mem.sample()