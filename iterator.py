# Here is a class which can be used as a linked list. Expand the
# class, to give it both an internal and an external iterator. Make
# sure that the external iterator conforms to Python's native iterator
# protocol.

class Node:

    def __init__(self, value, next=None):
        self.value = value
        self.next = next

    def __iter__(self):
        return LinkedListIterator(self)

    # The internal iterator
    def each(self, operation):
        next_node = self
        while next_node is not None:
            operation(next_node.value)
            next_node = next_node.next

# The external iterator
class LinkedListIterator:
    def __init__(self, node):
        self._node = node

    # Python's iterator protocol relies on the presence of the name
    # next.
    def next(self):
        if self._node is not None:
            value = self._node.value
            self._node = self._node.next
            return value

        raise StopIteration
    
        


# This is how you would use the Node class to create a linked list
# containing the elements 1,2,3 and 4.
l = Node(1, Node(2, Node(3, Node (4, None))))



# Apply the composite pattern to create a Tree-like data structure,
# which stores any data that are inserted into it, in sorted order.

# Provide internal and external iterators for the composite.
class Tree:

    def __init__(self, value):
        self._left = Leaf()
        self._value = value
        self._right = Leaf()

    def insert(self, value):
        if value < self._value:
            self._left.insert(value)
        else:
            self._right.insert(value)

    def __iter__(self):
        return TreeIterator(self)



class Leaf:

    "Your code goes here"

class TreeIterator:

    def __init__(self, tree):
        self._tree = tree

    def next(self):
        pass

"Your Leaf iterator class implementation goes here"

# The order in which we insert the data into the tree shouldn't
# matter, the tree should take care of storing them in increasing
# order, and iterating over the tree should give the data in sorted
# order.
t = Tree(5)
t.insert(2)
t.insert(4)
t.insert(9)
t.insert(1)
t.insert(6)
t.insert(3)
t.insert(8)
t.insert(7)

# We will repeat our tests for each of the two iterables we have
# created above.
iterables = l,t

# The output should always be
# 1 2 3 4         1 2 3 4 5 6 7 8 9        


# NB, you would normally *NOT* call __iter__ directly in Python (you
# would use the global iter, or let for loops take care of it), but we
# do it to show how the pattern would be used in a context where there
# is no built-in language support for it.
print "\n########## Using the iterator protocol explicitly ###########"
for thing in iterables:
    iterator = thing.__iter__() # iter(thing)
    try:
        while True:
            print iterator.next(),
    except StopIteration:
        pass
    print "       ",


# Here it is again: this time Python's for loop uses the iterator
# protocol to invoke __iter__.
print "\n########## Using Python's for loop ##########################"
for thing in iterables:
    for n in thing:
        print n,
    print "       ",


# Here is how the internal iterator would be used.
print "\n########## Using the internal iterator ######################"
for thing in iterables:
    def op(item):
        print item,
    thing.each(op)
    print "       ",
