from operator import add, mul, and_, or_

######################################################################
## Here is some tediously repetitive code which we will take as our ##
## starting point                                                   ##
######################################################################

# A simple class which performs some task.
class Crusher:

    def help(self):
        return "Gimme some numbers."

    def crush(self, *args):
        return reduce(add, args, 0)

# A variation on the above theme
class VerboseCrusher(Crusher):

    def help(self):
        return "So, what you have to do, like, is give me some numbers, right?"

# A second variation on the theme
class LaconicCrusher(Crusher):

    def help(self):
        return "numbers"

# A different variation (in an orthogonal direction) on the first
# theme: it changes a different aspect of the original idea.
class MultiplyingCrusher(Crusher):

    def crush(self, *args):
        return reduce(mul, args, 1)

# A second variation in the new direction
class AndCrusher(Crusher):

    def help(self):
        return "Gimme some booleans."

    def crush(self, *args):
        return reduce(and_, args, True)

# A third variation in the new direction
class OrCrusher(Crusher):

    def help(self):
        return "Gimme some booleans."

    def crush(self, *args):
        return reduce(or_, args, False)

# A variation which combines changes BOTH of the above directions.
class VerboseMultiplyingCrusher(Crusher):
    
    def help(self):
        return "So, what you have to do, like, is give me some numbers, right?"

    def crush(self, *args):
        return reduce(mul, args, 1)

# Notice that with the variations we have introduced so far, if we
# wanted to make all possible combinations, we would have to implement
# the following 5 variations too (making a total of 12 classes; 3 ways
# of giving instructions x 4 ways of crushing the data gives 12
# possible combinations):

class LaconicMultiplyingCrusher(Crusher):

    def help(self):
        return "numbers"

    def crush(self, *args):
        return reduce(mul, args, 1)

class LaconicAndCrusher(Crusher):

    def help(self):
        return "booleans"

    def crush(self, *args):
        return reduce(and_, args, True)
    
class LaconicOrCrusher(Crusher):

    def help(self):
        return "booleans"

    def crush(self, *args):
        return reduce(or_, args, False)
    
class VerboseAndCrusher(Crusher):

    def help(self):
        return "So, what you have to do, like, is give me some booleans, right?"

    def crush(self, *args):
        return reduce(and_, args, True)
    
class VerboseOrCrusher(Crusher):

    def help(self):
        return "So, what you have to do, like, is give me some booleans, right?"

    def crush(self, *args):
        return reduce(or_, args, False)

#################################################################
##                                                             ##
## A test that checks that all the above behave as they should ##
##                                                             ##
#################################################################

# The keys in the dictionary reflect the expected behaviour. The first
# letter specifies whether the help method behaviour is Normal,
# Verbose or Laconic; the second letter specifies whether the crushing
# operation is Normal, Multiply, And or Or.

def test(**crusher):
    assert crusher['nn'].help() == "Gimme some numbers."
    assert crusher['nn'].crush(1,2) == 3
    assert crusher['nn'].crush() == 0

    assert crusher['ln'].help() == "numbers"
    assert crusher['ln'].crush(1,2) == 3
    assert crusher['ln'].crush() == 0

    assert crusher['vn'].help() == "So, what you have to do, like, is give me some numbers, right?"
    assert crusher['vn'].crush(1,2) == 3
    assert crusher['vn'].crush() == 0

    assert crusher['nm'].help() == "Gimme some numbers."
    assert crusher['nm'].crush(1,2) == 2
    assert crusher['nm'].crush() == 1

    assert crusher['lm'].help() == "numbers"
    assert crusher['lm'].crush(1,2) == 2
    assert crusher['lm'].crush() == 1

    assert crusher['vm'].help() == "So, what you have to do, like, is give me some numbers, right?"
    assert crusher['vm'].crush(1,2) == 2
    assert crusher['vm'].crush() == 1

    assert crusher['na'].help() == "Gimme some booleans."
    assert crusher['na'].crush(True, False) == False
    assert crusher['na'].crush() == True

    assert crusher['la'].help() == "booleans"
    assert crusher['la'].crush(True, False) == False
    assert crusher['la'].crush() == True

    assert crusher['va'].help() == "So, what you have to do, like, is give me some booleans, right?"
    assert crusher['va'].crush(True, False) == False
    assert crusher['va'].crush() == True

    assert crusher['no'].help() == "Gimme some booleans."
    assert crusher['no'].crush(True, False) == True
    assert crusher['no'].crush() == False

    assert crusher['lo'].help() == "booleans"
    assert crusher['lo'].crush(True, False) == True
    assert crusher['lo'].crush() == False

    assert crusher['vo'].help() == "So, what you have to do, like, is give me some booleans, right?"
    assert crusher['vo'].crush(True, False) == True
    assert crusher['vo'].crush() == False

    print "OK"


test(nn=Crusher(),
     ln=LaconicCrusher(),
     vn=VerboseCrusher(),
     nm=MultiplyingCrusher(),
     lm=LaconicMultiplyingCrusher(),
     vm=VerboseMultiplyingCrusher(),
     na=AndCrusher(),
     la=LaconicAndCrusher(),
     va=VerboseAndCrusher(),
     no=OrCrusher(),
     lo=LaconicOrCrusher(),
     vo=VerboseOrCrusher())
