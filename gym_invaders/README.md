# Orbital project 2020 AI Dev Kit

## Installation

Via virtualenv
~~~
# set up python environment
apt-get install python3-venv
python3 -m venv .env
# activate python environment
source .env/bin/activate
# install all required packages
pip3 install -r requirements.txt
~~~

## Usage
### How to train your AI:
1. View the trainingDQN or trainingEvolution file, and change the given hyperparameters
2. The training loop is handled by the .train() method in the agent.
### How to load your AI:
1.To load trained AI, you can drop the files into gym_invaders/model
2.Head over to the evaluation file based on what model you train your AI in.
3.Run the eval file to see your AI in action
### How to code custom AI:
1. Inherit from TrainingAgent class and code the relevant functions for your Reinforcement Learning Algorithm of choice. 
2. Much of the incorporation to set the environment up is encoded into the functionalities of TrainingAgent class, hence allowing the user to concentrate on building the Deep Reinforcement Learning Framework.
3. For a version to incorporate into the main game after training, inherit from BaseAgent. This version is designed to perform forward propagation in the execution of the code, and output an action from the action space with the method .action(state) that takes in a state from the environment.


