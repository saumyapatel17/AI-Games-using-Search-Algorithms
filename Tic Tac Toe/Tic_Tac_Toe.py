import math
from copy import deepcopy
import numpy as np
import pygame
import sys
import time

X = "X"
O = "O"
EMPTY = None

pygame.init()
size = width, height = 600, 400

black = (0, 0, 0)
white = (255, 255, 255)

screen = pygame.display.set_mode(size)

mediumFont = pygame.font.Font("Open Sans Regular.ttf", 28)
largeFont = pygame.font.Font("Open Sans Regular.ttf", 40)
moveFont = pygame.font.Font("Open Sans Regular.ttf", 60)

def initial_state():
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]

def get_diagonal(board):
    return [[board[0][0], board[1][1], board[2][2]],
            [board[0][2], board[1][1], board[2][0]]]

def get_columns(board):
    columns = []
    for i in range(3):
        columns.append([row[i] for row in board])
    return columns

def three_in_a_row(row):
    return True if row.count(row[0]) == 3 else False

# Returns player who has the next turn on a board.
def player(board):
    count_x=0
    count_o=0
    for i in board:
        for j in i:
            if(j=="X"):
                count_x=count_x+1
            if(j=="O"):
                count_o=count_o+1
    return O if count_x > count_o else X

# Returns set of all possible actions (i, j) available
def actions(board):
    action=set()
    for i, row in enumerate(board):
        for j , vall in enumerate(row):
            if(vall==EMPTY):
                action.add((i,j))
    return action

# Returns the board that results from making move 
def result(board, action):
    i,j=action
    if(board[i][j]!=EMPTY):
        raise Exception("Invalid Move ")
    next_move=player(board)
    deep_board=deepcopy(board)
    deep_board[i][j]=next_move
    return deep_board

# Returns the winner of the game
def winner(board):
    rows=board+get_diagonal(board) +get_columns(board)
    for row in rows:
        current_palyer=row[0]
        if current_palyer is not None and three_in_a_row(row):
            return current_palyer
    return None

def terminal(board):
    xx=winner(board)
    if(xx is  not None):
        return True
    if(all(all(j!=EMPTY for j in i) for i in board)):
        return True
    return False

def utility(board):
    xx=winner(board)
    if(xx==X):
        return 1
    elif(xx==O):
        return -1
    else:
        return 0 

def max_alpha_beta_pruning(board ,alpha,beta):
    if(terminal(board)== True):
        return utility(board) , None
    vall=float("-inf")
    best=None
    for action in actions(board):
        min_val=min_alpha_beta_pruning(result(board ,action), alpha, beta)[0]
        if( min_val > vall):
            best=action
            vall=min_val
        alpha=max(alpha,vall)
        if (beta <= alpha):
            break
    return vall,best

def min_alpha_beta_pruning(board ,alpha,beta):
    if(terminal(board)== True):
        return utility(board) , None
    vall=float("inf")
    best=None
    for action in actions(board):
        max_val=max_alpha_beta_pruning(result(board ,action), alpha, beta)[0]
        if( max_val < vall):
            best=action
            vall=max_val
        beta=min(beta,vall)
        if (beta <= alpha):
            break
    return vall,best

def minimax(board):
    if terminal(board):
        return None
    if(player(board)==X):
        return max_alpha_beta_pruning(board ,float("-inf") ,float("inf"))[1]
    elif(player(board) == O):
        return min_alpha_beta_pruning(board , float("-inf"), float("inf"))[1]
    else:
        raise Exception("Error in Caculating Optimal Move")

user = None
board = initial_state()
ai_turn = False

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

    screen.fill(black)
    if user is None:
        title = largeFont.render("Play Tic-Tac-Toe", True, white)
        titleRect = title.get_rect()
        titleRect.center = ((width / 2), 50)
        screen.blit(title, titleRect)

        playXButton = pygame.Rect((width / 8), (height / 2), width / 4, 50)
        playX = mediumFont.render("Play as X", True, black)
        playXRect = playX.get_rect()
        playXRect.center = playXButton.center
        pygame.draw.rect(screen, white, playXButton)
        screen.blit(playX, playXRect)

        playOButton = pygame.Rect(5 * (width / 8), (height / 2), width / 4, 50)
        playO = mediumFont.render("Play as O", True, black)
        playORect = playO.get_rect()
        playORect.center = playOButton.center
        pygame.draw.rect(screen, white, playOButton)
        screen.blit(playO, playORect)

        click, _, _ = pygame.mouse.get_pressed()
        if click == 1:
            mouse = pygame.mouse.get_pos()
            if playXButton.collidepoint(mouse):
                time.sleep(0.2)
                user = X
            elif playOButton.collidepoint(mouse):
                time.sleep(0.2)
                user = O

    else:
        tile_size = 80
        tile_origin = (width / 2 - (1.5 * tile_size), height / 2 - (1.5 * tile_size))
        tiles = []
        for i in range(3):
            row = []
            for j in range(3):
                rect = pygame.Rect(tile_origin[0] + j * tile_size,tile_origin[1] + i * tile_size,tile_size, tile_size)
                pygame.draw.rect(screen, white, rect, 3)

                if board[i][j] != EMPTY:
                    move = moveFont.render(board[i][j], True, white)
                    moveRect = move.get_rect()
                    moveRect.center = rect.center
                    screen.blit(move, moveRect)
                row.append(rect)
            tiles.append(row)

        game_over = terminal(board)
        play = player(board)

        if game_over:
            winner = winner(board)
            if winner is None:
                title = f"Game Over: Tie."
            else:
                title = f"Game Over: {winner} wins."
        elif user == play:
            title = f"Play as {user}"
        else:
            title = f"Computer thinking..."
        title = largeFont.render(title, True, white)
        titleRect = title.get_rect()
        titleRect.center = ((width / 2), 30)
        screen.blit(title, titleRect)

        if user != play and not game_over:
            if ai_turn:
                time.sleep(0.5)
                move = minimax(board)
                board = result(board, move)
                ai_turn = False
            else:
                ai_turn = True

        click, _, _ = pygame.mouse.get_pressed()
        if click == 1 and user == play and not game_over:
            mouse = pygame.mouse.get_pos()
            for i in range(3):
                for j in range(3):
                    if (board[i][j] == EMPTY and tiles[i][j].collidepoint(mouse)):
                        board = result(board, (i, j))

        if game_over:
            againButton = pygame.Rect(width / 3, height - 65, width / 3, 50)
            again = mediumFont.render("Play Again", True, black)
            againRect = again.get_rect()
            againRect.center = againButton.center
            pygame.draw.rect(screen, white, againButton)
            screen.blit(again, againRect)
            click, _, _ = pygame.mouse.get_pressed()
            if click == 1:
                mouse = pygame.mouse.get_pos()
                if againButton.collidepoint(mouse):
                    time.sleep(0.2)
                    user = None
                    board = initial_state()
                    ai_turn = False

    pygame.display.flip()
