  # -*- coding: latin-1 -*-
import random
from Player import *
from Constants import *
from Construction import CONSTR_STATS
from Ant import UNIT_STATS
from Move import Move
from GameState import addCoords
from AIPlayerUtils import *


##
#AIPlayer
#Description: The responsbility of this class is to interact with the game by
#deciding a valid move based on a given game state. This class has methods that
#will be implemented by students in Dr. Nuxoll's AI course.
#
#Variables:
#   playerId - The id of the player.
##
class AIPlayer(Player):

    #__init__
    #Description: Creates a new Player
    #
    #Parameters:
    #   inputPlayerId - The id to give the new player (int)
    ##
    def __init__(self, inputPlayerId):
        super(AIPlayer,self).__init__(inputPlayerId, "The Ultimate AI")
    
    ##
    #getPlacement
    #Description: The getPlacement method corresponds to the 
    #action taken on setup phase 1 and setup phase 2 of the game. 
    #In setup phase 1, the AI player will be passed a copy of the 
    #state as currentState which contains the board, accessed via 
    #currentState.board. The player will then return a list of 10 tuple 
    #coordinates (from their side of the board) that represent Locations 
    #to place the anthill and 9 grass pieces. In setup phase 2, the player 
    #will again be passed the state and needs to return a list of 2 tuple
    #coordinates (on their opponent’s side of the board) which represent
    #Locations to place the food sources. This is all that is necessary to 
    #complete the setup phases.
    #
    #Parameters:
    #   currentState - The current state of the game at the time the Game is 
    #       requesting a placement from the player.(GameState)
    #
    #Return: If setup phase 1: list of ten 2-tuples of ints -> [(x1,y1), (x2,y2),…,(x10,y10)]
    #       If setup phase 2: list of two 2-tuples of ints -> [(x1,y1), (x2,y2)]
    ##
    def getPlacement(self, currentState):
        numToPlace = 0
        moves = []
        if currentState.phase == SETUP_PHASE_1:    #Our side
            move = None
            while move == None:
                #Choose an anthill x location
                x = 2
                #Choose a tunnel y location
                y = 1
                #Set the move if this space is empty
                if currentState.board[x][y].constr == None and (x, y) not in moves:
                    move = (x, y)
                    #Just need to make the space non-empty. So I threw whatever I felt like in there.
                    currentState.board[x][y].constr == True
            moves.append(move)
            move = None
            while move == None:
                #Choose a tunnel x location
                x = 8
                #Choose a tunnel y location
                y = 1
                if currentState.board[x][y].constr == None and (x,y) not in moves:
                    move = (x, y)
                    currentState.board[x][y].constr == True
                moves.append(move)
            for i in range(0,9):
                move = None
                x = i
                y = 3
                while move == None:
                    if currentState.board[x][y].constr == None and (x,y) not in moves:
                        move = (x, y)
                        currentState.board[x][y].constr == True
                    moves.append(move)
            return moves
        elif currentState.phase == SETUP_PHASE_2:   #Oppenents side
            numToPlace = 2
            moves = []

            move = None

            #Search for enemy anthill and tunnel
            oppId = None
            if(self.playerId == PLAYER_ONE):
                oppId = PLAYER_TWO
            else:
                oppId = PLAYER_ONE
            anthillLoc = getConstrList(currentState, oppId, [ANTHILL])
            tunnelLoc = getConstrList(currentState, oppId, [TUNNEL])
            listOfHill = []
            listOfTunnel = []
            for x in range(0, 10):
                for y in range(6,10):
                    stepsFromHill = stepsToReach(currentState, (x,y), anthillLoc[0].coords)
                    stepsFromTunnel = stepsToReach(currentState, (x,y), tunnelLoc[0].coords)
                    listOfHill.append((stepsFromHill,(x,y)))
                    listOfTunnel.append((stepsFromTunnel, (x,y)))
            listOfHill.sort(key=lambda tup: tup[0], reverse=True)#Snippit used from other team. Needed help sorting
            listOfTunnel.sort(key=lambda tup: tup[0], reverse=True)
            foodTile2 = listOfTunnel[1]
            curInt = 1
            while True:
                foodTile1 = listOfHill[curInt]
                if legalCoord(foodTile1[1]) and getConstrAt(currentState, foodTile1[1]) == None:
                    break
                else:
                    curInt += 1
            foodCoord1 = foodTile1[1]
            curInt = 1
            while True:
                foodTile2 = listOfTunnel[curInt]
                if foodTile2[1] == foodCoord1:
                    curInt += 1
                elif legalCoord(foodTile2[1]) and getConstrAt(currentState, foodTile2[1]) == None:
                    break
                else:
                    curInt += 1
            foodCoord2 = foodTile2[1]


            moves.append(foodCoord1)
            moves.append(foodCoord2)

            return moves
        else:
            return [(0, 0)]
    
    ##
    #getMove
    #Description: The getMove method corresponds to the play phase of the game 
    #and requests from the player a Move object. All types are symbolic 
    #constants which can be referred to in Constants.py. The move object has a 
    #field for type (moveType) as well as field for relevant coordinate 
    #information (coordList). If for instance the player wishes to move an ant, 
    #they simply return a Move object where the type field is the MOVE_ANT constant 
    #and the coordList contains a listing of valid locations starting with an Ant 
    #and containing only unoccupied spaces thereafter. A build is similar to a move 
    #except the type is set as BUILD, a buildType is given, and a single coordinate 
    #is in the list representing the build location. For an end turn, no coordinates 
    #are necessary, just set the type as END and return.
    #
    #Parameters:
    #   currentState - The current state of the game at the time the Game is 
    #       requesting a move from the player.(GameState)   
    #
    #Return: Move(moveType [int], coordList [list of 2-tuples of ints], buildType [int]
    ##
    def getMove(self, currentState):
        myId = self.playerId
        foodCoords = []
        buildingList = []
        constrList = getConstrList(currentState, None)
        for constr in constrList:
            if constr.type == FOOD:
                foodCoords.append(constr.coords)
            elif constr.type == TUNNEL:
                buildingList.append(constr.coords)
            elif constr.type == ANTHILL:
                buildingList.append(constr.coords)



        buildMoves = listAllBuildMoves(currentState)
        workAntList = getAntList(currentState, self.playerId, [WORKER])
        queenAntList = getAntList(currentState, self.playerId, [QUEEN])
        if len(workAntList) < 1:
            return buildMoves[0]
        antMoveList = []
        goFor = None
        for ant in queenAntList:
            for i in range (0, len(buildingList)):
                if getConstrAt(currentState, ant.coords) and getConstrAt(currentState, ant.coords).type == ANTHILL:
                    possibleMoves = listAllMovementPaths(currentState, ant.coords, 2)
                    queenMove = Move(MOVE_ANT, possibleMoves[0], None)
                    return queenMove
        for ant in workAntList:
            if ant.hasMoved: continue
            elif ant.type == WORKER:
                possibleMoves = listAllMovementPaths(currentState, ant.coords, 2)
                if not ant.carrying:
                    steps = 0
                    for i in range(0, 4):
                        steps = stepsToReach(currentState, ant.coords, foodCoords[i])
                        antMoveList.append(steps)
                    if antMoveList[0] <= antMoveList[1]:
                        goFor = 0
                    else:
                        goFor = 1
                    currentBestMove = -1
                    for move in range(0,len(possibleMoves)):
                        for move2 in possibleMoves[move]:
                            if stepsToReach(currentState, move2, foodCoords[goFor]) < steps:
                                currentBestMove = move
                                steps = stepsToReach(currentState, move2, foodCoords[goFor])
                    makeMove = []
                    #for move in range(1,len(possibleMoves[currentBestMove])):
                    #    makeMove.append(possibleMoves[currentBestMove][move])
                    bestMove = Move(MOVE_ANT, possibleMoves[currentBestMove], None)

                    return bestMove
                else:
                    steps = 0
                    for i in range(0, 4):
                        steps = stepsToReach(currentState, ant.coords, buildingList[i])
                        antMoveList.append(steps)
                    if antMoveList[2] <= antMoveList[3]:
                        goFor = 2
                    else:
                        goFor = 3
                    currentBestMove = -1
                    for move in range(0, len(possibleMoves)):
                        for move2 in possibleMoves[move]:
                            if stepsToReach(currentState, move2, buildingList[goFor]) < steps:
                                currentBestMove = move
                                steps = stepsToReach(currentState, move2, buildingList[goFor])
                    makeMove = 0
                    bestMove = Move(MOVE_ANT, possibleMoves[currentBestMove], None)
                    return bestMove
        return Move(END, None, None)

    
    ##
    #getAttack
    #Description: The getAttack method is called on the player whenever an ant completes 
    #a move and has a valid attack. It is assumed that an attack will always be made 
    #because there is no strategic advantage from withholding an attack. The AIPlayer 
    #is passed a copy of the state which again contains the board and also a clone of 
    #the attacking ant. The player is also passed a list of coordinate tuples which 
    #represent valid locations for attack. Hint: a random AI can simply return one of 
    #these coordinates for a valid attack. 
    #
    #Parameters:
    #   currentState - The current state of the game at the time the Game is requesting 
    #       a move from the player. (GameState)
    #   attackingAnt - A clone of the ant currently making the attack. (Ant)
    #   enemyLocation - A list of coordinate locations for valid attacks (i.e. 
    #       enemies within range) ([list of 2-tuples of ints])
    #
    #Return: A coordinate that matches one of the entries of enemyLocations. ((int,int))
    ##
    def getAttack(self, currentState, attackingAnt, enemyLocations):
        return enemyLocations[random.randint(0, len(enemyLocations) - 1)]
        
    ##
    #registerWin
    #Description: The last method, registerWin, is called when the game ends and simply 
    #indicates to the AI whether it has won or lost the game. This is to help with 
    #learning algorithms to develop more successful strategies.
    #
    #Parameters:
    #   hasWon - True if the player has won the game, False if the player lost. (Boolean)
    #
    def registerWin(self, hasWon):
        #method templaste, not implemented
        pass
