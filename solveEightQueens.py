import random
import copy
from optparse import OptionParser
import util

class SolveEightQueens:
    def __init__(self, numberOfRuns, verbose, lectureExample):
        """
        Value 1 indicates the position of queen
        """
        self.numberOfRuns = numberOfRuns
        self.verbose = verbose
        self.lectureCase = [[]]
        if lectureExample:
            self.lectureCase = [
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 1, 0, 0, 0, 0],
            [1, 0, 0, 0, 1, 0, 0, 0],
            [0, 1, 0, 0, 0, 1, 0, 1],
            [0, 0, 1, 0, 0, 0, 1, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            ]
    def solve(self):
        solutionCounter = 0
        for i in range(self.numberOfRuns):
            if self.search(Board(self.lectureCase), self.verbose).getNumberOfAttacks() == 0:
                solutionCounter += 1
        print("Solved: %d/%d" % (solutionCounter, self.numberOfRuns))

    def search(self, board, verbose):
        """
        Hint: Modify the stop criterion in this function
        """
        newBoard = board
        i = 0
        while True:
            if verbose:
                print("iteration %d" % i)
                print(newBoard.toString())
                print("# attacks: %s" % str(newBoard.getNumberOfAttacks()))
                print(newBoard.getCostBoard().toString(True))
            currentNumberOfAttacks = newBoard.getNumberOfAttacks()
            (newBoard, newNumberOfAttacks, newRow, newCol) = newBoard.getBetterBoard()
            i += 1
            if(newNumberOfAttacks == 0):
                break
            if(i > 100):
                if currentNumberOfAttacks <= newNumberOfAttacks:
                    break
        return newBoard

class Board:
    def __init__(self, squareArray = [[]]):
        if squareArray == [[]]:
            self.squareArray = self.initBoardWithRandomQueens()
        else:
            self.squareArray = squareArray

    @staticmethod
    def initBoardWithRandomQueens():
        tmpSquareArray = [[ 0 for i in range(8)] for j in range(8)]
        for i in range(8):
            tmpSquareArray[random.randint(0,7)][i] = 1
        return tmpSquareArray

    def toString(self, isCostBoard=False):
        """
        Transform the Array in Board or cost Board to printable string
        """
        s = ""
        for i in range(8):
            for j in range(8):
                if isCostBoard: # Cost board
                    cost = self.squareArray[i][j]
                    s = (s + "%3d" % cost) if cost < 9999 else (s + "  q")
                else: # Board
                    s = (s + ". ") if self.squareArray[i][j] == 0 else (s + "q ")
            s += "\n"
        return s

    def getCostBoard(self):
        """
        First Initalize all the cost as 9999.
        After filling, the position with 9999 cost indicating the position of queen.
        """
        costBoard = Board([[ 9999 for i in range(8)] for j in range(8)])
        for r in range(8):
            for c in range(8):
                if self.squareArray[r][c] == 1:
                    for rr in range(8):
                        if rr != r:
                            testboard = copy.deepcopy(self)
                            testboard.squareArray[r][c] = 0
                            testboard.squareArray[rr][c] = 1
                            costBoard.squareArray[rr][c] = testboard.getNumberOfAttacks()
        return costBoard

    def getBetterBoard(self):
        """
        "*** YOUR CODE HERE ***"
        This function should return a tuple containing containing four values
        the new Board object, the new number of attacks,
        the Column and Row of the new queen
        For exmaple:
            return (betterBoard, minNumOfAttack, newRow, newCol)
        The datatype of minNumOfAttack, newRow and newCol should be int
        """
        minNumOfAttack = self.getCostBoard().squareArray[0][0]
        pos = []
        for i in range(8):
            for j in range(8):
                if(self.getCostBoard().squareArray[i][j] <= minNumOfAttack):#Gets least number of attacks
                    if(self.getCostBoard().squareArray[i][j] == minNumOfAttack): #If they are the same, adds to list.
                        newRow = i
                        newCol = j
                        minNumOfAttack = self.getCostBoard().squareArray[i][j]
                        pos.append([newRow, newCol, minNumOfAttack])
                    if(self.getCostBoard().squareArray[i][j] < minNumOfAttack):#If not the same, the minNumOfAttack is updated
                        newRow = i
                        newCol = j
                        minNumOfAttack = self.getCostBoard().squareArray[i][j]
                        pos = [[newRow, newCol, minNumOfAttack]]
        c = pos[random.randint(0, len(pos)-1)]
        Row = c[0]
        Col = c[1]
        for i in range(8):
            if(self.squareArray[i][Col] == 1):
                self.squareArray[i][Col] = 0
                break
        self.squareArray[Row][Col] = 1
        betterBoard = self
        return(betterBoard, minNumOfAttack, Row, Col)

    def getNumberOfAttacks(self):
        """
        "*** YOUR CODE HERE ***"
        This function should return the number of attacks of the current board
        The datatype of the return value should be int
        """
        #Gets a list of queens and then checks if there are attacks horizontally and vertically.
        counter = 0
        for i in range(8):
            temp_row = row_queens = temp_diag = temp_diag2 = 0
            for j in range(8):
                if(self.squareArray[i][j] == 1):
                    row_queens = row_queens + 1
                    if(row_queens > 1):
                        temp_row = temp_row + (row_queens-1)
                    diag_queens1 = 0
                    #Checks for diagonal queens throughout the chess baord.
                    for k in range(max(i,j), 8):
                        if(i>=j):
                            y_val = j + k - i
                            x_val = k
                        else:
                            y_val = k
                            x_val = i + k - j
                        if(self.squareArray[x_val][y_val] == 1):
                            diag_queens1 = diag_queens1 + 1
                            if(diag_queens1 > 1):
                                temp_diag = temp_diag + 1
                    diag_queens2 = 0
                    if((i+j)<7):
                        temp = i
                    for k in range(i, -1, -1):
                        y_val = j + i - k
                        x_val = k
                        if(y_val <= 7 and self.squareArray[x_val][y_val] == 1):
                            diag_queens2 = diag_queens2 + 1
                            if(diag_queens2 > 1):
                                temp_diag2 = temp_diag2 + 1
            counter = counter + temp_row + temp_diag + temp_diag2
        return(counter)

if __name__ == "__main__":
    #Enable the following line to generate the same random numbers (useful for debugging)
    random.seed(1)
    parser = OptionParser()
    parser.add_option("-q", dest="verbose", action="store_false", default=True)
    parser.add_option("-l", dest="lectureExample", action="store_true", default=False)
    parser.add_option("-n", dest="numberOfRuns", default=1, type="int")
    (options, args) = parser.parse_args()
    EightQueensAgent = SolveEightQueens(verbose=options.verbose, numberOfRuns=options.numberOfRuns, lectureExample=options.lectureExample)
    EightQueensAgent.solve()
