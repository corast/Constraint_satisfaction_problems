#!/usr/bin/python

import copy
import itertools
import types

class CSP:
    def __init__(self):
        # self.variables is a list of the variable names in the CSP
        self.variables = []

        # self.domains[i] is a list of legal values for variable i
        self.domains = {}

        # self.constraints[i][j] is a list of legal value pairs for
        # the variable pair (i, j)
        self.constraints = {}

    def add_variable(self, name, domain):
        """Add a new variable to the CSP. 'name' is the variable name
        and 'domain' is a list of the legal values for the variable.
        """
        self.variables.append(name)
        self.domains[name] = list(domain)
        self.constraints[name] = {}

    def get_all_possible_pairs(self, a, b):
        """Get a list of all possible pairs (as tuples) of the values in
        the lists 'a' and 'b', where the first component comes from list
        'a' and the second component comes from list 'b'.
        """
        return itertools.product(a, b)

    def get_all_possible_pairs_as_list(self, a, b):
        """Get a list of all possible pairs (as tuples) of the values of
        a and b, where the first component comes from list/value
        'a' and the second component comes from list 'b'.
        """
        #need to check if a is a string value or a list of one elements.
        if isinstance(a,types.StringTypes):
            return list(itertools.product([a], b)) 
        return list(itertools.product(a, b)) 


    def get_all_arcs(self):
        """Get a list of all arcs/constraints that have been defined in
        the CSP. The arcs/constraints are represented as tuples (i, j),
        indicating a constraint between variable 'i' and 'j'.
        """
        return [ (i, j) for i in self.constraints for j in self.constraints[i] ]

    def get_all_neighboring_arcs(self, var):
        """Get a list of all arcs/constraints going to/from variable
        'var'. The arcs/constraints are represented as in get_all_arcs().
        """
        return [ (i, var) for i in self.constraints[var] ]

    def add_constraint_one_way(self, i, j, filter_function):
        """Add a new constraint between variables 'i' and 'j'. The legal
        values are specified by supplying a function 'filter_function',
        that returns True for legal value pairs and False for illegal
        value pairs. This function only adds the constraint one way,
        from i -> j. You must ensure that the function also gets called
        to add the constraint the other way, j -> i, as all constraints
        are supposed to be two-way connections!
        """
        if not j in self.constraints[i]:
            # First, get a list of all possible pairs of values between variables i and j
            self.constraints[i][j] = self.get_all_possible_pairs(self.domains[i], self.domains[j])

        # Next, filter this list of value pairs through the function
        # 'filter_function', so that only the legal value pairs remain
        self.constraints[i][j] = filter(lambda value_pair: filter_function(*value_pair), self.constraints[i][j])

    def add_all_different_constraint(self, variables):
        """Add an Alldiff constraint between all of the variables in the
        list 'variables'.
        """
        for (i, j) in self.get_all_possible_pairs(variables, variables):
            if i != j:
                self.add_constraint_one_way(i, j, lambda x, y: x != y)

    def backtracking_search(self):
        """This functions starts the CSP solver and returns the found
        solution.
        """
        # Make a so-called "deep copy" of the dictionary containing the
        # domains of the CSP variables. The deep copy is required to
        # ensure that any changes made to 'assignment' does not have any
        # side effects elsewhere.
        assignment = copy.deepcopy(self.domains)

        # Run AC-3 on all constraints in the CSP, to weed out all of the
        # values that are not arc-consistent to begin with
        self.inference(assignment, self.get_all_arcs())

        # Call backtrack with the partial assignment 'assignment'
        return self.backtrack(assignment)

    def backtrack(self, assignment):
        """The function 'Backtrack' from the pseudocode in the
        textbook.

        The function is called recursively, with a partial assignment of
        values 'assignment'. 'assignment' is a dictionary that contains
        a list of all legal values for the variables that have *not* yet
        been decided, and a list of only a single value for the
        variables that *have* been decided.

        When all of the variables in 'assignment' have lists of length
        one, i.e. when all variables have been assigned a value, the
        function should return 'assignment'. Otherwise, the search
        should continue. When the function 'inference' is called to run
        the AC-3 algorithm, the lists of legal values in 'assignment'
        should get reduced as AC-3 discovers illegal values.

        IMPORTANT: For every iteration of the for-loop in the
        pseudocode, you need to make a deep copy of 'assignment' into a
        new variable before changing it. Every iteration of the for-loop
        should have a clean slate and not see any traces of the old
        assignments and inferences that took place in previous
        iterations of the loop.
        """
        #Check if we are finished, every variable assigned one value.
        if self.finished(assignment):
            return assignment
        
        #Select next unassigned variable.
        variable = self.select_unassigned_variable(assignment)
        #Itterate thru every value we can chose for an variable.
        for value in self.order_domain_variable(assignment,variable):
            #Make a copy to prevent messing with old instanses of assignment for other itterations.
            assignment_copy = copy.deepcopy(assignment)
            #assign our current variable to our current value.
            assignment_copy[variable] = [value]
            #if value is incostistent with assignment.
            #iff choise of value consistent with every constraint
            #We need to check if we chose this value, that it is arc consistent
            if self.inference(assignment_copy, self.get_all_arcs()):
                # we nedd to call backtrack recursivly, to check next layer in the "tree" on the copy.
                result = self.backtrack(assignment_copy)
                if result: #result should be false if it doesn't work, or finished assignment list
                    return result
            #assignment_copy.remove(value)
        return False

    def select_unassigned_variable(self, assignment):
        """The function 'Select-Unassigned-Variable' from the pseudocode
        in the textbook. Should return the name of one of the variables
        in 'assignment' that have not yet been decided, i.e. whose list
        of legal values has a length greater than one.
        """

        #Itterate every item in the domain
        for variable, values in assignment.iteritems():
            #if there are more than one value to chose from in tis variables legal values
            if len(values) > 1: #We know there should exist atleast one, because the assignment is not finished at this stage.
                #return name corresponding to these values.
                return variable

    def inference(self, assignment, queue):
        """The function 'AC-3' from the pseudocode in the textbook.
        'assignment' is the current partial assignment, that contains
        the lists of legal values for each undecided variable. 'queue'
        is the initial queue of arcs that should be visited.
        """
        #itterate tru the que and check for consistency
        while queue:
            #que consists of all arcs that should be visited, an arc is a connection of every neighbour (x,y)
            #Get first element in queue
            (X_i,X_j) = queue.pop(0)
            if self.revise(assignment, X_i, X_j):
                #Check if x has any legal steps left.
                if not assignment[X_i]:
                    return False
                
                #Need to itterate every neighbour from this variable,
                #And add everyone to the list who is not the variables X_j (current arc)
                all_neighbors = self.get_all_neighboring_arcs(X_i)
                for X_k, X_i in all_neighbors:
                    #We need to check if X_k is the same neighbour as X_j
                    if X_k != X_j:
                        queue.append((X_k,X_i))#Need to add this new arc to neighbour.
        return True

    def revise(self, assignment, i, j):
        """The function 'Revise' from the pseudocode in the textbook.
        'assignment' is the current partial assignment, that contains
        the lists of legal values for each undecided variable. 'i' and
        'j' specifies the arc that should be visited. If a value is
        found in variable i's domain that doesn't satisfy the constraint
        between i and j, the value should be deleted from i's list of
        legal values in 'assignment'.
        """
        revised = False
        #List of every legal pair in the form {(C1,C2),...}
        legal_values = self.constraints[i][j] #All legal values between two variables. 
   
        #itterate tru every legal value in i's domain.
        for value in assignment[i]:
            #we create ever possible value from this one.
            all_value_pairs = self.get_all_possible_pairs_as_list(value, assignment[j])
            #We remove this value if we find no legal value that statisfy the constraint.
            remove_value = True
            for pair in all_value_pairs:
                #If there is atleast one value that is in the constraints, we can move on, otherwise we remove this value.
                if pair in legal_values:
                    remove_value = False
                    #we dont need to check the remaining pairs, since there exist atleast one valid pair to choose from.
                    break

            #Check if we need to remove this value as a option for i (X_i)
            if remove_value:
                #we know the pair is not a legal value, we need to prune/remove this value from i's domain
                assignment[i].remove(value)
                revised = True
        #Return whether or not we had to remove any values from i's domain.
        return revised

    
    def order_domain_variable(self, assignment, variable):
        """ return the list of legal values corresponding to this variable, in whatever oder we specify """
        #in our case we shouldnt do anything, but return the values for an variable in the default order.
        return assignment[variable]

    def finished(self,assingment):
        """ return true if all variables has been assigned/decided. 
            i.e every variable contain only a list of possible values of length 1"""
        for variable, values in assingment.iteritems():
            if len(values) != 1:
                return False
        return True

