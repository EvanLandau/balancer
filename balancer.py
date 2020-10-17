import molecules
import sympy
import fractions
import argparse

def balancer(left_side, right_side): #Algorithm based on: http://www.logical.ai/chemistry/html/chem-nullspace.html
    """Takes in left_side, which is a list of tuples (left side is number of molecules (0 if unknown), right side is the molecule itself)."""
    #Test to ensure each side has the same elements
    left_element_list = []
    for mol in left_side: #Loads atoms into list
        for atom in mol[1].atoms:
            if atom[0] not in left_element_list:
                left_element_list.append(atom[0])
    right_element_list = []
    for mol in right_side: #Loads atoms into other list
        for atom in mol[1].atoms:
            if atom[0] not in right_element_list:
                right_element_list.append(atom[0])
    left_element_list.sort() #Sorts lists into order (so they can be compared)
    right_element_list.sort()
    if left_element_list != right_element_list:
        raise Exception("Different elements on left and right side of chemical equation")
    molecule_list = left_side + right_side
    #Create array
    element_matrix = sympy.zeros(len(left_element_list), len(left_side) + len(right_side))
    for i in range(0, len(molecule_list)):
        for atom in molecule_list[i][1].atoms:
            element_matrix[left_element_list.index(atom[0]), i] = atom[1] #Uses the left side list to determine the order that different elements go into the matrix- it is arbitrary, as long as it is consistent
    element_matrix = element_matrix.T
    element_matrix = sympy.BlockMatrix([element_matrix, sympy.eye(len(left_side + right_side))], axis=1)
    element_matrix_rref = sympy.Matrix(element_matrix).rref()
    solution_list = []
    for i in range(0, element_matrix_rref[0].shape[0]): #Loop through list, and test if ansewers are solutions according to the algorithm (i.e. their pivots are further right than the number of atoms added)
        if element_matrix_rref[1][i] >= len(left_element_list):
            solution_list.append(sympy.Matrix(element_matrix_rref[0].row(i)))
    if len(solution_list) == 0:
        return None
    #Make negatives positive
    for solution in solution_list:
        for i in range(0, len(solution)):
                if solution[i] < 0:
                    solution[i] = solution[i] * -1
    #Turn fractions into whole numbers
    for i in range(0, len(solution_list)):
        while True:
            largest_denominator = 1 #Finds largest denominator, then multiplies by that until all denominators are 1
            for j in range(0, solution_list[i].shape[1]):
                if solution_list[i][j].q != 1:
                    if solution_list[i][j].q > largest_denominator:
                        largest_denominator = solution_list[i][j].q
            if largest_denominator != 1:
                solution_list[i] = solution_list[i] * largest_denominator
            else:
                break
    solution = solution_list[0].tolist()[0] #Convert to list
    solution = solution[len(left_element_list):]
    return solution

#Get command line arguments - should be unified into one file with other functions, once other modules are developed
parser = argparse.ArgumentParser(description='Balances a provided chemical equation')
parser.add_argument('equation', metavar='equation', type=str, help='Chemical equation to be balanced. Should include one of <-, ->, or <->. For unknown numbers of molecules, enter 0 before the molecule.')

args = parser.parse_args()

equation = args.equation.upper()
equation = equation.split() #Separate each group into its own thing
#Find arrow
for i in range(0, len(equation)):
    if equation[i] == '<-' or equation[i] ==  '->' or equation[i] == '<->':
        divider = i
        break
else:
    raise Exception('No divider in chemical equation')

left_molecules = []
right_molecules = []
for group in equation[0:divider]:
    if not group.isalnum():
        raise Exception('Molecule formula contains non-alphanumeric characters')
    if group[0].isalpha():
        left_molecules.append((1, molecules.molecule(group)))
    else: #TODO: Get any number of numbers at beginning of molecule
        left_molecules.append((int(group[0]), molecules.molecule(group[1:])))

for group in equation[divider+1:]:
    if not group.isalnum():
        raise Exception('Molecule formula contains non-alphanumeric characters')
    if group[0].isalpha():
        right_molecules.append((1, molecules.molecule(group)))
    else:
        right_molecules.append((int(group[0]), molecules.molecule(group[1:])))

solution = balancer(left_molecules, right_molecules)
if solution == None:
    print('No valid solutions to chemical equation found.')
else:
    solution.insert(divider, '')
    for i in range(0, len(solution)):
        if equation[i][0].isalpha():
            equation[i] = str(solution[i]) + equation[i]
    print(' '.join(equation))