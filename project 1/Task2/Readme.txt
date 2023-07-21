

What Programming Language is used:
Python Programming

How the code is structured:
1. total_check_Piece_Count() - Counts total pieces and save in class object. 
2. displayGB() - Function to display the current state of the board. 
3. print_the_game_board_to_file() - Function to save the current going board to file.
4. get_total_check_Piece_Count() - Function to pick the total count of pieces.
5. playPiece() - Function to make move. 
6. checkPiece() - Function to check the possibility of the move. 
7. maxVal() - Function to find max value. 
8. minVal() - Function to find min value. 
9. alphaBeta() - Function to check the best move and its position. 
10. betaAlpha() - Function to check the best move possible. 
11. minMax() - Gives the minmax value. 
12. verticalCheck() - Checks the streak vertically. 
13. horizontalCheck() - Function to check horizontal streaks. 
14. diagonalCheck() - Functions to check diagonal streak. 
15. streakCalc() - Function to find steak calculation. 
16. playerEvalCalc() - Function to check parameter for player move. 
17. evalFunc() - Final evaluation of parameters behind best move. 
18. compEvalCalc() - Function to check parameters of computer move. 
19. evalCalc() - Function to find the 
20. changeMove() - Function to change the mover after move. 
21. aiPlay() - Function to start the AI move. 
22. scoreCount() - Function to check total score on that moment. 
23. humanPlay() - Function to start a human move. 
24. interactiveMode() - Function to enter into interactive mode of game. 
25. oneMoveMode() - Function to enter into one move mode of the game.
26. main() - Main driver code.

How to run the code:

1.Open Terminal
2.Path should be set to the folder Task2

 -For Interactive Mode use commands
	-> python maxconnect4.py interactive input1.txt human_next 3
	-> python maxconnect4.py interactive input1.txt computer_next 3
 -For One-Move Mode use commands
	-> python maxconnect4.py one-move input1.txt output1.txt 2