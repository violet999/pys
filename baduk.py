from enum import Enum
import enum
import numpy as np

class State(enum.IntEnum):
    EMPTY=0
    BLACK=1
    WHITE=2
    WALL=3

class Baduk:
    size = 19
    size2 = 21
    current_board=None
    current_color=State.BLACK
    def __init__(self,size=19):
        self.size = size
        self.current_board = Board(size)
        self.size2 = size + 2

    def board_print(self):
        for line in range(self.size2):
            start = (self.size2-line-1)*self.size2
            end = (self.size2-line)*self.size2
            print(self.current_board.ToString()[start:end].tostring())
    def board_move(self,x,y):
        rev = self.current_board.Move(x,y,self.current_color)
        if rev == True:
            if self.current_color == State.BLACK :
                self.current_color = State.WHITE
            else :
                self.current_color = State.BLACK

class Board:
    size = 19
    size2 = 21
    board_state = None
    board_group = None
    def __init__(self,size=19):
        self.size=size
        self.size2= size+2
        self.board_state = np.zeros((self.size2,self.size2),dtype=np.int32)
        for x in range(self.size2):
            for y in range(self.size2):
                if x==0 or y==0 or x==self.size2-1 or y==self.size2-1 :
                    self.board_state[x,y] = State.WALL
                else :
                    self.board_state[x,y] = State.EMPTY
        self.board_group  = {0:0}
    def __del__(self):
        del self.board_state
        del self.board_group

    def Move(self,x,y,color):
        if self.board_state[x,y] != State.EMPTY :
            return False
        else :
            self.board_state[x,y] = color
        return True

    def ToString(self):
        rev = np.chararray((self.size2**2))
        for x in range(self.size2):
            for y in range(self.size2):
                color = self.board_state[x,y]
                if color==State.EMPTY :
                    rev[self.size2*y + x] = '.'
                elif color==State.BLACK :
                    rev[self.size2 * y + x] = 'B'
                elif color == State.WHITE:
                    rev[self.size2 * y + x] = 'W'
                else :
                    rev[self.size2 * y + x] = 'o'
        return rev


baduk = Baduk(19)
baduk.board_move(1,2)
baduk.board_move(2,3)
baduk.board_move(4,5)
baduk.board_print()