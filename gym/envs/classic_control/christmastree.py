"""
ChristmasTree  
"""

import logging
import gym
from gym import error, spaces, utils
from gym.utils import seeding
from gym import spaces
from gym.utils import seeding
import numpy as np

logger = logging.getLogger(__name__)

class ChristmasTreeEnv(gym.Env):

    metadata = {'render.modes': ['human']} # IS THIS CORRECT? - fair guess

    def __init__(self):

        self.irrigation = 4 # liters per week {0,1,2,...8}
        self.baseRateH = 0.038 # height growth base rate m/week (2m per year)
        self.baseRateB = 0.0096 # bushyness growth base rate m/week (0.5m radius per year)
        self.golden_ratio = 1.6
        self.height = 0.25 # REPLACED lastWeekHeight with height
        self.bushy = 0.05 #REPLACED lastWeekBushy with bushy
        self.done = False
        self.reward = 0

        self.weeks_passed = 0 # of 52
        self.state = None

        # Observation and Action spaces
        self.observation_space = spaces.Box(low=0, high=1000, shape=1) # Observing tree_ratio
        self.action_space = spaces.Discrete(9) # Action is irrigation of value 0-8


    def _seed(self, seed=None):
        self.np_random, seed = seeding.np_random(seed)
        return [seed]

    def _step(self, action):

        # get current state
        state = self.state

        # define new amount of irrigation - action
        self.irrigation = action

        # CHANGE these functions to make the system non-linear <<<
        self.funcHeightIrr = self.irrigation / 4
        self.funcBushyIrr = self.irrigation
        # weekly observation
        self.height_growth = (self.baseRateH + np.random.random(1)*0.01) * self.funcHeightIrr
        self.bushy_growth = (self.baseRateB + np.random.random(1)*0.01) * self.funcBushyIrr

        # cumulative growth
        #self.lastWeekHeight = lastWeekHeight + height_growth # DELETE IF WE DO NOT NEED THIS?
        #self.lastWeekBushy = lastWeekBushy + lastWeekBushy # DELETE IF WE DO NOT NEED THIS?
        self.height = self.height  + self.height_growth # REPLACED lastWeekHeight with height
        self.bushy = self.bushy + self.bushy_growth # REPLACED lastWeekBushy with bushy

        # metrics
        self.tree_ratio = self.height / self.bushy
        self.target_height = self.bushy * self.golden_ratio # DELETE IF WE DO NOT NEED THIS?

        # update state
        # state is self.height & self.bushy


        # reward
        self.reward = self._get_reward()

        # end episode if done is true
        if self.reward >= 52:
            done = True
        else:
            done = False

        return [self.height, self.bushy , self.tree_ratio], self.reward, done, {}


    def _irrigate(self, action):

        # DO WE NEED A PARAMETER TO CATER FOR FIRST VALUE OF irrigation?
        # 'weekly' action (related to Policy) WHAT IS THE FREQUENCY OF THIS? EACH EPISODE?
        # NEEDS INPUT!
        return self.irrigation #= action # value of the set {0,1,2,...8}

    def _get_reward(self):

        # reward is given if shape of tree is close to golden ratio
        # { = 1 if tree_ratio bw golden_ratio(+/-0.1) , else 0 ?} , max reward over year = 52, min = 0
        if self.golden_ratio + 0.1 >= self.tree_ratio >= self.golden_ratio - 0.1:
            return 1
        else:
            return 0

    def _reset(self):
        self.weeks_passed = 0
        self.state = None
        return self.state


    #def _render(self, mode='human', close=False):
    	#pass


