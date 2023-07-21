import copy   
import sys 
infinity = float('inf')     
utilityVal = {}    
Board_used_in_current_game = [[0 for i in range(7)] for j in range(6)]
current_move_taken = 0
total_count_of_pieces = 0
total_score_player_one = 0
total_score_player_two = 0
current_game_file = None
computerColumn = None
total_depth_taken = 1 

def total_check_Piece_Count():  
    global total_count_of_pieces
    temp_val = sum(1 for row in  Board_used_in_current_game for piece in row if piece)
    total_count_of_pieces = temp_val 

def displayGB():  
    print('-----------------')
    for i in range(6):
        print('| ',end=""),
        for j in range(7):
            print(int( Board_used_in_current_game[i][j]),end=" "),
        print('|')
    print('-----------------')    

def print_the_game_board_to_file(): 
    global current_game_file
    for row in Board_used_in_current_game:
        temp_data_loop = ''.join(str(col) for col in row)
        temp_str = '\r'
        temp = temp_data_loop + temp_str
        current_game_file.write(temp)
    current_game_file.write('%s\r' % str(current_move_taken))

def get_total_check_Piece_Count(): 
    current_val =  Board_used_in_current_game
    temp_val = sum(1 for row in current_val for piece in row if piece)
    return temp_val

def playPiece( column):  
    global total_count_of_pieces
    global Board_used_in_current_game
    temp_status =  Board_used_in_current_game[0][column]
    if not temp_status:
        temp_list = list(range(5, -1, -1))
        for i in temp_list:
            if not  Board_used_in_current_game[i][column]:
                Board_used_in_current_game[i][column] =  current_move_taken
                total_count_of_pieces =  total_count_of_pieces + 1
                return 1

def checkPiece( column, opponent): 
    global total_count_of_pieces
    global Board_used_in_current_game
    if not  Board_used_in_current_game[0][column]:
        for i in range(5, -1, -1):
            if not  Board_used_in_current_game[i][column]:
                Board_used_in_current_game[i][column] = opponent
                total_count_of_pieces += 1
                return 1

def maxVal( currentNode): 
    global Board_used_in_current_game
    node = copy.deepcopy(currentNode)
    childNode = []
    for i in range(7):
        currentState =  playPiece(i)
        if currentState != None:
            childNode.append( Board_used_in_current_game)
            Board_used_in_current_game = copy.deepcopy(node)
    return childNode

def minVal( currentNode): 
    global Board_used_in_current_game
    global current_move_taken
    node = copy.deepcopy(currentNode)
    opponent = None
    if  current_move_taken == 1:
        opponent = 2
    elif  current_move_taken == 2:
        opponent = 1
    childNode = []
    for i in range(7):
        currentState =  checkPiece(i, opponent)
        if currentState != None:
            childNode.append( Board_used_in_current_game)
            Board_used_in_current_game = copy.deepcopy(node)
    return childNode

def alphaBeta( currentNode, alpha, beta, depth):  
    global Board_used_in_current_game
    value = -infinity
    childNode =  maxVal(currentNode)
    if childNode == [] or depth == 0:
        scoreCount()
        return  evalCalc(Board_used_in_current_game)
    else:
        for node in childNode:
            Board_used_in_current_game = copy.deepcopy(node)
            value = max(value,  betaAlpha(node, alpha, beta, depth - 1))
            if value >= beta:
                return value
            alpha = max(alpha, value)
        return value

def betaAlpha(currentNode, alpha, beta, depth): 
    global Board_used_in_current_game
    value = infinity
    childNode =  minVal(currentNode)
    if childNode == [] or depth == 0:
        scoreCount()
        return  evalCalc( Board_used_in_current_game)
    else:
        for node in childNode:
            Board_used_in_current_game = copy.deepcopy(node)
            value = min(value,  alphaBeta(node, alpha, beta, depth - 1))
            if value <= alpha:
                return value
            beta = min(beta, value)
    return value

