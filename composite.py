# Recall the exercise for the Command pattern. In it, we created a
# menu class, which could store commands to be executed.

# In this exercise we will make a hierarchical menu: any menu can
# stored either an action or a submenu. The Menu should be a
# composite: the non-terminal nodes (menus) and terminal leaves
# (actions) should be treated identically.

class Component:

    def doit(self):
        """Performs an action
        """
        pass

class CompositeComponent(Component):

    def add_item(self):
        """Adds and item of type Component
        to the list of components.
        """
        pass

    def remove(self, c):
        """Removes the item `c` of type Component
        from the list of components.
        """        
        pass

    
# Composite
class Menu(CompositeComponent):

    def __init__(self):
        self._items = []

    def add_item(self, title, component):
        self._items.append((title, component))

    def remove(self, c):
        for n, (_, component) in enumerate(self._items):
            if component == c:
                del(self._items[n])

    def _choose(self):
        choice = input("Please choose one ")
        title, item = self._items[choice]
        # Here, with the `Component` interface, we are ensuring
        # every item in the Component list will have a
        # `doit` method
        return item.doit()

    def doit(self):
        for n, (title, component) in enumerate(self._items):
            print n, title
        return self._choose()
    

# Leaf
class MenuAction(Component):

    def __init__(self, command):
        self.command = command

    def doit(self):
        return self.command.do()

class WriteCommand:

    def __init__(self, msg):
        self._msg = msg

    def do(self):
        return self._msg


if __name__ == "__main__":

    # --- Some Python magic to help with the test code: ignore it ------#
    from cStringIO import StringIO                                      #
    from contextlib import contextmanager                               #
    import sys                                                          #
                                                                        #
    @contextmanager                                                     #
    def standard_input(data):                                           #
        previous_stdin = sys.stdin                                      #
        sys.stdin = StringIO('\n'.join(data))                           #
                                                                        #
        try:                                                            #
            yield                                                       #
        finally:                                                        #
            sys.stdin = previous_stdin                                  #
    # ----- End of ignorable Python magic ------------------------------#

    # You should be able to build a menu like this:
    root    = Menu()
    veggies = Menu()
    fruit   = Menu()
    citrus  = Menu()
    root.add_item   ("Vegetables", veggies)
    root.add_item   ("Fruit",      fruit)
    root.add_item   ('Bagel',      MenuAction(WriteCommand("bagel")))
    root.add_item   ('Herring',    MenuAction(WriteCommand("herring")))
    veggies.add_item("Carrot",     MenuAction(WriteCommand("carrot")))
    veggies.add_item("Tomato",     MenuAction(WriteCommand("tomato")))
    fruit.add_item  ("Banana",     MenuAction(WriteCommand("banana")))
    fruit.add_item  ("Citrus",     citrus)
    citrus.add_item ("Orange",     MenuAction(WriteCommand("orange")))
    citrus.add_item ("Lemon",      MenuAction(WriteCommand("lemon")))
    citrus.add_item ("Lime",       MenuAction(WriteCommand("lime")))

    # And you should be able to use it like this

    with standard_input("2"):
        assert root.doit() == 'bagel'

    with standard_input("01"):
        assert root.doit() == 'tomato'

    with standard_input("112"):
        assert root.doit() == 'lime'


    print "\n\n*********************************"
    print "You've passed the tests"

    root.doit()
