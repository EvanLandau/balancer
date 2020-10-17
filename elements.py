#Element class and list thereof

class element:
    """Class representing a chemical element."""
    def __init__ (self, symbol, atomic_number, atomic_weight, electronegativity, oxidation_states, group, period):
        self.symbol = symbol
        self.n = atomic_number
        self.weight = atomic_weight
        self.oxidation_states = oxidation_states
        self.group = group
        self.period = period
        
    def __str__(self):
        return self.symbol
    def __repr__(self):
        return self.symbol
    def __gt__(self, other):
        if self.n > other.n:
            return True
        else:
            return False
    def __lt__(self, other):
        if self.n < other.n:
            return True
        else:
            return False
    def __eq__(self, other):
        if self.n == other.n:
            return True
        else:
            return False

periodic_table = [] #Stores all elements, from 1-118, elements can be looked up with periodic_table[n], where n is the atomic number
periodic_table.append(element('X', 0, 0, 0, [0], 0, 0)) #Fake element (element 0) to make things line up
periodic_table.append(element('H', 1, 1.008, 2.20, [-1, 1], 1, 1))
periodic_table.append(element('He', 2, 4.0026, 0, [0], 1, 18))
periodic_table.append(element('Li', 3, 6.94, 0.98, [1], 2, 1))
periodic_table.append(element('Be', 4, 9.01218, 1.57, [+2], 2, 2))
periodic_table.append(element('B', 5, 10.81, 2.04, [+3], 13, 2))
periodic_table.append(element('C', 6, 12.011, 2.55, [-4, +4], 14, 2))
periodic_table.append(element('N', 7, 14.006, 3.04, [-3, +3], 15, 2))
periodic_table.append(element('O', 8, 15.999, 3.44, [-2], 16, 2))
periodic_table.append(element('F', 9, 18.998, 3.98, [-1], 17, 2))
periodic_table.append(element('Ne', 10, 20.180, 0, [0], 18, 2))
#TODO: Rest of elements

periodic_dictionary = {} #Dictionary to allow easy lookup of elements from symbols
for el in periodic_table:
    periodic_dictionary.update( {el.symbol : el} )