def minMax( depth):  
    global Board_used_in_current_game
    currentState = copy.deepcopy( Board_used_in_current_game)
    for i in range(7):
        if  playPiece(i) != None:
            if  total_count_of_pieces == 42 or  total_depth_taken == 0:
                Board_used_in_current_game = copy.deepcopy(currentState)
                return i
            else:
                val =  betaAlpha( Board_used_in_current_game, -infinity, infinity, depth - 1)
                utilityVal[i] = val
                Board_used_in_current_game = copy.deepcopy(currentState)
    maxUtilityVal = max([i for i in utilityVal.values()])
    for i in range(7):
        if i in utilityVal:
            if utilityVal[i] == maxUtilityVal:
                utilityVal.clear()
                return i

def verticalCheck( row, column, state, streak):  
    consecutiveCount = 0
    for i in range(row, 6):
        if state[i][column] == state[row][column]:
            consecutiveCount += 1
        else:
            break
    if consecutiveCount >= streak:
        return 1
    else:
        return 0

def horizontalCheck( row, column, state, streak): 
    temp_count = 0
    for j in range(column, 7):
        if state[row][j] == state[row][column]:
            temp_count += 1
        else:
            break
    if temp_count >= streak:
        return 1
    else:
        return 0

def diagonalCheck( row, column, state, streak):  
    total = 0
    temp_count = 0
    temp_value_of_j = column
    for i in range(row, 6):
        if temp_value_of_j > 6:
            break
        elif state[i][temp_value_of_j] == state[row][column]:
            temp_count += 1
        else:
            break
        temp_value_of_j += 1
    if temp_count >= streak:
        total += 1
    temp_count = 0
    temp_value_of_j = column
    for i in range(row, -1, -1):
        if temp_value_of_j > 6:
            break
        elif state[i][temp_value_of_j] == state[row][column]:
            temp_count += 1
        else:
            break
        temp_value_of_j += 1
    if temp_count >= streak:
        total += 1
    return total

def streakCalc( state, color, streak):   
    temp_count = 0
    for i in range(6):
        for temp_value_of_j in range(7):
            if state[i][temp_value_of_j] == color:
                temp_count +=  verticalCheck(i, temp_value_of_j, state, streak)
                temp_count +=  horizontalCheck(i, temp_value_of_j, state, streak)
                temp_count +=  diagonalCheck(i, temp_value_of_j, state, streak)
    return temp_count

def playerEvalCalc( state):   
    playerFours =  streakCalc(state,  current_move_taken, 4)
    playerThrees =  streakCalc(state,  current_move_taken, 3)
    playerTwos =  streakCalc(state,  current_move_taken, 2)
    return (playerFours * 37044 + playerThrees * 882 + playerTwos * 21) 

def evalFunc():
    oneMoveColor = None
    if  current_move_taken == 1:
        oneMoveColor = 2
    elif  current_move_taken == 2:
        oneMoveColor = 1
    return oneMoveColor

def compEvalCalc( state):  
    oneMoveColor =  evalFunc()
    compFours =  streakCalc(state, oneMoveColor, 4)
    compThrees =  streakCalc(state, oneMoveColor, 3)
    compTwos =  streakCalc(state, oneMoveColor, 2)
    return (compFours * 37044 + compThrees * 882 + compTwos * 21)

def evalCalc( state):  
    return  playerEvalCalc(state) -  compEvalCalc(state)

def changeMove():  
    global current_move_taken
    if  current_move_taken == 1:
         current_move_taken = 2
    elif  current_move_taken == 2:
         current_move_taken = 1

def aiPlay():   
    randomCol =  minMax(int( total_depth_taken))
    result =  playPiece(randomCol)
    if not result:
        print('No Result')
    else:
        print('Player: %d, Column: %d\n' % ( current_move_taken, randomCol + 1))
        changeMove()

