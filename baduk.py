from enum import Enum
import enum
import numpy as np
import string

class State(enum.IntEnum):
    EMPTY = 0
    BLACK = 1
    WHITE = 2
    WALL = 3

class Baduk:
    size = 19
    size2 = 21
    current_board = None
    current_color = State.BLACK
    def __init__(self,size=19):
        self.size = size
        self.current_board = Board(size)
        self.size2 = size + 2

    def board_print(self):
        for line in range(self.size2):
            start = (self.size2 - line - 1) * self.size2
            end = (self.size2 - line) * self.size2
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
    board_group_live = None
    board_group_next_group_number = 1
    def __init__(self):
        return
    def __init__(self,size=19):
        self.size = size
        self.size2 = size + 2
        self.board_state = np.zeros((self.size2,self.size2),dtype=np.int32)
        self.board_group = np.zeros((self.size2,self.size2),dtype=np.int32)
        for x in range(self.size2):
            for y in range(self.size2):
                self.board_group[x,y] = 0
                if x == 0 or y == 0 or x == self.size2 - 1 or y == self.size2 - 1 :
                    self.board_state[x,y] = State.WALL
                else :
                    self.board_state[x,y] = State.EMPTY
        self.board_group_live = {0:0}
        board_group_next_group_number = 1
    def clone(self):
        newone = Board()
        newone.size = self.size
        newone.size2 = self.size2
        newone.board_group_next_group_number = self.board_group_next_group_number
        newone.board_group_live = self.board_group_live.copy()
        np.copy(newone.board_group,self.board_group)
        np.copy(newone.board_state,self.board_state)
        
        return newone

    def __del__(self):
        del self.board_state
        del self.board_group
        del self.board_group_live

    def Move(self,x,y,color):
        if self.board_state[x,y] != State.EMPTY :
            return False
        else :
            near_empty_number = 0
            near_same_number = 0
            near_diff_number = 0
            dx = (1,-1,0,0)
            dy = (0,0,1,-1)
            for d in range(4):
                nx = x + dx[d]
                ny = y + dy[d]
                ncolor = self.board_state[nx,ny]
                if ncolor == State.EMPTY:
                    near_empty_number+=1
                if ncolor == State.BLACK or ncolor == State.WHITE:
                    if ncolor == color:
                        near_same_number+=1
                    else:
                        near_diff_number+=1
            if near_same_number == 0 and near_diff_number == 0:
                self.board_state[x,y] = color
                self.board_group[x,y] = self.board_group_next_group_number
                self.board_group_live[self.board_group_next_group_number]= near_empty_number
                self.board_group_next_group_number+=1
            if near_empty_number == 0:
                self.clone().try_move()
            else: #주의에 빈곳이 있어서 무조건 놓을 수 있음
                self.board_state[x,y] = color
                #group을 주위와 맞추기 위해서 검색함
                for d in range(4):
                    nx = x + dx[d]
                    ny = y + dy[d]
                    ncolor = self.board_state[nx,ny]
                    if ncolor != State.EMPTY:
                        self.board_group_live[ self.board_group[nx,ny]] -=1
                    
                    if color == ncolor and self.board_group[x,y]==0:  #현재 빈곳이라 
                        self.board_state[x,y] = color
                        self.board_group[x,y] = self.board_group[nx,ny]
                        self.board_group_live[self.self.board_group[x,y]]+=near_empty_number
                    elif color == ncolor and self.board_group[x,y]!=0:
                        gxy = self.board_group[x,y]
                        gnxy = self.board_group[nx,ny]
                        if gxy != gnxy:
                            join_group( gxy , gnxy)

                # 일단 주변 그룹넘버로 정하고
                # 더 찾아서 더 있으면 join
            
        return True
    def try_move(self):
        return True
    def join_group(self,ga,gb):
        gmax = max(ga,gb)
        gmin = ga+gb - gmax
        for x in range(size2):
            for y in range(size2):
                if board_group[x,y]==gmax:
                    board_group[x,y]=gmin
        self.board_group_live[gmin] += self.board_group_live[gmax]
        
                

                

    def ToString(self):
        rev = np.chararray((self.size2 ** 2))
        for x in range(self.size2):
            for y in range(self.size2):
                color = self.board_state[x,y]
                if color == State.EMPTY :
                    rev[self.size2 * y + x] = '.'
                elif color == State.BLACK :
                    rev[self.size2 * y + x] = 'B'
                elif color == State.WHITE:
                    rev[self.size2 * y + x] = 'W'
                else :
                    rev[self.size2 * y + x] = 'o'
        return rev

class BadukGame:
    
    def Run(self):
        baduk = Baduk(19)
        while(True):
            command = input("Input x,y (q:exit) : ")
            if len(command)<1:
                continue
            if command[0]=='q':
                print("End")
                break
            left,right = command.split(',')
            print("left:",left," right:",right)
            
            x = int(left)
            y = int(right)
            baduk.board_move(x,y)
            baduk.board_print()

def __main__():
    baduk_game = BadukGame()
    baduk_game.Run()

__main__()