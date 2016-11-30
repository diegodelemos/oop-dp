# Recall the exercise for the Command pattern. In it, we created a
# menu class, which could store commands to be executed.

# In this exercise we will make a hierarchical menu: any menu can
# stored either an action or a submenu. The Menu should be a
# composite: the non-terminal nodes (menus) and terminal leaves
# (actions) should be treated identically.

class Menu:

    def __init__(self):
        self.items = []

    def doit(self):
        for n, (title, action) in enumerate(self.items):
            print n, title
        return self._choose()

    def add_item(self, title, item):
        self.items.append((title,item))

    def _choose(self):
        choice = input("Please choose one ")
        title, item = self.items[choice]
        return item.doit()

class MenuAction:

    def __init__(self, action):
        self.action = action

    def doit(self):
        return self.action()

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
    root.add_item   ('Bagel',      MenuAction(lambda:"bagel"))
    root.add_item   ('Herring',    MenuAction(lambda:"herring"))
    veggies.add_item("Carrot",     MenuAction(lambda:"carrot"))
    veggies.add_item("Tomato",     MenuAction(lambda:"tomato"))
    fruit.add_item  ("Banana",     MenuAction(lambda:"banana"))
    fruit.add_item  ("Citrus",     citrus)
    citrus.add_item ("Orange",     MenuAction(lambda:"orange"))
    citrus.add_item ("Lemon",      MenuAction(lambda:"lemon"))
    citrus.add_item ("Lime",       MenuAction(lambda:"lime"))

    # And you should be able to use it like this

    with standard_input("2"):
        assert root.doit() == 'bagel'

    with standard_input("01"):
        assert root.doit() == 'tomato'

    with standard_input("112"):
        assert root.doit() == 'lime'


    print "\n\n*********************************"
    print "You've passed the tests"