def scoreCount(): 
    global total_score_player_one
    global total_score_player_two
    total_score_player_one = 0;
    total_score_player_two = 0;

    for row in  Board_used_in_current_game:

        if row[0:4] == [1] * 4:
            total_score_player_one += 1
        if row[1:5] == [1] * 4:
            total_score_player_one += 1
        if row[2:6] == [1] * 4:
            total_score_player_one += 1
        if row[3:7] == [1] * 4:
            total_score_player_one += 1
  
        if row[0:4] == [2] * 4:
             total_score_player_two += 1
        if row[1:5] == [2] * 4:
             total_score_player_two += 1
        if row[2:6] == [2] * 4:
             total_score_player_two += 1
        if row[3:7] == [2] * 4:
             total_score_player_two += 1
 
    for j in range(7):

        if ( Board_used_in_current_game[0][j] == 1 and  Board_used_in_current_game[1][j] == 1 and  Board_used_in_current_game[2][j] == 1 and  Board_used_in_current_game[3][j] == 1):
             total_score_player_one += 1
        if ( Board_used_in_current_game[1][j] == 1 and  Board_used_in_current_game[2][j] == 1 and  Board_used_in_current_game[3][j] == 1 and  Board_used_in_current_game[4][j] == 1):
             total_score_player_one += 1
        if ( Board_used_in_current_game[2][j] == 1 and  Board_used_in_current_game[3][j] == 1 and  Board_used_in_current_game[4][j] == 1 and  Board_used_in_current_game[5][j] == 1):
             total_score_player_one += 1
 
        if ( Board_used_in_current_game[0][j] == 2 and  Board_used_in_current_game[1][j] == 2 and  Board_used_in_current_game[2][j] == 2 and  Board_used_in_current_game[3][j] == 2):
             total_score_player_two += 1
        if ( Board_used_in_current_game[1][j] == 2 and  Board_used_in_current_game[2][j] == 2 and  Board_used_in_current_game[3][j] == 2 and  Board_used_in_current_game[4][j] == 2):
             total_score_player_two += 1
        if ( Board_used_in_current_game[2][j] == 2 and  Board_used_in_current_game[3][j] == 2 and  Board_used_in_current_game[4][j] == 2 and  Board_used_in_current_game[5][j] == 2):
             total_score_player_two += 1

    if ( Board_used_in_current_game[2][0] == 1 and  Board_used_in_current_game[3][1] == 1 and  Board_used_in_current_game[4][2] == 1 and  Board_used_in_current_game[5][3] == 1):
         total_score_player_one += 1
    if ( Board_used_in_current_game[1][0] == 1 and  Board_used_in_current_game[2][1] == 1 and  Board_used_in_current_game[3][2] == 1 and  Board_used_in_current_game[4][3] == 1):
         total_score_player_one += 1
    if ( Board_used_in_current_game[2][1] == 1 and  Board_used_in_current_game[3][2] == 1 and  Board_used_in_current_game[4][3] == 1 and  Board_used_in_current_game[5][4] == 1):
         total_score_player_one += 1
    if ( Board_used_in_current_game[0][0] == 1 and  Board_used_in_current_game[1][1] == 1 and  Board_used_in_current_game[2][2] == 1 and  Board_used_in_current_game[3][3] == 1):
         total_score_player_one += 1
    if ( Board_used_in_current_game[1][1] == 1 and  Board_used_in_current_game[2][2] == 1 and  Board_used_in_current_game[3][3] == 1 and  Board_used_in_current_game[4][4] == 1):
         total_score_player_one += 1
    if ( Board_used_in_current_game[2][2] == 1 and  Board_used_in_current_game[3][3] == 1 and  Board_used_in_current_game[4][4] == 1 and  Board_used_in_current_game[5][5] == 1):
         total_score_player_one += 1
    if ( Board_used_in_current_game[0][1] == 1 and  Board_used_in_current_game[1][2] == 1 and  Board_used_in_current_game[2][3] == 1 and  Board_used_in_current_game[3][4] == 1):
         total_score_player_one += 1
    if ( Board_used_in_current_game[1][2] == 1 and  Board_used_in_current_game[2][3] == 1 and  Board_used_in_current_game[3][4] == 1 and  Board_used_in_current_game[4][5] == 1):
         total_score_player_one += 1
    if ( Board_used_in_current_game[2][3] == 1 and  Board_used_in_current_game[3][4] == 1 and  Board_used_in_current_game[4][5] == 1 and  Board_used_in_current_game[5][6] == 1):
         total_score_player_one += 1
    if ( Board_used_in_current_game[0][2] == 1 and  Board_used_in_current_game[1][3] == 1 and  Board_used_in_current_game[2][4] == 1 and  Board_used_in_current_game[3][5] == 1):
         total_score_player_one += 1
    if ( Board_used_in_current_game[1][3] == 1 and  Board_used_in_current_game[2][4] == 1 and  Board_used_in_current_game[3][5] == 1 and  Board_used_in_current_game[4][6] == 1):
         total_score_player_one += 1
    if ( Board_used_in_current_game[0][3] == 1 and  Board_used_in_current_game[1][4] == 1 and  Board_used_in_current_game[2][5] == 1 and  Board_used_in_current_game[3][6] == 1):
         total_score_player_one += 1
    if ( Board_used_in_current_game[0][3] == 1 and  Board_used_in_current_game[1][2] == 1 and  Board_used_in_current_game[2][1] == 1 and  Board_used_in_current_game[3][0] == 1):
         total_score_player_one += 1
    if ( Board_used_in_current_game[0][4] == 1 and  Board_used_in_current_game[1][3] == 1 and  Board_used_in_current_game[2][2] == 1 and  Board_used_in_current_game[3][1] == 1):
         total_score_player_one += 1
    if ( Board_used_in_current_game[1][3] == 1 and  Board_used_in_current_game[2][2] == 1 and  Board_used_in_current_game[3][1] == 1 and  Board_used_in_current_game[4][0] == 1):
         total_score_player_one += 1
    if ( Board_used_in_current_game[0][5] == 1 and  Board_used_in_current_game[1][4] == 1 and  Board_used_in_current_game[2][3] == 1 and  Board_used_in_current_game[3][2] == 1):
         total_score_player_one += 1
    if ( Board_used_in_current_game[1][4] == 1 and  Board_used_in_current_game[2][3] == 1 and  Board_used_in_current_game[3][2] == 1 and  Board_used_in_current_game[4][1] == 1):
         total_score_player_one += 1
    if ( Board_used_in_current_game[2][3] == 1 and  Board_used_in_current_game[3][2] == 1 and  Board_used_in_current_game[4][1] == 1 and  Board_used_in_current_game[5][0] == 1):
         total_score_player_one += 1
    if ( Board_used_in_current_game[0][6] == 1 and  Board_used_in_current_game[1][5] == 1 and  Board_used_in_current_game[2][4] == 1 and  Board_used_in_current_game[3][3] == 1):
         total_score_player_one += 1
    if ( Board_used_in_current_game[1][5] == 1 and  Board_used_in_current_game[2][4] == 1 and  Board_used_in_current_game[3][3] == 1 and  Board_used_in_current_game[4][2] == 1):
         total_score_player_one += 1
    if ( Board_used_in_current_game[2][4] == 1 and  Board_used_in_current_game[3][3] == 1 and  Board_used_in_current_game[4][2] == 1 and  Board_used_in_current_game[5][1] == 1):
         total_score_player_one += 1
    if ( Board_used_in_current_game[1][6] == 1 and  Board_used_in_current_game[2][5] == 1 and  Board_used_in_current_game[3][4] == 1 and  Board_used_in_current_game[4][3] == 1):
         total_score_player_one += 1
    if ( Board_used_in_current_game[2][5] == 1 and  Board_used_in_current_game[3][4] == 1 and  Board_used_in_current_game[4][3] == 1 and  Board_used_in_current_game[5][2] == 1):
         total_score_player_one += 1
    if ( Board_used_in_current_game[2][6] == 1 and  Board_used_in_current_game[3][5] == 1 and  Board_used_in_current_game[4][4] == 1 and  Board_used_in_current_game[5][3] == 1):
         total_score_player_one += 1

    if ( Board_used_in_current_game[2][0] == 2 and  Board_used_in_current_game[3][1] == 2 and  Board_used_in_current_game[4][2] == 2 and  Board_used_in_current_game[5][3] == 2):
         total_score_player_two += 1
    if ( Board_used_in_current_game[1][0] == 2 and  Board_used_in_current_game[2][1] == 2 and  Board_used_in_current_game[3][2] == 2 and  Board_used_in_current_game[4][3] == 2):
         total_score_player_two += 1
    if ( Board_used_in_current_game[2][1] == 2 and  Board_used_in_current_game[3][2] == 2 and  Board_used_in_current_game[4][3] == 2 and  Board_used_in_current_game[5][4] == 2):
         total_score_player_two += 1
    if ( Board_used_in_current_game[0][0] == 2 and  Board_used_in_current_game[1][1] == 2 and  Board_used_in_current_game[2][2] == 2 and  Board_used_in_current_game[3][3] == 2):
         total_score_player_two += 1
    if ( Board_used_in_current_game[1][1] == 2 and  Board_used_in_current_game[2][2] == 2 and  Board_used_in_current_game[3][3] == 2 and  Board_used_in_current_game[4][4] == 2):
         total_score_player_two += 1
    if ( Board_used_in_current_game[2][2] == 2 and  Board_used_in_current_game[3][3] == 2 and  Board_used_in_current_game[4][4] == 2 and  Board_used_in_current_game[5][5] == 2):
         total_score_player_two += 1
    if ( Board_used_in_current_game[0][1] == 2 and  Board_used_in_current_game[1][2] == 2 and  Board_used_in_current_game[2][3] == 2 and  Board_used_in_current_game[3][4] == 2):
         total_score_player_two += 1
    if ( Board_used_in_current_game[1][2] == 2 and  Board_used_in_current_game[2][3] == 2 and  Board_used_in_current_game[3][4] == 2 and  Board_used_in_current_game[4][5] == 2):
         total_score_player_two += 1
    if ( Board_used_in_current_game[2][3] == 2 and  Board_used_in_current_game[3][4] == 2 and  Board_used_in_current_game[4][5] == 2 and  Board_used_in_current_game[5][6] == 2):
         total_score_player_two += 1
    if ( Board_used_in_current_game[0][2] == 2 and  Board_used_in_current_game[1][3] == 2 and  Board_used_in_current_game[2][4] == 2 and  Board_used_in_current_game[3][5] == 2):
         total_score_player_two += 1
    if ( Board_used_in_current_game[1][3] == 2 and  Board_used_in_current_game[2][4] == 2 and  Board_used_in_current_game[3][5] == 2 and  Board_used_in_current_game[4][6] == 2):
         total_score_player_two += 1
    if ( Board_used_in_current_game[0][3] == 2 and  Board_used_in_current_game[1][4] == 2 and  Board_used_in_current_game[2][5] == 2 and  Board_used_in_current_game[3][6] == 2):
         total_score_player_two += 1
    if ( Board_used_in_current_game[0][3] == 2 and  Board_used_in_current_game[1][2] == 2 and  Board_used_in_current_game[2][1] == 2 and  Board_used_in_current_game[3][0] == 2):
         total_score_player_two += 1
    if ( Board_used_in_current_game[0][4] == 2 and  Board_used_in_current_game[1][3] == 2 and  Board_used_in_current_game[2][2] == 2 and  Board_used_in_current_game[3][1] == 2):
         total_score_player_two += 1
    if ( Board_used_in_current_game[1][3] == 2 and  Board_used_in_current_game[2][2] == 2 and  Board_used_in_current_game[3][1] == 2 and  Board_used_in_current_game[4][0] == 2):
         total_score_player_two += 1
    if ( Board_used_in_current_game[0][5] == 2 and  Board_used_in_current_game[1][4] == 2 and  Board_used_in_current_game[2][3] == 2 and  Board_used_in_current_game[3][2] == 2):
         total_score_player_two += 1
    if ( Board_used_in_current_game[1][4] == 2 and  Board_used_in_current_game[2][3] == 2 and  Board_used_in_current_game[3][2] == 2 and  Board_used_in_current_game[4][1] == 2):
         total_score_player_two += 1
    if ( Board_used_in_current_game[2][3] == 2 and  Board_used_in_current_game[3][2] == 2 and  Board_used_in_current_game[4][1] == 2 and  Board_used_in_current_game[5][0] == 2):
         total_score_player_two += 1
    if ( Board_used_in_current_game[0][6] == 2 and  Board_used_in_current_game[1][5] == 2 and  Board_used_in_current_game[2][4] == 2 and  Board_used_in_current_game[3][3] == 2):
         total_score_player_two += 1
    if ( Board_used_in_current_game[1][5] == 2 and  Board_used_in_current_game[2][4] == 2 and  Board_used_in_current_game[3][3] == 2 and  Board_used_in_current_game[4][2] == 2):
         total_score_player_two += 1
    if ( Board_used_in_current_game[2][4] == 2 and  Board_used_in_current_game[3][3] == 2 and  Board_used_in_current_game[4][2] == 2 and  Board_used_in_current_game[5][1] == 2):
         total_score_player_two += 1
    if ( Board_used_in_current_game[1][6] == 2 and  Board_used_in_current_game[2][5] == 2 and  Board_used_in_current_game[3][4] == 2 and  Board_used_in_current_game[4][3] == 2):
         total_score_player_two += 1
    if ( Board_used_in_current_game[2][5] == 2 and  Board_used_in_current_game[3][4] == 2 and  Board_used_in_current_game[4][3] == 2 and  Board_used_in_current_game[5][2] == 2):
         total_score_player_two += 1
    if ( Board_used_in_current_game[2][6] == 2 and  Board_used_in_current_game[3][5] == 2 and  Board_used_in_current_game[4][4] == 2 and  Board_used_in_current_game[5][3] == 2):
         total_score_player_two += 1    

