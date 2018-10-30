from collections import namedtuple

Isotope = namedtuple('isotope', ['A', 'mass'])

class Element():
    """
    Contains information about an element:
    atomic number (str),
    symbol (str),
    stable isotopes (tuple)
    """
    def __init__(self, index, name, isotopes):
        self.index = index
        self.name = name
        self.isotopes = isotopes

def constructElementTable():
    """"
    Parse isotope data
    return: list of elements
    """
    element_table = list()
    with open('isotope.txt', 'r') as f:
        for line in f:
            s = line.split('\t')
            if len(s) > 2: #new element entry has more than 2 column
                try: # check if a previous element has been found
                    element_table.append(Element(index, name, tuple(isotopes)))
                except:
                    pass
                index = s[0]
                name = s[0] + s[1]
                isotopes = list()
                isotopes.append(Isotope(A=s[2], mass=s[3]))
            else:
                isotopes.append(Isotope(A=s[0].strip(), mass=s[1]))
                #strip the white space in front the line
        else:
            element_table.append(Element(index, name, tuple(isotopes)))
    return element_table

table = constructElementTable()
