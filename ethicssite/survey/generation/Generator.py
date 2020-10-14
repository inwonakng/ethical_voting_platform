from .Category import Category
from .Rule import Rule
from .Combo import Combo
from itertools import combinations as comb

class Generator():
    def __init__(self, adaptive=False, rule={}):
        if len(rule) == 0:
            raise "Rule is empty"
        elif len(rule['categories']) == 0:
            raise "Categories is empty"
        # assign attributes
        self.adaptive = adaptive
        self.categories = []
        self.bad_combos = []

        for key, value in rule['categories'].items():
            self.categories.append(Category(name=key, options=value))
        for attr, vals in rule['bad combo'].items():
            self.bad_combos.append(Rule(category=attr, value=vals))

        # Cache result
        self.combinations = []
        
    def get_scenario(self,numcombos = 3):
        self.permutate_options(numcombos)
        return [c.getCombo() for c in self.combinations]

    def permutate_options(self,numcombos):
        self.combinations = []
        for _ in range(numcombos): self.__recursive_permutation()
        # check for duplicates. let's allow 2 values to be repeated up to numcombos -1 times
        if not self.check_duplicates(): self.permutate_options(numcombos)
        return True

    def check_duplicates(self):
        # get all possible pairs to compare duplicates
        tocheck = list(comb(self.combinations,2))
        found = {}
        for c1,c2 in tocheck:
            dups = c1.compare(c2)
            for d in dups:
                if not d in found: found[d] = 0
                else: found[d] += 1
        numfound = list(found.values())
        return max(numfound) < 3 and numfound.count(2) < len(self.combinations)-1

    # modified to compute just one combination.
    def __recursive_permutation(self, stack = [], categoryIndex = 0):
        if categoryIndex >= len(self.categories):
            # The end of recursion
            self.combinations.append(Combo.fromList(stack))
            return

        categ = self.categories[categoryIndex]
        name = categ.name

        # grab a value that follows the rules generated by the category objects
        nxt = categ.getnext(self.bad_combos,stack)
        stack.append((name,nxt))
        self.__recursive_permutation(stack, categoryIndex + 1)