def humanPlay(Board_used_in_current_game):    
    global current_game_file
    while  get_total_check_Piece_Count() != 42:  
        print(" Human will play it") 
        print("*************")
        UsersMove = int(input("Enter a column number (1-7): "))  
        if not 0 < UsersMove < 8:    
            print("Column invalid! Enter Again.")
            continue
        if not  playPiece(UsersMove - 1):
            print("Column number: %d is full. Try other column." % UsersMove)
            continue
        print("Your made move: " + str(UsersMove))
        displayGB()   
        current_game_file = open("human_out.txt", 'w')  
        print_the_game_board_to_file()
        current_game_file.close()  
        if  get_total_check_Piece_Count() == 42:    
            print("No more moves left, Game Over!")
            scoreCount() 
            print('Score: PlayerA = %d, PlayerB = %d\n' % ( total_score_player_one,  total_score_player_two))
            break
        else:   
            print("Computer is computing based on next " + str( total_depth_taken) + " steps...")
            changeMove()  
            aiPlay() 
            displayGB()  
            current_game_file = open('computer_out.txt', 'w') 
            print_the_game_board_to_file()
            current_game_file.close()  
            scoreCount()  
            print('Score: PlayerA = %d, PlayerB = %d\n' % ( total_score_player_one,  total_score_player_two))

