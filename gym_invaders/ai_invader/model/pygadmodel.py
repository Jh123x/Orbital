import numpy as np
import pygad.cnn as cnn


class PyGADModel():
    def __init__(self, input_shape,num_actions):
        self.input_shape = input_shape
        self.num_actions = num_actions
        self.input_layer = cnn.Input2D(input_shape=input_shape)
        self.conv_layer1 = cnn.Conv2D(num_filters=32,
                                      kernel_size=8,
                                      previous_layer=self.input_layer,
                                      activation_function=None)
        self.relu_layer1 = cnn.ReLU(previous_layer=self.conv_layer1)
        self.avg_pooling1 = cnn.AveragePooling2D(pool_size=32,
                                                 previous_layer=self.relu_layer1,
                                                 stride=8)
        self.conv_layer2 = cnn.Conv2D(num_filters=32,
                                      kernel_size=4,
                                      previous_layer=self.avg_pooling1,
                                      activation_function=None)
        self.relu_layer2 = cnn.ReLU(previous_layer=self.conv_layer2)
        self.max_pooling_layer = cnn.MaxPooling2D(pool_size=4,
                                                  previous_layer=self.relu_layer2,
                                                  stride=2)
        self.conv_layer3 = cnn.Conv2D(num_filters=64,
                                      kernel_size=3,
                                      previous_layer=self.max_pooling_layer,
                                      activation_function=None)
        self.relu_layer3 = cnn.ReLU(previous_layer=self.conv_layer3)
        self.flatten = cnn.Flatten(previous_layer=self.relu_layer3)
        self.dense_layer1 = cnn.Dense(num_neurons=512,
                                      previous_layer=self.flatten,
                                      activation_function='relu')
        self.dense_layer2 = cnn.Dense(num_neurons=self.num_actions,
                                      previous_layer=self.dense_layer1,
                                      activation_function='softmax')
        self.model = cnn.Model(last_layer=self.dense_layer2,learning_rate=0.0001)
    def feature_size(self):
        return np.zeros((1,)+self.input_shape).reshape(1,-1).shape[1]

    def forward(self, stacked_frames):
        return self.model.feed_sample(stacked_frames)
