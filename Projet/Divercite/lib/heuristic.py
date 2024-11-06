from abc import abstractmethod
from typing import Literal
from game_state_divercite import GameStateDivercite
#from cachetools import FIFOCache,LFUCache,TTLCache,LRUCache,cachedmethod, Cache
import numpy as np

Method =Literal['min','max','mean','sum']

method = {
    'min':np.min,
    'max':np.max,
    'mean':np.mean,
    'sum':np.sum,
}

class Heuristic:
    
    def __init__(self,method:Method,k):
        self.h_list:list[Heuristic] = [self]
        self.method = method
        self.k = k
        

    def __call__(self, *args, **kwds):
        if len(self.h_list) ==1:
            return self.evaluate(*args)
        
        vals = [h.evaluate(*args) for h in self.h_list]
        return method[self.method](vals)
        
    @abstractmethod
    def evaluate(self,current_state:GameStateDivercite):
        ...

    @abstractmethod
    def _normalize(self,current_state:GameStateDivercite):
        ...

    def _sigmoid(self,x):
        return -1 +(2/(1+np.exp2(-x*self.k)))

    def __add__(self,other):
        if other not in self.h_list: 
            self.h_list.append(other)

