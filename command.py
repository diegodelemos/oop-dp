step = 4

###########################################
## Step 1                                ##
##                                       ##
## Stateless, uses first-class functions ##
##                                       ##
## Understand how this code works        ##
###########################################

class Menu:

    def __init__(self):
        self._items = []
        self.exit = False

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
                self.exit = True
        else:
            action()

    def run(self):
        while not self.exit:
            self.display()
            self.choose()
        print "Bye"

menu = Menu()

def up():
    print "Going up"

def down():
    print "Going down"

menu.add_item("Up", up)
menu.add_item("Down", down)
if step == 1:
    menu.run()


################################################################
## Step 2                                                     ##
##                                                            ##
## Make the commands stateful, by linking them to some object ##
##                                                            ##
## Fill in the blanks, using Python's first class functions   ##
################################################################

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
    
liftA = Lift('A')
liftB = Lift("B")
menu = Menu()
menu.add_item("A Up",   liftA.up)
menu.add_item("A Down", liftA.down)
menu.add_item("B Up",   liftB.up)
menu.add_item("B Down", liftB.down)
if step == 2:
    menu.run()

##################################################################
## Step 3:                                                      ##
##                                                              ##
## Same again, but this time avoid using first class functions: ##
## each command must be an object, with a method with an agreed ##
## name which needs to be called to execute the command.        ##
##################################################################

# Hints:

# You will need to implement the commands as classes this time.
class UpCommand:

    def __init__(self, obj):
        self._obj = obj

    def do(self):
        self._obj.up()

class DownCommand:

    def __init__(self, obj):
        self._obj = obj

    def do(self):
        self._obj.down()

# You will need to enhance the Menu class too
class Menu3(Menu):

    def choose(self):
        choice = self.input_int("Please enter your choice: ")
        try:
            name, obj = self._items[choice]
        except IndexError:
            if choice == len(self._items):
                self.exit = True
        else:
            obj.do()

liftA = Lift("A")
liftB = Lift("B")
menu = Menu3()
menu.add_item("A Up",   UpCommand(liftA))
menu.add_item("A Down", DownCommand(liftA))
menu.add_item("B Up",   UpCommand(liftB))
menu.add_item("B Down", DownCommand(liftB))
if step == 3:
    menu.run()

###################################################################
##                                                               ##
## Step 4: Undoing                                               ##
##                                                               ##
## Enhance your command objects with a method which performs the ##
## reverse operation of whatever its normal action method does.  ##
##                                                               ##
## Use this to implement an undo option for yor menu.            ##
##                                                               ##
###################################################################

class Menu4(Menu3):

    def __init__(self):
        self._commands = []
        Menu3.__init__(self)


    def choose(self):
        choice = self.input_int("Please enter your choice: ")
        try:
            name, obj = self._items[choice]
        except IndexError:
            if choice == len(self._items):
                self.exit = True
        else:
            if name != 'Undo':
                self._commands.append(obj)
                obj.do()
            else:
                if self._commands:
                    obj = self._commands.pop()
                    obj.undo()
                else:
                    print 'No more commands to undo'

class UpCommand4:

    def __init__(self, obj):
        self._obj = obj

    def do(self):
        self._obj.up()

    def undo(self):
        self._obj.down()


class DownCommand4(UpCommand):

    def do(self):
        self._obj.down()

    def undo(self):
        self._obj.up()


liftA = Lift("A")
liftB = Lift("B")
up_command_A = UpCommand4(liftA)
down_command_A = DownCommand4(liftA)
up_command_B = UpCommand4(liftB)
down_command_B = DownCommand4(liftB)
menu = Menu4()
menu.add_item("A Up",   up_command_A)
menu.add_item("A Down", down_command_A)
menu.add_item("B Up",   up_command_B)
menu.add_item("B Down", down_command_B)
menu.add_item("Undo",   None)
if step == 4:
    menu.run()
