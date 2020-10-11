"""
Created on Sat Oct  3 10:01:41 2020
@author: Emil Melfald
"""
import numpy as np 
from q_agent_v2 import Agent_v2
from random import shuffle
from random import randint

class First_to_100(): 
    def __init__(self, goal, n_players): 
        #                   between (0, 100)     (0 or 1)   (0, 105)    (0, 105)   
        #Agent must see 4 things: [round_score, self_turn, self_score, other_score]
        self.observation_space = {"n": 4, "low": np.array([0,0]+[0]*n_players), 
                                  "high": np.array([goal+7,1]+[goal+7]*n_players)}

        #Actions are either: [skip turn, throw dice]
        self.action_space = {"n": 2}
        self.actions = np.array([0, 1])

        self.WIN_REWARD = 20
        self.ROUND_PENALTY = 1
        self.THROW_PENALTY = 0
        self.WIN_SCORE = goal
        self.MAX_ROUNDS = 100
        self.players = [Agent_v2(self.observation_space["low"], self.observation_space["high"], self.action_space["n"],
                                 DISCRETE_OS_SPACE=self.WIN_SCORE+6, q_init=(-10, -5)) for _ in range(n_players)]

        self.metrics = {"Player_won": [], "Rounds_to_finish":[]}
        self.observations = {}
        self.order = {}
        for i, player in enumerate(self.players): 
            self.observations[player] = {"Score": 0, "Order": i, "Win": False}
            self.order[i] = player      
            player.update_agent()

        self.turn_score = 0  
        self.turn = 1

    def reset(self): 
        self.done_turn = False
        self.done_game = False
        self.turn_score = 0
        self.turn = 1
        self.round_count = 0
        shuffle(self.order)
        for i, player in self.order.items():  
            self.observations[player]["Score"] = 0
            self.observations[player]["Order"] = i
            self.observations[player]["Win"] = False 
        
    def round(self):
        self.round_count += 1
        for pl in self.order: 
            player = self.order[pl]
            self.turn_score = 0
            self.done_turn = False
            while (not self.done_turn) or (not self.done_game):
                player.act(self)
                if self.observations[player]["Score"] >= self.WIN_SCORE:
                    self.done_game = True
                    self.done_turn = True
                    break
            if self.done_game: 
                break

    def one_game(self): 
        self.reset() 
        self.round_count = 0
        for i in range(self.MAX_ROUNDS): 
            self.round() 
            if self.done_game or (self.round_count > self.MAX_ROUNDS): 
                for player in self.observations: 
                    if self.observations[player]["Win"]: 
                        self.metrics["Player_won"].append(player)
                break
        self.metrics["Rounds_to_finish"].append(self.round_count)


    def get_state(self, player): 
        #The state is different, depending on who is watching.
        other_players = self.players.copy() 
        other_players.remove(player)
        other_scores = []
        for pl in other_players: 
            other_scores.append(self.observations[pl]["Score"])

        return [self.turn_score, self.turn, self.observations[player]["Score"]] + other_scores

    def step(self, action, player): 
        if action == 1:
            self.turn = 1
            throw = randint(1, 7)
            if throw == 1: 
                self.turn_score = 0
                self.turn = 0 
                self.done_turn = True
                reward = -self.ROUND_PENALTY
                self.observations[player]["Win"] = False
            else: 
                self.turn_score += throw 
                if self.turn_score+self.observations[player]["Score"] >= self.WIN_SCORE: 
                    self.observations[player]["Score"] += self.turn_score
                    self.done_game = True 
                    reward = self.WIN_REWARD
                    self.observations[player]["Win"] = True
                else: 
                    reward = -self.THROW_PENALTY
                    self.observations[player]["Win"] = False
                    self.done_game = False 
        else: 
            self.turn = 0 
            self.done_turn = True
            self.observations[player]["Score"] += self.turn_score
            if self.observations[player]["Score"] >= self.WIN_SCORE:
                reward = self.WIN_REWARD
                self.done_game = True 
                self.turn = 0 
                self.observations[player]["Win"] = True

            else:
                reward = -self.ROUND_PENALTY
                self.observations[player]["Win"] = False

        new_state = self.get_state(player) 
        return new_state, reward, "Optional info"
        
        

