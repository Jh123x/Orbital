import torch

class BaseModel(torch.nn.Module):
    def __init__(self, input_shape, num_actions):
        """Cosntructor for the base model"""
        
        #Call the superclass constructor
        super(BaseModel, self).__init__()

        #Store variables used for training
        self.input_shape = input_shape
        self.num_actions = num_actions
        self.features = torch.nn.Sequential(
            torch.nn.Conv2d(input_shape[0],32,kernel_size=8,stride=4),
            torch.nn.LeakyReLU(),
            torch.nn.Conv2d(32,64,kernel_size=4,stride=2),
            torch.nn.LeakyReLU(),
            torch.nn.Conv2d(64,64,kernel_size=3,stride=1),
            torch.nn.LeakyReLU()
        )
        
    def forward(self,x):
        x = self.features(x)
        x = x.view(x.size(0),-1)
        x = self.fc(x)
        return x

    def feature_size(self):
        '''Unravels the model inputs'''
        return self.features(torch.autograd.Variable(torch.zeros(1,*self.input_shape))).view(1,-1).size(1)
