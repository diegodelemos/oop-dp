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
        return LiftMemento(self._id, self._height)

    def set_memento(self, memento):
        self._height = memento._height
        self._id     = memento._id
        self.report_height()

class LiftMemento:

    def __init__(self, id, height):
        self._id     = id
        self._height = height

class UpCommand:

    def __init__(self, lift):
        self.lift = lift

    def do(self):
        self.lift.up()

class DownCommand:

    def __init__(self, lift):
        self.lift = lift

    def do(self):
        self.lift.down()

class UndoCommand:

    def __init__(self, *state_components):
        self._state = state_components
        self._history = []

    def do(self):
        if self._history:
            for memento, substate in zip(self._history.pop(), self._state):
                substate.set_memento(memento)
        else:
            print "Nothing to undo"

    def remember(self):
        self._history.append([ss.create_memento() for ss in self._state])

class Menu:

    def __init__(self):
        self._items = []
        self._exit = False
        self._undo = None

    def add_item(self, title, action):
        self._items.append((title, action))

    def set_undo(self, undo):
        self._undo = undo

    def display(self):
        for n, (title, action) in enumerate(self._items):
            print n, title
        print n+1, "Quit"
        if self._undo: print n+2, "Undo"

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
            if self._undo and choice == len(self._items) + 1:
                self._undo.do()
        else:
            if self._undo: self._undo.remember()
            action.do()

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
menu.set_undo(UndoCommand(liftA, liftB))
menu.run()

