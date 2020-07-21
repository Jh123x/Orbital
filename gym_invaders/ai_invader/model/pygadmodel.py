import numpy as np
import pygad.cnn as cnn
from .CNN2D import Conv2DImproved


class PyGADModel():
    def __init__(self, input_shape,num_actions):
        self.input_shape = input_shape
        self.num_actions = num_actions
        input_layer = cnn.Input2D(input_shape=input_shape)
        conv_layer1 = Conv2DImproved(num_filters=32,
                                 kernel_size=8,
                                       previous_layer=input_layer,
                                       activation_function=None)
        self.relu_layer1 = cnn.ReLU(previous_layer=conv_layer1)

        self.conv_layer2 = Conv2DImproved(num_filters=64,
                                       kernel_size=3,
                                       previous_layer=self.relu_layer1,
                                       activation_function=None)
        self.relu_layer2 = cnn.ReLU(previous_layer=self.conv_layer2)


        self.conv_layer3 = Conv2DImproved(num_filters=64,
                                       kernel_size=3,
                                       previous_layer=self.relu_layer2,
                                       activation_function=None)
        self.relu_layer3 = cnn.ReLU(previous_layer=self.conv_layer3)
        self.pooling_layer = cnn.AveragePooling2D(pool_size=2,
                                                   previous_layer=self.relu_layer3,
                                                   stride=2)

        self.flatten_layer = cnn.Flatten(previous_layer=self.pooling_layer)
        self.dense_layer1 = cnn.Dense(num_neurons=100,
                                       previous_layer=self.flatten_layer,
                                       activation_function="relu")
        self.dense_layer2 = cnn.Dense(num_neurons=num_actions,
                                       previous_layer=self.dense_layer1,
                                       activation_function="softmax")

        self.model = cnn.Model(last_layer=self.dense_layer2,
                                epochs=1,
                                learning_rate=0.01)



    # def save_model(self):

    def forward(self, stacked_frames):
        x = self.model.feed_sample(stacked_frames)
        x = np.exp(x) / sum(np.exp(x))
        return x
