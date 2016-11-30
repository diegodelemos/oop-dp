# Take a simple composite
class Node:

    def __init__(self, value, l1, l2):
        self.value = value
        self.l1 = l1
        self.l2 = l2

    def process_with(self, processor):
        # hey! look processor, you are talking
        # to a node
        return processor.process_node(self)

class Leaf:

    def __init__(self, value):
        self.value = value

    def process_with(self, processor):
        # hey! look processor, you are talking
        # to a leaf        
        return processor.process_leaf(self)


# Here are two example composite structures
fourteen = Node("+",
                Leaf(2),
                Node("x",
                     Leaf(3),
                     Leaf(4)))

twenty = Node("x",
              Node("+",
                   Leaf(2),
                   Leaf(3)),
              Leaf(4))

# Create a visitor which will collect the information stored in the
# composite and present it in fully parenthesized mathematical infix
# notation.

# Hint, you will need to enhance the Node and Leaf classes to make
# them accept the visitor.
class Infix:

    def process_leaf(self, leaf):
        return '{}'.format(leaf.value)

    def process_node(self, node):
        return '({op1} {op} {op2})'.format(op1=node.l1.process_with(self),
                                           op=node.value,
                                           op2=node.l2.process_with(self))

# This is what you are aiming for
infix_processor = Infix()
assert fourteen.process_with(infix_processor) == "(2 + (3 x 4))"
assert twenty  .process_with(infix_processor) == "((2 + 3) x 4)"
print "Infix OK"

# Once you've got the Composite-Visitor combination, it is easy to add
# new operations to your composite. For example, add a new operation
# (visitor) which presents the data stored in the composite in prefix
# notation (Lisp syntax).
class Prefix:

    def process_leaf(self, leaf):
        return '{}'.format(leaf.value)

    def process_node(self, node):
        return '({op} {op1} {op2})'.format(op=node.value,
                                           op1=node.l1.process_with(self),
                                           op2=node.l2.process_with(self))

# Here's what you are aiming for with your prefix processor
prefix_processor = Prefix()
assert fourteen.process_with(prefix_processor) == "(+ 2 (x 3 4))"
assert twenty  .process_with(prefix_processor) == "(x (+ 2 3) 4)"
print "Prefix OK"


# Now that you've got the hang of it, it should be trivial to add a
# postfix (Forth) representation.
class Postfix:


    def process_leaf(self, leaf):
        return '{}'.format(leaf.value)

    def process_node(self, node):
        return '{op1} {op2} {op}'.format(op1=node.l1.process_with(self),
                                 op2=node.l2.process_with(self),
                                 op=node.value)


postfix_processor = Postfix()
assert fourteen.process_with(postfix_processor) == "2 3 4 x +"

assert twenty  .process_with(postfix_processor) == "2 3 + 4 x"
print "Postfix OK"


# And it should take almost no effort at all to add an evaluator:
class Evaluate:

    from operator import mul, div, add, sub
    ops = {'x': mul, '/':div, '+':add, '-':sub}

    def process_leaf(self, leaf):
        return leaf.value

    def process_node(self, node):
        return self.ops[node.value](node.l1.process_with(self),
                                    node.l2.process_with(self))

evaluator = Evaluate()
assert fourteen.process_with(evaluator) == 14
assert twenty  .process_with(evaluator) == 20
print "Evaluate OK"
