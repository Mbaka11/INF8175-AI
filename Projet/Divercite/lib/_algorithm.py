from .heuristic import Heuristic
from game_state_divercite import GameStateDivercite
from cachetools import FIFOCache,LFUCache,TTLCache,LRUCache,cachedmethod, Cache


class Algorithm:
    
    # Meta Data 
    is_first_move: bool = None
    current_state: GameStateDivercite = None
    my_id: int = None
    opponent_id: int = None
    remaining_time: float = None
    my_step:int = 0
    max_step: int = 0 
    
    @staticmethod
    def set_current_state(current_state:GameStateDivercite,remaining_time: float):
        Algorithm.current_state = current_state
        Algorithm.remaining_time = remaining_time
        Algorithm.my_step+=1
        if Algorithm.my_step == 1:
            Algorithm.init_game_state()
        
    @staticmethod
    def init_game_state():
        Algorithm.opponent_id = Algorithm.current_state.compute_next_player().id
        temp = [ player.id for player in Algorithm.current_state.players]
        temp.remove(Algorithm.opponent_id)
        Algorithm.my_id = temp[0]
        Algorithm.is_first_move = Algorithm.my_step == Algorithm.current_state.step
        
    
    def __init__(self,heuristic:Heuristic,cache:Cache):
        self.heuristic: Heuristic = heuristic
        self.cache = cache
        pass

    def compute_best_moves(self):
        pass
    
    @property
    def _get_my_pieces(self):
        return self.current_state.players_pieces_left[self.my_id]
    
    @property
    def my_score(self):
        return self.current_state.scores[self.my_id]

    @property
    def opponent_score(self):
        return self.current_state.scores[self.opponent_id]

    def _utility(self,state:GameStateDivercite):
        scores = state.get_scores()
        my_scores = scores[self.my_id]
        opponent_scores = scores[self.opponent_id]

        if my_scores > opponent_scores:
            return 1
        
        if my_scores < opponent_scores:
            return -1
        
        if my_scores == opponent_scores:
            return 0

    def _isTerminal(self,state:GameStateDivercite,current_depth:int):
        return state.step + current_depth == state.max_step

    def _turn(self):
        ...

    def _is_our_turn(self):
        if self.is_first_move and self.current_state.step % 2 == 0:
            return True
        
        if not self.is_first_move and self.current_state.step % 2 == 1:
            return True
        
        return False
             
    def _transition(self,state,action):
        return state.apply_action(action)
    
    def _compute_redondant_state(self,states:list):
        return states