# The purpose of this class is to be a very easy subject of
# iteration. The class always contains two data, so the iterators will
# have to yield the first, then the second, then stop.
class AlwaysContainsTwoThings:

    def __init__(self, first, second):
        self._first  = first
        self._second = second

    # If an external iterator exists, there must be some means of
    # acquiring that iterator.
    def give_me_an_external_iterator(self):
        return IteratorForAlwaysContainsTwoThings(self)

    def internal_iterator(self, operation):
        operation(self._first)
        operation(self._second)

    # This is the hook into Python's iterator protocol. It is
    # essentially the same as give_me_an_external_iterator, but
    # Python's iterator protocol looks for the exact name __iter__,
    # whenever the global function iter is called. Python for loops do
    # this implicitly.
    def __iter__(self):
        return PyIterACTT(self)


# The external iterator class for the above class.
class IteratorForAlwaysContainsTwoThings:

    def __init__(self, the_thing_to_be_iterated):
        self._it = the_thing_to_be_iterated
        self._how_many_done = 0

    # Generally speaking, we could provide all sorts of methods for
    # inspecting and advancing external iterators: here we keep it
    # simple, providing only two.
    def is_there_anything_left(self):
        return self._how_many_done < 2

    def give_me_the_next_thing(self):
        if self._how_many_done == 0:
            self._how_many_done = 1
            return self._it._first
        if self._how_many_done == 1:
            self._how_many_done = 2
            return self._it._second
        raise Exception("There is nothing left in this iterator")


# This is how you would write the external iterator to make it conform
# to Python's iterator protocol.
class PyIterACTT:

    def __init__(self, the_thing_to_be_iterated):
        self._it = the_thing_to_be_iterated
        self._how_many_done = 0

    # Python's iterator protocol relies on the presence of the name
    # next.
    def next(self):
        if self._how_many_done == 0:
            self._how_many_done = 1
            return self._it._first
        if self._how_many_done == 1:
            self._how_many_done = 2
            return self._it._second
        raise StopIteration
        



def show_it(thing):
    print thing

a = AlwaysContainsTwoThings('apple','pear')

# Using the internal iterator
a.internal_iterator(show_it)

# Using the external iterator
a_iterator = a.give_me_an_external_iterator()
while a_iterator.is_there_anything_left():
    print a_iterator.give_me_the_next_thing()

# Python for loop implicitly using the Python iterator protocol
# version.
for thing in a:
    print thing
