import numpy as np 
import pygame as pg
import random 

size = 7 
area = np.ones((size, size))
area[2,2:5] = 0
area[2:6,5] = 0 
area[2:6,3] = 0 

walkable = np.argwhere(area > 0)

actions = {0:[0,1], 1:[0,-1], 2:[1,0], 3:[-1,0]}

class MazeSimple: 

    def __init__(self): 

        self.area = area 
        self.walkable = walkable

        self.pos_ini = None 
        self.pos_fin = self.walkable[np.random.randint(walkable.shape[0])]

    def reset(self): 

        pos_ini = self.pos_fin.copy()

        while np.array_equal(pos_ini, self.pos_fin): 
            inds = random.sample(range(walkable.shape[0]), 2)
            pos_ini = self.walkable[inds]


        self.pos_ini = self.walkable[inds[0]]

    def observe(self): 

        return self.pos_ini.copy()

    def step(self, ac): 

        incs = actions[ac]
        next_pos = np.clip(self.pos_ini + incs, 0, size-1) 

        is_walkable = True if self.area[next_pos[0], next_pos[1]] == 1 else False 
        

        reward = 0
        done = False 
        if is_walkable: 
            self.pos_ini = next_pos

            if np.array_equal(self.pos_ini, self.pos_fin):
                reward = 1
                done = True
        else: 
            reward = -0.1 


        infos = {}
        return self.observe(), reward, done, infos

    def render(self): 

        matrix = np.empty_like(self.area, dtype = object)
        matrix.fill('x')

        for w in self.walkable: 
            matrix[w[0], w[1]] = 'o'

        matrix[self.pos_ini[0],self.pos_ini[1]] = 'P'
        matrix[self.pos_fin[0],self.pos_fin[1]] = '.'

        print(matrix)
        print('\n\n')



m = MazeSimple()
s = m.reset()

for _ in range(2000): 

    ac = np.random.randint(4)
    ns, r ,done, infos = m.step(ac)
    if done: 
        s = m.reset()
        print('New state')
        m.render()
        input()
    
    s = ns 
    m.render()