def interactiveMode(Board_used_in_current_game, nextPlayer):  
    global current_game_file
    print('State of board (current)')
    displayGB()  
    scoreCount()  
    print('Score: PlayerA = %d, PlayerB = %d\n' % ( total_score_player_one,  total_score_player_two))
    if nextPlayer == 'human_next': 
        humanPlay(Board_used_in_current_game)    
    else:
        aiPlay()
        current_game_file = open('computer_out.txt', 'w') 
        print_the_game_board_to_file()
        current_game_file.close()  
        displayGB()   
        scoreCount() 
        print('Score: PlayerA = %d, PlayerB = %d\n' % ( total_score_player_one,  total_score_player_two))
        humanPlay(Board_used_in_current_game)

    if  get_total_check_Piece_Count() == 42: 
        if  total_score_player_one >  total_score_player_two:
            print("Player 1 wins")
        if  total_score_player_one ==  total_score_player_two:
            print("The game is a Tie")
        if  total_score_player_one <  total_score_player_two:
            print("Player 2 wins")
        print("Game Over")


def oneMoveMode(Board_used_in_current_game):  
    if  total_count_of_pieces >= 42:  
        print('Game board is full !\n Game Over...')
        sys.exit(0)
    print ('Board_used_in_current_game state before move:')
    displayGB()  
    aiPlay()      
    print ('Board_used_in_current_game state after move:')
    displayGB()   
    scoreCount() 
    print('Score: PlayerA = %d, PlayerB = %d\n' % ( total_score_player_one,  total_score_player_two))
    print_the_game_board_to_file()   
    current_game_file.close() 

def main(argv):  
    global Board_used_in_current_game
    global current_move_taken
    global total_score_player_one
    global total_score_player_two
    global current_game_file 
    global total_depth_taken 
    current_game_file = open(argv[2], 'r')    
    fileLines = current_game_file.readlines()
    Board_used_in_current_game = [[int(char) for char in line[0:7]] for line in fileLines[0:-1]]
    current_move_taken = int(fileLines[-1][0])
    current_game_file.close()
    total_check_Piece_Count()     
    total_depth_taken = argv[4]  
    if argv[1] == 'one-move':   
        try:
             current_game_file = open(argv[3], 'w')
        except:
            sys.exit('Error while opening output file.')
        oneMoveMode(Board_used_in_current_game)
    else:  
        interactiveMode(Board_used_in_current_game, argv[3])

main(sys.argv)