import networkx as nx
import pandas as pd
import random
from collections import defaultdict

class Triest:
    def __init__(self,M):
        self._M = M     # max buffer size
        self._t = 0     # timestamp
        self._S = []    # Buffer
        self._neighborhood = defaultdict(set)
        self._globalT = 0       # Global Triangle number estimation
        self._localT = {}       # Local Triangle number estimation
        

    def add_edge(self,u,v):
        '''
        Add an edge to buffer S and then update the neighborhood
        '''

        self._S.append((u,v))
        self.update_neighborhood('+',u,v)

    def remove_random_edge(self):
        '''
        Pick a random edge from the buffer S and remove it. Then update the neighborhood
        '''

        rand_choice = random.randint(0,len(self._S)-1)
        u_dash,v_dash = self._S.pop(rand_choice)
        self.update_neighborhood('-',u_dash,v_dash)
        return u_dash, v_dash

    def find_common_neighborhood(self,u,v):
        '''
        Find common neighborhood(if any) between Nodes u,v
        '''

        if u in self._neighborhood and v in self._neighborhood:
            return self._neighborhood[u].intersection(self._neighborhood[v])
        else:
            return None

    def update_neighborhood(self,op,u,v):
        '''
        Update the neighborhood dictionary after addition/removal of u,v edge
        '''

        if op == '+':
            self._neighborhood[u].add(v)
            self._neighborhood[v].add(u)
        elif op == '-':
            try:
                self._neighborhood[u].remove(v)
                self._neighborhood[v].remove(u)
            except:
                pass
            
            # check if node has any edges left or else remove it
            if not self._neighborhood[u]:
                self._neighborhood.pop(u)
            if not self._neighborhood[v]:
                self._neighborhood.pop(v)
    

    def sample_edge(self, u, v):
        '''
        Check whether given edge can be added to the buffer S
        if self._t <= self._M then YES
        if self._t > self._M then flip coin to decide 
        '''

        if self._t <= self._M:
            return True
        elif self.flip_biased_coin():
            u_rmv, v_rmv = self.remove_random_edge()
            self.update_counters(u_rmv,v_rmv,'-')
            return True
        return False

    def flip_biased_coin(self):
        '''
        Flip biased coin and return True if coin_toss<= self._M/self._t
        '''

        coin_toss = random.random()
        if (coin_toss <= self._M/self._t):
            return True
        else:
            return False
    
    def update_counters(self,u,v,op):
        '''
        Update the local and the global counters based on the operation proceeded on this cycle
        '''

        common_neighborhood = self.find_common_neighborhood(u,v)
        if common_neighborhood:
            for c in common_neighborhood:
                if op == '+':
                    # Increment
                    self._globalT += 1
                    if c in self._localT:
                        self._localT[c] += 1
                    else:
                        self._localT[c] = 1
                    if u in self._localT:
                        self._localT[u] += 1
                    else:
                        self._localT[u] =1
                    if v in self._localT:
                        self._localT[v] += 1
                    else:
                        self._localT[v] = 1

                elif op == '-':
                    # Decrement 
                    self._globalT -= 1
                    self._localT[c] -= 1
                    self._localT[u] -= 1
                    self._localT[v] -= 1

                    # Remove if zero
                    if self._localT[c] == 0:
                        self._localT.pop(c)
                    if self._localT[u] == 0:
                        self._localT.pop(u)
                    if self._localT[v] == 0:
                        self._localT.pop(v)
        
    def estimate_triangles(self):
        '''
        Calculate the final triangle estimation from the current counters, M, t values
        '''

        estimate = max(1, (self._t * (self._t - 1) * (self._t - 2))/(self._M * (self._M - 1) * (self._M - 2)))
        global_estimate = int(estimate * self._globalT)
        for each in self._localT:
            self._localT[each] = int(self._localT[each] * estimate)

        return {'global':global_estimate,'local':self._localT}

    @staticmethod
    def run(self, graph):
        for u,v in graph.values:
            self._t += 1
            if self.sample_edge(u, v):
                self.add_edge(u,v)
                self.update_counters(u,v,'+')
        estimation = self.estimate_triangles()
        return estimation

df = pd.read_csv('../input/lastfm_asia_edges.csv', delimiter=',')
# graph = nx.from_pandas_edgelist(df, 'node_1', 'node_2')
tr = Triest(1000)
result = tr.run(tr, df)
print(result)
# print(len(tr))
