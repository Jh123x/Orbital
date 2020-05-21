#Code for the AI of the bot
from __future__ import print_function
import torch

#Creating random tensor
x = torch.rand(5, 3)

#Print tensor
print(x)

#Check if cuda is available
print(f"Cuda available: {torch.cuda.is_available()}")
