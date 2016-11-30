# Memento
class LiftMemento:

    def __init__(self, height, id):
        self._height = height
        self._id = id    

class Lift:

    def __init__(self, id):
        self._height = 0
        self._id = id
        
    def up(self):
        self._height += 1
        self.report_height()

    def down(self):
        self._height -= 1
        self.report_height()

    def report_height(self):
        print "Height of %s is %s." % (self._id, self._height)

    def create_memento(self):
        return LiftMemento(
            self._height,
            self._id
        )

    def set_memento(self, memento):
        self._height = memento._height
        self._id = memento._id
        self.report_height()        


# Caretaker
class Caretaker:

    def __init__(self, lift):
        self._memento_list = []
        self.lift = lift

    def undo(self):
        if self._memento_list:
            self.lift.set_memento(self._memento_list.pop())
        else:
            print 'No actions to undo'

class UpCommand(Caretaker):

    def do(self):
        self.lift.up()
        self._memento_list.append(self.lift.create_memento())

class DownCommand(Caretaker):

    def do(self):
        self.lift.down()
        self._memento_list.append(self.lift.create_memento())

class Menu:

    def __init__(self):
        self._actions = []
        self._items = []
        self._exit = False

    def add_item(self, title, action):
        self._items.append((title, action))

    def display(self):
        for n, (title, action) in enumerate(self._items):
            print n, title
        print n+1, "Quit"

    def input_int(self, prompt):
        result = None
        while result is None:
            try:
                result = int(raw_input(prompt))
            except ValueError:
                pass
        return result

    def choose(self):
        choice = self.input_int("Please enter your choice: ")
        try:
            name, action = self._items[choice]
        except IndexError:
            if choice == len(self._items):
                self._exit = True
        else:
            if name == 'Undo' and self._actions:
                self._actions.pop().undo()
            elif name == 'Undo' and not self._actions:
                print 'No actions to undo'
            else:
                action.do()
                self._actions.append(action)


    def run(self):
        while not self._exit:
            self.display()
            self.choose()
        print "Bye"


liftA = Lift("A")
liftB = Lift("B")
menu = Menu()
menu.add_item("A Up",   UpCommand(liftA))
menu.add_item("A Down", DownCommand(liftA))
menu.add_item("B Up",   UpCommand(liftB))
menu.add_item("B Down", DownCommand(liftB))
menu.add_item("Undo", None)
menu.run()

