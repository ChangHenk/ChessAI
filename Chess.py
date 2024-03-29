# Title: Chess AI
# Author: Henk
# Create date: 2022/12/09
# Latest Update: 2023/07/24
# Log:
# 2022/12/09:   1.create Chess.py 2.define rules
# 2022/12/22:   1.show board 2.move chessmen 3.record play in match.txt
# 2022/12/23:   1.pawn movement 2.possible moves 3.adjust match record 
# 2022/12/25:   1.all movements 2.all possible moves exept specials 
# 2023/03/30:   1.redo move if illegal. 2.promotion 3.concept of checkmate
# 2023/07/24:   1.fix jumping through opponent pieces and promotion 2. add intro description

'''
Chess board coordinates:
        Row (horizontal)  - a-h
        Column (vertical) - 1-8


Chessmen movements:
King K:
        Basic - Diagonal, straight, sideways for 1 grid 
        Eat   - Chessmen on diagonal, straight, sideways for 1 grid 
        Note  - None

Queen Q:
        Basic - Diagonal, straight, sideways
        Eat   - First chessmen on diagonal/straight/sideways
        Note  - Cannot cross other chessmens

Rook R:
        Basic - Straight, sideways
        Eat   - First chessmen straight/sideways
        Note  - Cannot cross other chessmens

Bishop B:
        Basic - Diagonal
        Eat   - First chessmen on diagonal
        Note  - Cannot cross other chessmens

Knight N:
        Basic - Row +/-1, column +/- 2 | row +/- 2, column +/- 1 
        Eat   - Chessmen on row +/-1, column +/- 2 | row +/- 2, column +/- 1
        Note  - Can cross other chessmens

Pawn  :
        Basic - Column + 1/2 for first move, column + 1 for else (o)
        Eat   - Chessmen on column +1, +/-1 row 
        Note  - Cannot cross other chessmens

Special movements:
En passant:
        Basic - Enemy pawn column+2, pawn on column5 can eat enemy pawn and go to enemy pawn column-1 
        Note  - Can only exicute right after enemy pawn column + 2

Promotion: 
        Basic - Pawn goto column8, promote to King/Queen/Rook/Bishop/Knight 

Castling:
        Basic - King row +2, Rook row -2 / King row -2, Rook row +3 
        Rule1 - King and rook have not been moved
        Rule2 - No chessmen between King and rook
        Rule3 - King cannot be eat on the way
        Rule4 - King and rook on the same row
        
'''

import re
import os
from colorama import init
import win32console
import win32gui




def writeRecord(str):
        with open('match.txt','a+') as f:
                f.write(str)


def clear():
        _ = os.system('cls')


def setWindow():
        window = win32console.GetConsoleWindow()
        win32gui.MoveWindow(window, 500, 100, 500, 500, True)


