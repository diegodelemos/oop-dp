# Exercise 1

# Expand the following classes to make them work together as requested
# below

# A simple stateful class. The state can be modified.
class Temperature:

    def __init__(self, init):
        self.observers = []
        self.state = init

    def get_state(self):
        return self.state

    def set_state(self, state):
        if self.state != state:
            self.state = state
            # The call to the `notify` method should
            # be meditated. i.e. if the operation
            # inside set_state has 40 steps, maybe
            # it is not feasible to notify observers
            # after each step, maybe it is better
            # to notify them at the end.
            self._notify()

    def _notify(self):
        # this is not cool if you have a billion
        # of records but it is ok now.
        for observer in self.observers[:]:
            observer.update(self)

    # GoF name `attach`
    def subscribe(self, obj):
        self.observers.append(obj)

    # GoF name `dettach``
    def unsubscribe(self, obj):
        self.observers.remove(obj)

# A class which can be connected to the previous one. Make it notice
# when the state of its subject changes, and display the new value of
# the subject's state.
class Observer:
    def update(self, obj):
        pass


class Numeric_display(Observer):
    # def __init__(self, subject, strategy=UnsubscribeNever()):
    def __init__(self, subject, strategy = lambda _: False):
        self.subject = subject
        self.subject.subscribe(self)
        self.unsubscribe_strategy = strategy

    def display(self, n):
        print "%4d" % n

    def update(self, subject):
        # Numeric_display's code affected by the change
        # if self.unsubscribe_strategy.do_unsubscribe(t.get_state()):
        if self.unsubscribe_strategy(subject.get_state()):
            self.subject.unsubscribe(self)
        else:
            self.display(subject.get_state())


# A variation on the theme. Make it work like the above, too.
class Bar_display(Numeric_display):

    def display(self, n):
        print "*" * int(n)
            
# TODO: this needs finihish. See the solution file.
# A class with an unrelated interface which is interested in temperature changes
class Change_detector(Observer):

    def __init__(self):
        self._previous_value = None

    def report_change(self, t):
        if self._previous_value is not None:
            delta = t.get_state() - self._previous_value
            print "Temperature changed by", delta
        self._previous_value = t.get_state()

    def update(self, subject):        
        self.report_change(subject)

"""
# Java and C++ world
class UnsubscribeStrategy: pass

class UnsubscribeNever(UnsubscribeStrategy):

    def do_unsubscribe(self, t):
        return False
    
class UnsubscribeOver70(UnsubscribeStrategy):

    def do_unsubscribe(self, t):
        return t > 70

t = Temperature(0)
n = Numeric_display(t, UnsubscribeNever())
b = Bar_display(t, UnsubscribeOver70())
c = Change_detector(t, UnsubscribeNever())
"""

# solved using default parameter
# never_unsubscribe = lambda t: False
over70_unsubscribe = lambda t: t > 70

t = Temperature(0)
# n = Numeric_display(t, never_unsubscribe)
n = Numeric_display(t)
b = Bar_display(t, over70_unsubscribe)
c = Change_detector()
t.subscribe(c)

# Every time the state is changed, the displays should show the new
# value.
for n in range(0, 100,5):
    t.set_state(n)

# Exercise 2

# Make Bar_display detach itself from its subject when the temperature
# exceeds 70 degrees.


# Exercise 3

# Use a strategy for deciding when any observer should detach
# itself. (Hint: make it easier, at first, by using a first-class
# function, before progressing to a fully-blown Strategy pattern.)
