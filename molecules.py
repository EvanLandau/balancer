#Class for molecules
import elements

class molecule:
    """Class for a molecule"""
    def __init__ (self, formula):
        self.atoms = [] #Left is the atom, right is the number
        end = 1
        start = 0
        groups = []
        while end < len(formula):
            while end < len(formula):
                if formula[end].isupper():
                    groups.append(formula[start:end])
                    start = end
                    end += 1
                    break
                end += 1
        else:
            groups.append(formula[start:end])
        for group in groups:
            if group.isalpha():
                self.atoms.append((elements.periodic_dictionary[group], 1))
            else:
                for i in range(1, len(group)):
                    if group[i:len(group)].isnumeric():
                        self.atoms.append((elements.periodic_dictionary[group[0:i]], int(group[i:len(group)])))
                        break
        self.total_weight = 0
        for atom in self.atoms:
            self.total_weight += atom[0].weight * atom[1]
    
        