# Tests defining the required behaviour.

def test(Box):
    box = Box()
    # Box should start off empty
    assert box.is_empty()
    # Removing from an empty box should raise some exception
    try:
        box.remove()
    except: pass
    else: raise Exception("Should have complained at removing from empty box.")
    # Inserting into empty box should work
    box.insert('banana')  # OK
    # is_empty on full box should work
    assert not box.is_empty()
    # Inserting to full box shouldn't work
    try:
        box.insert('orange')  # Can't do that
    except: pass
    else: raise Exception("Adding to full box should have complained.")
    # Removing from full box should work
    assert  box.remove() == 'banana'
    # Box should now be empty again
    assert box.is_empty()
    # Make sure the contents aren't hard-wired
    box.insert(12)
    assert box.remove() == 12
    print box.__class__.__name__, "passed the tests."



#####################################################
##                                                 ##
## Exercise 1                                      ##
##                                                 ##
## Implement a class which passes the above tests. ##
##                                                 ##
#####################################################

# Implementation without the State pattern. Each method has branches
# for all possible states.

class Box:

    def __init__(self, thing = None):
        self.thing = thing

    def is_empty(self):
        if self.thing is None:
            return True
        else:
            return False

    def insert(self, thing):
        if self.thing is None:
            self.thing = thing
        else:
            raise Exception("The box is already full")

    def remove(self):
        if self.thing is None:
            raise Exception("There is nothing in the box")
        else:
            o = self.thing
            self.thing = None
            return o

test(Box)


##################################################################
##                                                              ##
## Exercise 2                                                   ##
##                                                              ##
## Now do it again, writing *two* classes, one for each of the  ##
## states. Use Python's ability to change the type of an object ##
## dynamically, to change the state:                            ##
##                                                              ##
##     some_instance.__class__ = SomeClass                      ##
##                                                              ##
##################################################################

# First State pattern implementation. There is a separate class for
# each state, and state changes require class changes.

class Empty:

    def insert(self, thing):
        self.thing = thing
        self.__class__ = Full

    def remove(self):
        raise Exception("There is nothing in the box")

    def is_empty(self):
        return True


class Full:

    def insert(self, thing):
        raise Exception("The box is already full")

    def remove(self):
        self.__class__ = Empty
        return self.thing

    def is_empty(self):
        return False


test(Empty)



#####################################################################
##                                                                 ##
## Exercise 3:                                                     ##
##                                                                 ##
## In Java and C++ changing an object's class at runtime is        ##
## impossible. Write a set of classes which will pass the test but ##
## do *not* rely on the ability to change the object's class at    ##
## runtime.                                                        ##
##                                                                 ##
#####################################################################

class EmptyState:

    def insert(self, box, thing):
        box._thing = thing
        box._state = box.fullState

    def remove(self, box):
        raise Exception("There is nothing in the box")

    def is_empty(self, box):
        return True


class FullState:

    def insert(self, box, thing):
        raise Exception ("The box is already full")

    def remove(self, box):
        box._state = box.emptyState
        return box._thing

    def is_empty(self, box):
        return False


class SBox:

    fullState = FullState()
    emptyState = EmptyState()

    def __init__(self):
        self._state = self.emptyState

    def insert(self, thing):
        self._state.insert(self, thing)
    
    def remove(self):
        return self._state.remove(self)

    def is_empty(self):
        return self._state.is_empty(self)

test(SBox)

# You must appreciate that Python lets you get away without devoting
# any thought to the class hierarchy. In Java and C++ you will have to
# think carefully about how these objects are related by
# inheritance. Specifically, EmptyState and FullState will have to
# share a common formal interface.

