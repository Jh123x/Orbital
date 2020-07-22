import numpy as np
import pygad
import pygad.gacnn as g
import gym
from ai_invader.util import stack_frame,preprocess_frame
from ai_invader.model import PyGADModel
import gym_game

def stack_frames(frames, state, is_new=False):
    '''
    Function combine of utility functions to preprocess the frames
    '''

    #Preprocess the frame
    frame = preprocess_frame(state, (160, 120))

    #Stack the frame
    frames = stack_frame(frames, frame, is_new)

    #Return stacked frames
    return frames

def forward(model, stacked_frames):
    x = model.feed_sample(stacked_frames)
    x = np.exp(x) / sum(np.exp(x))
    return x
    
def environment_solver(env, model):
    '''
    Returns a certain reward value/score that determines the fitness score/function of the neural network
    '''
    print('starting game')
    stacked_frames = stack_frames(None,env.reset(),True)
    r = 0
    s = 0
    done = False
    env.render(True)
    while not done:
        output_probs = forward(model,state)
        action = np.random.choice(range(num_actions), 1, p = output_probs).item()
        next_state, reward, done, info = env.step(action)
        next_state = stack_frames(state, next_state, False)
        state = next_state
        r = r+reward
    return r


def fitness_func(solution, sol_idx):
    global GACNN_instance

    #     predictions = GACNN_instance.population_networks[sol_idx].predict(data_inputs=data_inputs)
    model = GACNN_instance.population_networks[sol_idx]

    solution_fitness = environment_solver(env, model=model)

    return solution_fitness


def callback_generation(ga_instance):
    global GACNN_instance, last_fitness

    population_matrices = g.population_as_matrices(population_networks=GACNN_instance.population_networks,
                                                       population_vectors=ga_instance.population)
    GACNN_instance.update_population_trained_weights(population_trained_weights=population_matrices)

    print("Generation = {generation}".format(generation=ga_instance.generations_completed))


#Input shape of the nn
input_shape = (4, 160, 120)

#Total number of actions available
num_actions = 6

#Make the Classic screen env
env = gym.make("Classic-v0")

#Use the pyGADModel
model = PyGADModel(input_shape, num_actions).model
GACNN_instance = g.GACNN(model=model, num_solutions=5)
pop_vectors = g.population_as_vectors(population_networks=GACNN_instance.population_networks)

initial_population = pop_vectors.copy()

num_parents_mating = 4

num_generations = 10

mutation_percent_genes = 5

parent_selection_type = "sss"

crossover_type = "single_point"

mutation_type = "random"

keep_parents = 1

init_range_low = -2
init_range_high = 5

ga_instance = pygad.GA(num_generations=num_generations,
                       num_parents_mating=num_parents_mating,
                       initial_population=initial_population,
                       fitness_func=fitness_func,
                       mutation_percent_genes=mutation_percent_genes,
                       parent_selection_type=parent_selection_type,
                       crossover_type=crossover_type,
                       mutation_type=mutation_type,
                       keep_parents=keep_parents,
                       callback_generation=callback_generation)

ga_instance.run()