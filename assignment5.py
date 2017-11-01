#!/usr/bin/python

import copy
import itertools

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
        # TODO: IMPLEMENT THIS
        """ 
        if assignment is complete 
            return assignment
        var = SELECT_UNASSIGNED_VARIABLES(csp)
        for each value in order-domain-value(var, assignment, cps)
            if value is consistent with assignment
                add var to assignment
                inferences = inference(assignment, queu)
                if inference not failour
                    add inference to assignment
                    result = backtrack(assignment)
                    if result not failure
                        return result
            remove var and inference from assignment
        return failure
        """
        if finished(assignment):
            return assignment
        
        variable = self.select_unassigned_variable(assignment)

        #Itterate thru every value we can chose for an variable.
        for value in order_domain_variable(assignment,variable):
            #Make a copy
            assignment_copy = copy.deepcopy(assignment)
            assignment_copy[variable] = value
            #if value is incostistent with assignment.
            #iff choise of value consistent with every constraint
            #We need to check if we chose this value, that it is arc consistent
            if self.inference(assignment_copy, value):
                result = self.backtrack(assignment_copy)
                if result: #result should be false if it doesn't work.
                    return result
            
        return assignment

    def select_unassigned_variable(self, assignment):
        """The function 'Select-Unassigned-Variable' from the pseudocode
        in the textbook. Should return the name of one of the variables
        in 'assignment' that have not yet been decided, i.e. whose list
        of legal values has a length greater than one.
        """
        # TODO: IMPLEMENT THIS

        #Itterate every item in the domain
        for variable, values in assingment.iteritems():
            #if there are more than one value to chose from
            if len(values) > 1: #We know there should exist atleast one, because the assignment is not finished at this stage.
                #return name corresponding to these values.
                return variable

    def inference(self, assignment, queue):
        """The function 'AC-3' from the pseudocode in the textbook.
        'assignment' is the current partial assignment, that contains
        the lists of legal values for each undecided variable. 'queue'
        is the initial queue of arcs that should be visited.
        """
        # TODO: IMPLEMENT THIS

        #itterate tru the que and check for consistency
        for arcs in queue:
            pass
        while queue:
            #que consists of all arcs that should be visited, an arc is a connection of every neighbour (x,y)
            (X_i,X_j) = queue.pop()
            if self.revise(assignment, X_i, X_j):
                #Check if x has any legal steps left.
                if not assignment[X_i]:
                    return False
                
                #Need to itterate every 
                
        pass

    def revise(self, assignment, i, j):
        """The function 'Revise' from the pseudocode in the textbook.
        'assignment' is the current partial assignment, that contains
        the lists of legal values for each undecided variable. 'i' and
        'j' specifies the arc that should be visited. If a value is
        found in variable i's domain that doesn't satisfy the constraint
        between i and j, the value should be deleted from i's list of
        legal values in 'assignment'.
        """
  
        """ Returns true iff we revise the domain of X_i
            revised = False
            for each x in D_i
                if no value y in D_j allows (x,y) to statify the constraint between X_i and X_j 
                    then delete x from D_i
                    revised = True
            return revised
        """
        #Go thru 
        reviced = False

        #itterate every legal value for variable i's domain.
        #for x_i in assignment[i]:
        """
            possible_arcs = []
            #All values that should be visited next
            for x_j in assignment[j]:
                possible_arcs.append((x_i,x_j))
            print "arcs: ", possible_arcs

            #List of every legal pair in the form {(C1,C2),...}
            legal_values = self.constraints[i][j] #All legal values between two variables. 
            print "leg_val", legal_values
            #Generate a list of every possible arc with the value x_i and all of one of the neighbours.
            pairs = self.get_all_possible_pairs(assignment[i],assignment[j])
            
            for pai in pairs:
                print pai

            #We need to check if 

            for pair in legal_values:
                if pair in possible_arcs:
                    #print "pair is in possible pair", pair
                    pass
            #We need to check if our pair of x_i and every pair of x_j is not in this list.

            #print "constraints:", self.constraints[i][j]
            #Check if x_i is an invallid assignment in domain[j]
            if not self.constraints[x_i][j]:
                #if there are no valie x_j in domain[j] that satisfy the constraint between i and j.
                #then delete x_i from D_i.
                #And set reviced = True
                assignment[i].remove(x_i)
                reviced = True
        return reviced
        """
        #List of every legal pair in the form {(C1,C2),...}
        legal_values = self.constraints[i][j] #All legal values between two variables. 
        #every possible pair we can make from these values. 
        all_value_pairs = self.get_all_possible_pairs(assignment[i],assignment[j])
        for pair in all_value_pairs:
            if pair in legal_values:
                continue
            reviced = True
            assignment[i].remove(pair[0])
        #Return with having remove 
        return reviced

    def order_domain_variable(self, assignment, variable):
        """ return the list of legal values corresponding to this variable, in whatever oder we specify """
        #in our case we shouldnt do anything, but return the values for an variable in the default order.
        return assignment[variable]

    def finished(self,assingment):
        """ return true if all variables has been assigned/decided. 
            i.e every variable contain only a list of lengt 1"""
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
            print solution['%d-%d' % (row, col)][0]
            if col == 2 or col == 5:
                print '|',
        print
        if row == 2 or row == 5:
            print '------+-------+------'


csp = create_map_coloring_csp()
asigment = copy.deepcopy(csp.domains)
"""print "get_all_arcs= ", csp.get_all_arcs()
print "variables= ",csp.variables
print ""
print "domains= ",csp.domains 
print "domains['WA]'= ",csp.domains['WA'] 
print "asigmen['WA']=", asigment['WA']
print ""
print "csp.constraints['WA']['SA']=",csp.constraints['WA']['SA']
"""
print "finished:", csp.finished(csp.domains)

csp.backtracking_search()