def create_map_coloring_csp():
    """Instantiate a CSP representing the map coloring problem from the
    textbook. This can be useful for testing your CSP solver as you
    develop your code.
    """
    csp = CSP()
    states = [ 'WA', 'NT', 'Q', 'NSW', 'V', 'SA', 'T' ]
    edges = { 'SA': [ 'WA', 'NT', 'Q', 'NSW', 'V' ], 'NT': [ 'WA', 'Q' ], 'NSW': [ 'Q', 'V' ] }
    colors = [ 'red', 'green', 'blue' ]
    for state in states:
        csp.add_variable(state, colors)
    for state, other_states in edges.items():
        for other_state in other_states:
            csp.add_constraint_one_way(state, other_state, lambda i, j: i != j)
            csp.add_constraint_one_way(other_state, state, lambda i, j: i != j)
    return csp

def create_sudoku_csp(filename):
    """Instantiate a CSP representing the Sudoku board found in the text
    file named 'filename' in the current directory.
    """
    csp = CSP()
    board = map(lambda x: x.strip(), open(filename, 'r'))

    for row in range(9):
        for col in range(9):
            if board[row][col] == '0':
                csp.add_variable('%d-%d' % (row, col), map(str, range(1, 10)))
            else:
                csp.add_variable('%d-%d' % (row, col), [ board[row][col] ])

    for row in range(9):
        csp.add_all_different_constraint([ '%d-%d' % (row, col) for col in range(9) ])
    for col in range(9):
        csp.add_all_different_constraint([ '%d-%d' % (row, col) for row in range(9) ])
    for box_row in range(3):
        for box_col in range(3):
            cells = []
            for row in range(box_row * 3, (box_row + 1) * 3):
                for col in range(box_col * 3, (box_col + 1) * 3):
                    cells.append('%d-%d' % (row, col))
            csp.add_all_different_constraint(cells)

    return csp

def print_sudoku_solution(solution):
    """Convert the representation of a Sudoku solution as returned from
    the method CSP.backtracking_search(), into a human readable
    representation.
    """
    for row in range(9):
        for col in range(9):
            print solution['%d-%d' % (row, col)][0],
            if col == 2 or col == 5:
                print '|',
        print ""
        if row == 2 or row == 5:
            print '------+-------+------'


csp = create_map_coloring_csp()
asigment = copy.deepcopy(csp.domains)

#print csp.backtracking_search()


csp_easy = create_sudoku_csp("sudokus/veryhard.txt")
solution = csp_easy.backtracking_search()
print_sudoku_solution(solution)