######################################################################
##                                                                  ##
## In short, we have N=3 variations in one direction, and M=4       ##
## variations in the second direction. This makes a total of NxM =  ##
## 4x3 = 12 different classes that we would have to write, to cover ##
## all possibilities. These classes mostly use copy-paste           ##
## (i.e. evil) code reuse. Extremely tedious, and very              ##
## error-prone. Can we do better?                                   ##
##                                                                  ##
## Yes, we parametrize the variations.                              ##
##                                                                  ##
######################################################################

class Crusher:

    def __init__(self, help_template, combination_spec):
        self._help = help_template
        self._op, self._default, self._kind = combination_spec

    def help(self):
        return self._help % (self._kind,)

    def crush(self, *args):
        return reduce(self._op, args, self._default)

# With this parametrized version, we can create any combination we
# like at run-time, without having to create any more
# classes. Effectively, we get all the classes for free.

# Here they are passing the same tests.

test(nn=Crusher("Gimme some %s.", (add, 0, 'numbers')),
     ln=Crusher(           "%s" , (add, 0, 'numbers')),
     vn=Crusher("So, what you have to do, like, is give me some %s, right?" , (add,  0, 'numbers')),
     nm=Crusher("Gimme some %s.", (mul, 1, 'numbers')),
     lm=Crusher(           "%s" , (mul, 1, 'numbers')),
     vm=Crusher("So, what you have to do, like, is give me some %s, right?" , (mul,  1, 'numbers')),
     na=Crusher("Gimme some %s.", (and_, True, 'booleans')),
     la=Crusher(           "%s" , (and_, True, 'booleans')),
     va=Crusher("So, what you have to do, like, is give me some %s, right?" , (and_, True, 'booleans')),
     no=Crusher("Gimme some %s.", (or_, False, 'booleans')),
     lo=Crusher(           "%s" , (or_, False, 'booleans')),
     vo=Crusher("So, what you have to do, like, is give me some %s, right?" , (or_, False, 'booleans')),)

#####################################################################
##                                                                 ##
##  Exercise:                                                      ##
##                                                                 ##
##  Of course, the implementation shown above relies on            ##
##  conveniences like Python's first-class functions and duck      ##
##  typing. In Java and C++ we would have some extra work to       ##
##  do. This also gives us the opportunity to package the related  ##
##  information (operation, defualt, kind) into some container     ##
##  object.                                                        ##
##                                                                 ##
##  Rewrite the Crusher class, to use Strategy classes rather than ##
##  relying on Python's first-class functions.                     ##
##                                                                 ##
#####################################################################

class Crusher:

    def __init__(self, help_strategy, combination_strategy):
        self._help_strategy = help_strategy
        self._combination_strategy = combination_strategy

    def help(self):
        return self._help_strategy % (self._combination_strategy.kind,)

    def crush(self, *args):
        # result = self._combination_strategy.default
        # for element in args:
        #    result = self._combination_strategy.op(result, element)
        #
        # return result

        return reduce(self._combination_strategy.op, args,
                      self._combination_strategy.default)
    


# In Java and C++ we'll need a base class or interface for the
# strategies. Let's try to make that explicit in Python
from abc import abstractmethod, ABCMeta

class CombinationStrategy:
    # Python magic which allows us to create abstract methods
    __metaclass__ = ABCMeta

    @abstractmethod
    def op(self, lhs, rhs):
        pass

# And each different strategy is likely to be a new class.
class AdditionStrategy(CombinationStrategy):

    kind = 'numbers'
    default = 0

    def op(self, lhs, rhs):
        return lhs + rhs

class MultiplicationStrategy(CombinationStrategy):

    kind = 'numbers'
    default = 1

    def op(self, lhs, rhs):
        return lhs * rhs


class AndStrategy(CombinationStrategy):

    kind = 'booleans'
    default = True

    def op(self, lhs, rhs):
        return lhs and rhs


class OrStrategy(CombinationStrategy):

    kind = 'booleans'
    default = False

    def op(self, lhs, rhs):
        return lhs or rhs


####################################################
##                                                ##
## Make sure your implementation passes the tests ##
##                                                ##
####################################################

test(nn=Crusher("Gimme some %s.", AdditionStrategy()),
     ln=Crusher(           "%s" , AdditionStrategy()),
     vn=Crusher("So, what you have to do, like, is give me some %s, right?" , AdditionStrategy()),
     nm=Crusher("Gimme some %s.", MultiplicationStrategy()),
     lm=Crusher(           "%s" , MultiplicationStrategy()),
     vm=Crusher("So, what you have to do, like, is give me some %s, right?" , MultiplicationStrategy()),
     na=Crusher("Gimme some %s.", AndStrategy()),
     la=Crusher(           "%s" , AndStrategy()),
     va=Crusher("So, what you have to do, like, is give me some %s, right?" , AndStrategy()),
     no=Crusher("Gimme some %s.", OrStrategy()),
     lo=Crusher(           "%s" , OrStrategy()),
     vo=Crusher("So, what you have to do, like, is give me some %s, right?" , OrStrategy()))

# Not as trivial and clean as the fully Pythonic version, but still
# much better than the original. 

# Note that the more varieties and directions of varieties there are,
# the larger the gains.

# Also note that this gives the potential of changing the strategy at
# runtime. In the original version, the behaviour of the object was
# fixed for its lifetime.
