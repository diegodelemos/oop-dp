class Node:

    def __init__(self, value, next=None):
        self.value = value
        self.next = next

    def __iter__(self):
        return LinkedListIterator(self)

    # Iterative version
    def each(self, operation):
        current = self
        while current.next is not None:
            operation(current.value)
            current = current.next
        operation(current.value)

    # Recursive version
    def each(self, operation):
        operation(self.value)
        if self.next:
            self.next.each(operation)

class LinkedListIterator:

    def __init__(self, head):
        self.head = head

    def next(self):
        if self.head is not None:
            value = self.head.value
            self.head = self.head.next
            return value
        raise StopIteration

l = Node(1, Node(2, Node(3, Node (4, None))))

################################################################################
################################################################################

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

    def each(self, op):
        self._left.each(op)
        op(self._value)
        self._right.each(op)

class Leaf:

    def insert(self, value):
        self._left = Leaf()
        self._value = value
        self._right = Leaf()
        # When data is stored in a leaf
        # if becomes a Tree
        # So this is a `state` pattern
        self.__class__ = Tree

    def __iter__(self):
        return LeafIterator()

    def each(self, op):
        pass

class TreeIterator:

    def __init__(self, tree):
        self._subiterators = [iter(tree._left), iter([tree._value]), iter(tree._right)]

    def next(self):
        while self._subiterators:
            try:
                return self._subiterators[0].next()
            except StopIteration:
                self._subiterators.pop(0)
        raise StopIteration

class LeafIterator:

    def next(self):
        raise StopIteration


# Have you noticed the use of the State and Composite patterns in
# Tree/Leaf ?

            
# For Python programmers: The implementations shown above, are very
# poor from a Python perspective. Two obvious ways improving them
# would be to use itertools.chain on the TreeIterator _subiterators,
# or (better still) avoid the need to create the TreeIterator class,
# by implementing Tree.__iter__ as a generator function.  However, in
# this course we ignore these possibilitiesq, as this is not a course
# about Python, and we don't want to waste non-Python programmers'
# time on Python-specific explanations.

# In Python, you might choose to implement the external
# iterator for Tree along these lines:

def __iter__(self):
    for item in self._left:
        yield item
    yield self._value
    for item in self._right:
        yield item

# To test it, uncomment this line
# Tree.__iter__ = __iter__

# while the implementation for Leaf might look like this:

def __iter__(self):
    return
    yield

# To test it, uncomment this line
# Leaf.__iter__ = __iter__

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
