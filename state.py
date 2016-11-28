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

class Box:

    def __init__(self, thing = None):
        self.thing = thing

    def is_empty(self):
        return True if self.thing is None else False

    def insert(self, thing):
        if self.thing is None:
            self.thing = thing
        else:
            raise Exception('Box full')

    def remove(self):
        if self.thing is None:
            raise Exception('There is nothing in the box')
        else:
            thing = self.thing
            self.thing = None
            return thing



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

class Empty:

    def insert(self, thing):
        self.thing = thing
        self.__class__ = Full

    def remove(self):
        raise Exception('There is nothing in the box')

    def is_empty(self):
        return True


class Full:

    def insert(self, thing):
        raise Exception('Box full')

    def remove(self):
        thing = self.thing
        self.thing = None
        self.__class__ = Empty
        return thing

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

# Hint: Rather than switching the object's class, you will need to
# store an internal object which forwards requests to the current
# state's methods, and it is these internal objects that you will have
# to switch when the state changes.

class State:
    
    def __init__(self, thing = None):
        self.thing = thing

class EmptyState(State):

    def __init__(self, state):
        self.state = state
    
    def insert(self, thing):
        self.state.thing = thing

    def remove(self):
        raise Exception('There is nothing in the box')

    def is_empty(self):
        return True
    
class FullState(State):

    def __init__(self, state):
        self.state = state

    def insert(self, thing):
        raise Exception('Box full')

    def remove(self):
        value = self.state.thing
        self.state.thing = None
        return value

    def is_empty(self):
        return False

class SBox:

    def __init__(self):
        state = State()
        self.empty_state = EmptyState(state)
        self.full_state = FullState(state)
        self.actual_state = self.empty_state

    def insert(self, thing):
        self.actual_state.insert(thing)
        self.actual_state = self.full_state

    def remove(self):
        value = self.actual_state.remove()
        self.actual_state = self.empty_state
        return value

    def is_empty(self):
        return self.actual_state.is_empty()
    

test(SBox)

# You must appreciate that Python lets you get away without devoting
# any thought to the class hierarchy. In Java and C++ you will have to
# think carefully about how these objects are related by inheritance.
