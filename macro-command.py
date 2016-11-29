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

    def display(self):
        for n, (title, action) in enumerate(self._items):
            print n, title
        print n+1, "Quit"
    
    def doit(self):
        self.display()
        return self._choose()
    

# Leaf
class MenuAction(Component):

    def __init__(self, command):
        self.command = command

    def doit(self):
        return self.command.do()

class Lift:

    def __init__(self, id):
        self.height = 0
        self.id = id

    def up(self):
        self.height += 1
        self.report_height()

    def down(self):
        self.height -= 1
        self.report_height()

    def report_height(self):
        print "Height of %s is %s." % (self.id, self.height)


class UpCommand:

    def __init__(self, obj):
        self._obj = obj

    def do(self):
        self._obj.up()

    def undo(self):
        self._obj.down()


class DownCommand(UpCommand):

    def do(self):
        self._obj.down()

    def undo(self):
        self._obj.up()


class MacroCommand(object):
    def __init__(self, subcomands):
        self._subcommands = subcommands

    def do(self):
        for command in self._subcommands:
            command.do()

    def undo(self):
        for command in reverse(self._subcommands):
            command.undo()

if __name__ == "__main__":

    liftA = Lift("General")
    liftB = Lift("Banana")
    liftC = Lift("Lemon")
    up_command_A = UpCommand(liftA)
    down_command_A = DownCommand(liftA)
    up_command_B = UpCommand(liftB)
    down_command_B = DownCommand(liftB)
    up_command_C = UpCommand(liftC)
    down_command_C = DownCommand(liftC)

    # You should be able to build a menu like this:
    root    = Menu()
    veggies = Menu()
    fruit   = Menu()
    citrus  = Menu()
    root.add_item("Fruit Building", fruit)
    fruit.add_item("Citrus Building", citrus)
    root.add_item ("General up", MenuAction(up_command_A))
    root.add_item ("General down", MenuAction(down_command_A))
    fruit.add_item ("Banana up", MenuAction(up_command_B))
    fruit.add_item ("Banana down", MenuAction(down_command_B))
    citrus.add_item ("Lemon up", MenuAction(up_command_C))
    citrus.add_item ("Lemon down", MenuAction(down_command_C))


    root.doit()
