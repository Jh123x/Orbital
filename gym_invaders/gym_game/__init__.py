from gym.envs.registration import register

register(
    id='Invader-v0',
    entry_point='gym_game.envs:CustomEnv'
)
register(
    id = 'Classic-v0',
    entry_point = 'gym_game.envs:ClassicEnv'
)