class Chess:
        def __init__(self):
                self.board = {
                'a8':['R','b'], 'b8':['N','b'], 'c8':['B','b'],'d8':['Q','b'], 'e8':['K','b'], 'f8':['B','b'], 'g8':['N','b'], 'h8':['R','b'],
                'a7':['P','b'], 'b7':['P','b'], 'c7':['P','b'],'d7':['P','b'], 'e7':['P','b'], 'f7':['P','b'], 'g7':['P','b'], 'h7':['P','b'],                                
                'a6':[' ',' '], 'b6':[' ',' '], 'c6':[' ',' '],'d6':[' ',' '], 'e6':[' ',' '], 'f6':[' ',' '], 'g6':[' ',' '], 'h6':[' ',' '],
                'a5':[' ',' '], 'b5':[' ',' '], 'c5':[' ',' '],'d5':[' ',' '], 'e5':[' ',' '], 'f5':[' ',' '], 'g5':[' ',' '], 'h5':[' ',' '], 
                'a4':[' ',' '], 'b4':[' ',' '], 'c4':[' ',' '],'d4':[' ',' '], 'e4':[' ',' '], 'f4':[' ',' '], 'g4':[' ',' '], 'h4':[' ',' '],  
                'a3':[' ',' '], 'b3':[' ',' '], 'c3':[' ',' '],'d3':[' ',' '], 'e3':[' ',' '], 'f3':[' ',' '], 'g3':[' ',' '], 'h3':[' ',' '],  
                'a2':['P','w'], 'b2':['P','w'], 'c2':['P','w'],'d2':['P','w'], 'e2':['P','w'], 'f2':['P','w'], 'g2':['P','w'], 'h2':['P','w'], 
                'a1':['R','w'], 'b1':['N','w'], 'c1':['B','w'],'d1':['Q','w'], 'e1':['K','w'], 'f1':['B','w'], 'g1':['N','w'], 'h1':['R','w'],
                }

                self.intro()

                player1 = input('Enter your name(White): ')
                player2 = input('Enter your name(Black): ')

                self.player = {
                0:[player1,'w','e1'],
                1:[player2,'b','e8']
                }

                print('Match found!')
                
                str = '{0}({1}) vs {2}({3}).\n'.format(self.player[0][0], self.player[0][1], self.player[1][0], self.player[1][1])
                self.countMoves = 1
                self.flag_end = 0
                self.turn = 0
                writeRecord(str)


        def drawboard(self):
                print('\033[33m',' ','a','b','c','d','e','f','g','h',' ','\033[0m',sep=' ')
                for i in range(8):
                        line = list(self.board.values())[8*i:8*(i+1)]
                        print('\033[33m{}\033[0m|'.format(8-i),line[0][0],line[1][0],line[2][0],line[3][0],line[4][0],line[5][0],line[6][0],line[7][0],'|\033[33m{}\033[0m'.format(8-i),sep=' ')

                print('\033[33m',' ','a','b','c','d','e','f','g','h',' ','\033[0m',sep=' ')
                print('\nIt\'s {0}({1})\'s turn!'.format(self.player[self.turn][0],self.player[self.turn][1]))


        def move(self):
                self.movement = input('Enter your move: ')
                self.checkEnd()

                if self.flag_end == 0:
                        if self.turn == 0:
                                str = '{0}.{1} '.format(self.countMoves,self.movement)
                                writeRecord(str)
                        else:
                                self.countMoves = self.countMoves + 1
                                str = '{0} '.format(self.movement)
                                writeRecord(str)
                        
                        # \w(?=\w\d) for +
                        regex = re.compile('\w\d')
                        From, To = regex.findall(self.movement)

                        # is possible move align with actual move? if so redo move.
                        Possible = self.possibleMove(From)

                        move_illegal = [i for i in Possible if i==To]
                        if(move_illegal == []):
                                if(self.board[From][0] == ' '):
                                        str = "No chessmen on {0}!".format(From)
                                else:
                                        str = "Can't move from {0} to {1}.\nPossible moves for {0} is {2}.".format(From,To,Possible)
                                print(str+"\nPlease redo your move.")
                                self.move()

                        elif(self.board[From][1] != self.player[self.turn][1]):
                                print("Not your chessmen!\nPlease redo your move.")
                                self.move()

                        else:
                                # Promotion
                                if(self.board[From][0] == 'P'):
                                        if(To[1]=='8' and self.board[From][1]=='w'):
                                                self.promotion(From)
                                        elif(To[1]=='1' and self.board[From][1]=='b'):
                                                self.promotion(From)


                                if self.board[To][0] != ' ':
                                        self.board[To] = [' ',' ']
                                        
                                tempF = self.board[From]
                                tempT = self.board[To]

                                self.board[From] = tempT
                                self.board[To] = tempF
                                # king pos update
                                # 1. save king pos in self.player[self.turn][2]
                                # 2. use function findKing
                                if self.board[From][0] == 'K':
                                        self.player[self.turn][2] = To

                                # change player
                                self.turn = not self.turn


        def possibleMove(self, Pos):

                Possible = []
                forward = 1
                backward = -1

                Chessmen = self.board[Pos][0]
                if Chessmen == ' ':
                        return Possible

                color = self.board[Pos][1]

                coordinates = {
                        'column':       {'1':1,'2':2,'3':3,'4':4,'5':5,'6':6,'7':7,'8':8},
                        'row':          {'a':1,'b':2,'c':3,'d':4,'e':5,'f':6,'g':7,'h':8}
                }

                row = coordinates['row'][Pos[0]]
                column = coordinates['column'][Pos[1]]
                


                if Chessmen == 'N':
                        row1 = row + 1
                        row2 = row - 1
                        row3 = row + 2
                        row4 = row - 2
                        column1 = column - 2
                        column2 = column + 2
                        column3 = column - 1
                        column4 = column + 1

                        if row1 <= 8 and column1 >= 1:
                                Pos1 = self.getKey(coordinates['row'], row1) + self.getKey(coordinates['column'], column1)
                                if self.board[Pos1][0] == ' ' or self.board[Pos1][1] == self.player[not self.turn][1]:
                                        Possible.append(Pos1)

                        if row1 <= 8 and column2 <= 8:
                                Pos2 = self.getKey(coordinates['row'], row1) + self.getKey(coordinates['column'], column2)
                                if self.board[Pos2][0] == ' ' or self.board[Pos2][1] == self.player[not self.turn][1]:
                                        Possible.append(Pos2)

                        if row2 >= 1 and column1 >= 1:
                                Pos3 = self.getKey(coordinates['row'], row2) + self.getKey(coordinates['column'], column1)
                                if self.board[Pos3][0] == ' ' or self.board[Pos3][1] == self.player[not self.turn][1]:
                                        Possible.append(Pos3)

                        if row2 >= 1 and column2 <= 8:
                                Pos4 = self.getKey(coordinates['row'], row2) + self.getKey(coordinates['column'], column2)
                                if self.board[Pos4][0] == ' ' or self.board[Pos4][1] == self.player[not self.turn][1]:
                                        Possible.append(Pos4)

                        if row3 <= 8 and column3 >= 1:
                                Pos5 = self.getKey(coordinates['row'], row3) + self.getKey(coordinates['column'], column3)
                                if self.board[Pos5][0] == ' ' or self.board[Pos5][1] == self.player[not self.turn][1]:
                                        Possible.append(Pos5)

                        if row3 <= 8 and column4 <= 8:
                                Pos6 = self.getKey(coordinates['row'], row3) + self.getKey(coordinates['column'], column4)
                                if self.board[Pos6][0] == ' ' or self.board[Pos6][1] == self.player[not self.turn][1]:
                                        Possible.append(Pos6)

                        if row4 >= 1 and column3 >= 1:
                                Pos7 = self.getKey(coordinates['row'], row4) + self.getKey(coordinates['column'], column3)
                                if self.board[Pos7][0] == ' ' or self.board[Pos7][1] == self.player[not self.turn][1]:
                                        Possible.append(Pos7)

                        if row4 >= 1 and column4 <= 8:
                                Pos8 = self.getKey(coordinates['row'], row4) + self.getKey(coordinates['column'], column4)
                                if self.board[Pos8][0] == ' ' or self.board[Pos8][1] == self.player[not self.turn][1]:
                                        Possible.append(Pos8)

                elif Chessmen == 'R':
                        for i in range(1,8):
                                row1 = row + i
                                if row1 <= 8 and row1 >= 1:
                                        Pos1 = self.getKey(coordinates['row'], row1) + self.getKey(coordinates['column'], column)
                                        if self.board[Pos1][0] == ' ':
                                                Possible.append(Pos1)
                                        elif self.board[Pos1][1] == self.player[not self.turn][1]:
                                                Possible.append(Pos1)
                                                break
                                        else:
                                                break
                                else:
                                        break

                        for i in range(1,8):
                                row2 = row - i
                                if row2 <= 8 and row2 >= 1:
                                        Pos2 = self.getKey(coordinates['row'], row2) + self.getKey(coordinates['column'], column)
                                        if self.board[Pos2][0] == ' ':
                                                Possible.append(Pos2)
                                        elif self.board[Pos2][1] == self.player[not self.turn][1]:
                                                Possible.append(Pos2)
                                                break
                                        else:
                                                break
                                else:
                                        break

                        for i in range(1,8):
                                column1 = column + i
                                if column1 <= 8 and column1 >= 1:
                                        Pos3 = self.getKey(coordinates['row'], row) + self.getKey(coordinates['column'], column1)
                                        if self.board[Pos3][0] == ' ':
                                                Possible.append(Pos3)
                                        elif self.board[Pos3][1] == self.player[not self.turn][1]:
                                                Possible.append(Pos3)
                                                break
                                        else:
                                                break
                                else:
                                        break

                        for i in range(1,8):
                                column2 = column - i
                                if column2 <= 8 and column2 >= 1:
                                        Pos4 = self.getKey(coordinates['row'], row) + self.getKey(coordinates['column'], column2)
                                        if self.board[Pos4][0] == ' ':
                                                Possible.append(Pos4)
                                        elif self.board[Pos4][1] == self.player[not self.turn][1]:
                                                Possible.append(Pos4)
                                                break
                                        else:
                                                break
                                else:
                                        break

                elif Chessmen == 'B':
                        for i in range(1,8):
                                row1 = row + i
                                column1 = column + i
                                if row1 <= 8 and column1 <= 8:
                                        Pos1 = self.getKey(coordinates['row'], row1) + self.getKey(coordinates['column'], column1)
                                        if self.board[Pos1][0] == ' ':
                                                Possible.append(Pos1)
                                        elif self.board[Pos1][1] == self.player[not self.turn][1]:
                                                Possible.append(Pos1)
                                                break
                                        else:
                                                break
                                else:
                                        break

                        for i in range(1,8):
                                row2 = row + i
                                column2 = column - i
                                if row2 <= 8 and column2 >= 1:
                                        Pos2 = self.getKey(coordinates['row'], row2) + self.getKey(coordinates['column'], column2)
                                        if self.board[Pos2][0] == ' ':
                                                Possible.append(Pos2)
                                        elif self.board[Pos2][1] == self.player[not self.turn][1]:
                                                Possible.append(Pos2)
                                                break
                                        else:
                                                break
                                else:
                                        break

                        for i in range(1,8):
                                row3 = row - i
                                column3 = column + i
                                if row3 >= 1 and column3 <= 8:
                                        Pos3 = self.getKey(coordinates['row'], row3) + self.getKey(coordinates['column'], column3)
                                        if self.board[Pos3][0] == ' ':
                                                Possible.append(Pos3)
                                        elif self.board[Pos3][1] == self.player[not self.turn][1]:
                                                Possible.append(Pos3)
                                                break
                                        else:
                                                break
                                else:
                                        break

                        for i in range(1,8):
                                row4 = row - i
                                column4 = column - i
                                if row4 >= 1 and column4 >= 1:
                                        Pos4 = self.getKey(coordinates['row'], row4) + self.getKey(coordinates['column'], column4)
                                        if self.board[Pos4][0] == ' ':
                                                Possible.append(Pos4)
                                        elif self.board[Pos4][1] == self.player[not self.turn][1]:
                                                Possible.append(Pos4)
                                                break
                                        else:
                                                break
                                else:
                                        break

                elif Chessmen == 'K':
                        row1 = row + 1
                        row2 = row - 1
                        column1 = column + 1
                        column2 = column - 1

                        if row1 <= 8:
                                Pos1 = self.getKey(coordinates['row'], row1) + self.getKey(coordinates['column'], column)
                                if self.board[Pos1][0] == ' ':
                                        Possible.append(Pos1)
                                elif self.board[Pos1][1] == self.player[not self.turn][1]:
                                        Possible.append(Pos1)

                        if row1 <= 8 and column1 <= 8:
                                Pos2 = self.getKey(coordinates['row'], row1) + self.getKey(coordinates['column'], column1)
                                if self.board[Pos2][0] == ' ':
                                        Possible.append(Pos2)
                                elif self.board[Pos2][1] == self.player[not self.turn][1]:
                                        Possible.append(Pos2)

                        if row1 <= 8 and column2 >= 1:
                                Pos3 = self.getKey(coordinates['row'], row1) + self.getKey(coordinates['column'], column2)
                                if self.board[Pos3][0] == ' ':
                                        Possible.append(Pos3)
                                elif self.board[Pos3][1] == self.player[not self.turn][1]:
                                        Possible.append(Pos3)

                        if column1 <= 8:
                                Pos4 = self.getKey(coordinates['row'], row) + self.getKey(coordinates['column'], column1)
                                if self.board[Pos4][0] == ' ':
                                        Possible.append(Pos4)
                                elif self.board[Pos4][1] == self.player[not self.turn][1]:
                                        Possible.append(Pos4)

                        if column2 >= 1:
                                Pos5 = self.getKey(coordinates['row'], row) + self.getKey(coordinates['column'], column2)
                                if self.board[Pos5][0] == ' ':
                                        Possible.append(Pos5)
                                elif self.board[Pos5][1] == self.player[not self.turn][1]:
                                        Possible.append(Pos5)

                        if row2 >= 1:
                                Pos6 = self.getKey(coordinates['row'], row2) + self.getKey(coordinates['column'], column)
                                if self.board[Pos6][0] == ' ':
                                        Possible.append(Pos6)
                                elif self.board[Pos6][1] == self.player[not self.turn][1]:
                                        Possible.append(Pos6)

                        if row2 >= 1 and column1 <= 8:
                                Pos7 = self.getKey(coordinates['row'], row2) + self.getKey(coordinates['column'], column1)
                                if self.board[Pos7][0] == ' ':
                                        Possible.append(Pos7)
                                elif self.board[Pos7][1] == self.player[not self.turn][1]:
                                        Possible.append(Pos7)

                        if row2 >= 1 and column2 >= 1:
                                Pos8 = self.getKey(coordinates['row'], row2) + self.getKey(coordinates['column'], column2)
                                if self.board[Pos8][0] == ' ':
                                        Possible.append(Pos8)
                                elif self.board[Pos8][1] == self.player[not self.turn][1]:
                                        Possible.append(Pos8)

                elif Chessmen == 'Q':
                        for i in range(1,8):
                                row1 = row + i
                                if row1 <= 8:
                                        Pos1 = self.getKey(coordinates['row'], row1) + self.getKey(coordinates['column'], column)
                                        if self.board[Pos1][0] == ' ':
                                                Possible.append(Pos1)
                                        elif self.board[Pos1][1] == self.player[not self.turn][1]:
                                                Possible.append(Pos1)
                                                break
                                        else:
                                                break
                                else:
                                        break

                        for i in range(1,8):
                                row1 = row + i
                                column1 = column + i
                                if row1 <= 8 and column1 <= 8:
                                        Pos2 = self.getKey(coordinates['row'], row1) + self.getKey(coordinates['column'], column1)
                                        if self.board[Pos2][0] == ' ':
                                                Possible.append(Pos2)
                                        elif self.board[Pos2][1] == self.player[not self.turn][1]:
                                                Possible.append(Pos2)
                                                break
                                        else:
                                                break
                                else:
                                        break

                        for i in range(1,8):
                                row1 = row + i
                                column2 = column - i
                                if row1 <= 8 and column2 >= 1:
                                        Pos3 = self.getKey(coordinates['row'], row1) + self.getKey(coordinates['column'], column2)
                                        if self.board[Pos3][0] == ' ':
                                                Possible.append(Pos3)
                                        elif self.board[Pos3][1] == self.player[not self.turn][1]:
                                                Possible.append(Pos3)
                                                break
                                        else:
                                                break
                                else:
                                        break

                        for i in range(1,8):
                                column1 = column + i
                                if column1 <= 8:
                                        Pos4 = self.getKey(coordinates['row'], row) + self.getKey(coordinates['column'], column1)
                                        if self.board[Pos4][0] == ' ':
                                                Possible.append(Pos4)
                                        elif self.board[Pos4][1] == self.player[not self.turn][1]:
                                                Possible.append(Pos4)
                                                break
                                        else:
                                                break
                                else:
                                        break

                        for i in range(1,8):
                                column2 = column - i
                                if column2 >= 1:
                                        Pos5 = self.getKey(coordinates['row'], row) + self.getKey(coordinates['column'], column2)
                                        if self.board[Pos5][0] == ' ':
                                                Possible.append(Pos5)
                                        elif self.board[Pos5][1] == self.player[not self.turn][1]:
                                                Possible.append(Pos5)
                                                break
                                        else:
                                                break
                                else:
                                        break

                        for i in range(1,8):
                                row2 = row - i
                                if row2 >= 1:
                                        Pos6 = self.getKey(coordinates['row'], row2) + self.getKey(coordinates['column'], column)
                                        if self.board[Pos6][0] == ' ':
                                                Possible.append(Pos6)
                                        elif self.board[Pos6][1] == self.player[not self.turn][1]:
                                                Possible.append(Pos6)
                                                break
                                        else:
                                                break
                                else:
                                        break

                        for i in range(1,8):
                                row2 = row - i
                                column1 = column + i
                                if row2 >= 1 and column1 <= 8:
                                        Pos7 = self.getKey(coordinates['row'], row2) + self.getKey(coordinates['column'], column1)
                                        if self.board[Pos7][0] == ' ':
                                                Possible.append(Pos7)
                                        elif self.board[Pos7][1] == self.player[not self.turn][1]:
                                                Possible.append(Pos7)
                                                break
                                        else:
                                                break
                                else:
                                        break

                        for i in range(1,8):
                                row2 = row - i
                                column2 = column - i
                                if row2 >= 1 and column2 >= 1:
                                        Pos8 = self.getKey(coordinates['row'], row2) + self.getKey(coordinates['column'], column2)
                                        if self.board[Pos8][0] == ' ':
                                                Possible.append(Pos8)
                                        elif self.board[Pos8][1] == self.player[not self.turn][1]:
                                                Possible.append(Pos8)
                                                break
                                        else:
                                                break
                                else:
                                        break

                # Castling
                elif Chessmen == 'O-O-O':
                        pass
                
                elif Chessmen == 'O-O':
                        pass


                # Pawn
                else:
                        if color == 'w':
                                moveDir = forward
                                if Pos[1] != '2':
                                        firstmove = 0
                                else:
                                        firstmove = 1                                        
                        else:
                                moveDir = backward
                                if Pos[1] != '7':
                                        firstmove = 0
                                else:
                                        firstmove = 1

                        column1 = column + moveDir*1
                        
                        # En passant
                        
                        Pos1 = self.getKey(coordinates['row'], row) + self.getKey(coordinates['column'], column1)
                        if self.board[Pos1][0] == ' ':
                                Possible.append(Pos1)

                        if firstmove == 1:
                                column2 = column + moveDir*2
                                Pos2 = self.getKey(coordinates['row'], row) + self.getKey(coordinates['column'], column2)
                                if self.board[Pos2][0] == ' ' and self.board[Pos1][0] ==' ':
                                        Possible.append(Pos2)

                        row1 = row + 1
                        if row1 <= 8:
                                Pos3 = self.getKey(coordinates['row'], row1) + self.getKey(coordinates['column'], column1)
                                if self.board[Pos3][1] == self.player[not self.turn][1]:
                                        Possible.append(Pos3)

                        row2 = row - 1
                        if row2 >= 1:                    
                                Pos4 = self.getKey(coordinates['row'], row2) + self.getKey(coordinates['column'], column1)
                                if self.board[Pos4][1] == self.player[not self.turn][1]:
                                        Possible.append(Pos4)


                return Possible


        # 1. search all opponent chessmen see if there are possible moves on the king's position (check)
        # 2. for those chessmen that match 1., record their positions and possible moves toward the king 
        # 3. by 2. we will know which position is available, then search all possible moves 
        #    that will make no opponent chessmen has possible move on the king
        # 4. if moves in 3. don't exist, checkmate; else they are the possible moves
        # 5. when the player enters the move they want, compare these possible moves

        def check(self):
                BKPos, WKPos = self.findKing()
                searchColor = 'w'
                Possible = []
                if self.player[self.turn][1] == 'w':
                        searchColor = 'b'
                for key, value in self.board.items():
                        if searchColor == value[1]:
                                Possible.append(self.possibleMove(key))
                


        def promotion(self,From):
                promote = input("Select for promotion: 1.Q 2.R 3.B 4.N").upper()
                if(promote == 'Q'):
                        self.board[From][0] = promote.upper()
                        print("Promote Pawn to Queen.")
                elif(promote == 'R'):
                        self.board[From][0] = promote.upper()
                        print("Promote Pawn to Rook.")                
                elif(promote == 'B'):
                        self.board[From][0] = promote.upper()
                        print("Promote Pawn to Bishop.")               
                elif(promote == 'N'):
                        self.board[From][0] = promote.upper()
                        print("Promote Pawn to Knight.")      
                else:
                        print("Please enter Q,R,B,N to choose promotion.")
                        self.promotion(From)
                

        def checkEnd(self):
                if(self.movement.lower() == 'resign'):
                        self.flag_end = 1
                        str = '\n{0} won.\n'.format(self.player[not self.turn][0])
                        writeRecord(str)
                        print('Match end.')

                # checkmate
                # elif(self.possibleMove(self.player[self.turn][2]) == [] and King is checked):
                        # self.flag_end = 1
                        # str = '\n{0} won.\n'.format(self.player[not self.turn][0])
                        # writeRecord(str)
                        # print('Match end.')

                # draw
                # 1. players agree on a draw
                # 2. no possible move for all chessmen
                # 3. repeated moves for N steps, N=limited steps
                
                else:
                        pass


        def findKing(self):
                for key, value in self.board.items():
                        if ['K','b'] == value:
                                print("Black king at {0}".format(key))
                                BKPos = key
                        elif ['K','w'] == value:
                                print("White king at {0}".format(key))
                                WKPos = key
                return BKPos, WKPos


        def getKey(self, dict, value):
                for k,v in dict.items():
                        if v == value:
                                return k




        def intro(self):
                clear()
                print("Game: Chess\nAuthor: Henk\nSelect 1~3 for more information:\n1. Start Game\n2. How To Play\n3. Chess Rules\n")
                select = input('Please enter: ')
                if select == '1':
                        clear()
                elif select == '2':
                        print("\n\n***************************How To Play***************************\n\n")
                        print("\
1. Enter names for Players, then the game will be started.\n\
2. Enter the block the peice you want to move and where to.\n   For example: \
to move \"Pawn\" from \"c2\" to \"c4\", enter: \"c2c4\".\n\
3. Enter \"resign\" and you will lose the game.\n")
                        print("\n\n*****************************************************************\n\n")
                        menu = input("Press Y to return menu.").upper()
                        if menu == 'Y':
                                self.intro()

                elif select == '3':
                        print("Chess Rules")
                        menu = input("Press Y to return menu.").upper()
                        if menu == 'Y':
                                self.intro()

                else:
                        self.intro()


def play():
        init(autoreset=True)
        setWindow()
        chess = Chess()

        while(chess.flag_end == 0):
                chess.drawboard()
                chess.move()
