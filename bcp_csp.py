from constraint import *
import operator
class BlockCSP:
    def __init__(self,readingFile):
        pass
        self.readingFile = readingFile
        self.variables = dict()
        self.IsSolutionFeasible = True
        self.ActualSolution = dict()
        
    def readFile(self):
        """
        Input Format:
            Second Line     : Number of Vertical Block
            Third Line      : Number of Horizontal Block
            Other Lines     : UniqueNameOfBlock,X-Coordinate,Y-Coordinate
                              Example: V1,2,3
                              V standsfor Vertical. X = 2 and Y =3 
        """
        file = open(self.readingFile,"r")
        lines = file.readlines()
        self.numberOfVerticalBlock = int(lines[0].rstrip('\n'))
        self.numberOfHorizontalBlock = int(lines[1].rstrip('\n'))
        for i in range(2,len(lines)):
            line_val = lines[i].rstrip('\n')
            if(len(line_val)>=5):
                line = line_val.split(',')
                self.variables[line[0]] = (int(line[1]),int(line[2]))
    def constructBoard(self):
        max_x_axis = 3*self.numberOfHorizontalBlock+self.numberOfVerticalBlock - 1 
        max_y_axis = 3*self.numberOfVerticalBlock+self.numberOfHorizontalBlock - 1
        self.max_x_axis = max_x_axis
        self.max_y_axis = max_y_axis
        self.board = []
        for i in range(max_y_axis):
            self.board.append(['__']*max_x_axis)

    #şuan bu kısım eksik            
    def placedBlocksView(self):
        for key,value in self.variables.items():
            print(key," and ",value)

    def printBoardState(self):
        for i in range(len(self.board)):
            for k in range(len(self.board[0])):
                print(self.board[i][k],end=" ")
            print("") #new line
    def printSolution(self):
        if (self.IsSolutionFeasible == True):
            self.ActualSolution = sorted(self.ActualSolution.items(), key=lambda x: x[1])
            for val in self.ActualSolution:
                print(val[0]," - ",val[1])
        else:
            print("There is no solution.")


    def constructConstraints(self,problem):

        possible_value_list = []
        for i in range(len(self.variables.keys())):
            possible_value_list.append(i+1)

        problem.addVariables(self.variables.keys(),possible_value_list)

        possible_1H_2V_case_list = []
        possible_1H_2V_case_supported_middle = False

        # All variables should be unique value in the final result
        problem.addConstraint(AllDifferentConstraint())
        for keyA,valueA in self.variables.items():
            key_a_type = keyA[0]
            key_a_x_position = valueA[0]
            key_a_y_position = valueA[1]
            for keyB,valueB in self.variables.items():
                if keyA == keyB:
                    continue

                key_b_type = keyB[0]
                key_b_x_position = valueB[0]
                key_b_y_position = valueB[1]

                if( ((key_a_type != "H") or (key_b_type != "V")) and (key_a_y_position < key_b_y_position)):
                    problem.addConstraint(lambda a, b: a < b, [keyA,keyB])
                # Case: Horizontal block can be supported by two vertical block 
                if ((key_a_type == "H") and (key_b_type == "V") and (key_a_y_position - (key_b_y_position + 3) == 0) and ((key_a_x_position + 1) != key_b_x_position) and ((key_a_x_position == key_b_x_position or (key_a_x_position+2) == key_b_x_position))):
                    possible_1H_2V_case_list.clear()
                    for keyC,valueC in self.variables.items():
                        possible_1H_2V_case_supported_middle = False
                        key_c_type = keyC[0]
                        key_c_x_position = valueC[0]
                        key_c_y_position = valueC[1]
                        if((key_c_type == "H" and key_a_type == "H") and ( (key_a_y_position - key_c_y_position) == 1 ) and (abs(key_a_x_position - key_c_x_position) <= 1 )):
                            possible_1H_2V_case_list.clear()
                            possible_1H_2V_case_supported_middle = True
                            break

                        if (key_a_y_position - (key_c_y_position + 3) != 0):
                            continue
                        if ((key_a_x_position+1) == key_c_x_position):
                            possible_1H_2V_case_list.clear()
                            possible_1H_2V_case_supported_middle = True
                            break
                        if(key_c_x_position == key_a_x_position or (key_a_x_position+2) == key_c_x_position):
                            possible_1H_2V_case_list.append(keyC)
                            
                    if(possible_1H_2V_case_supported_middle == False and len(possible_1H_2V_case_list) != 2):
                        self.IsSolutionFeasible = False
                        return
                    elif (possible_1H_2V_case_supported_middle == False and len(possible_1H_2V_case_list) == 2):
                        problem.addConstraint(lambda a, b: a > b, [keyA,possible_1H_2V_case_list[0]])
                        problem.addConstraint(lambda a, b: a > b, [keyA,possible_1H_2V_case_list[1]])
        
        
        self.ActualSolution = problem.getSolution()
        self.OtherFeasibleSolutions = problem.getSolutions()

if __name__=="__main__":
    print("Main Started")
    problem = Problem(BacktrackingSolver())
    bcp_csp = BlockCSP("input_figure_1.txt")
    bcp_csp.readFile()
    bcp_csp.constructBoard()
    bcp_csp.constructConstraints(problem)
    bcp_csp.printSolution()

    
    print("Main Ended")