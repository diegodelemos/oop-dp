##################################################################
# Exercise: You are given a menu implemented using the composite #
# pattern. Your task is to provide both internal and external    #
# iterators which traverse the menu in depth-first order.        #
##################################################################

class Menu:

    def __init__(self):
        self.items = []

    def doit(self):
        for n, (title, action) in enumerate(self.items):
            print n, title
        self._choose()

    def add_item(self, title, item):
        self.items.append((title,item))

    def _choose(self):
        choice = input("Please choose one ")
        title, item = self.items[choice]
        item.doit()

    def __iter__(self):
        for _, item in self.items:
            for subitem in item:
                yield subitem

    def each(self, op):
        for item in self:
            op(item)

class MenuAction:

    def __init__(self, action):
        self.action = action

    def doit(self):
        print self.action()

    def __iter__(self):
        yield self

    def each(op):
        for item in self:
            show(op)
    
# Here is 
root    = Menu()
veggies = Menu()
fruit   = Menu()
root.add_item("Vegetables", veggies)
root.add_item("Fruit",      fruit)
root.add_item('Bagel',   MenuAction(lambda:"bagel"))
root.add_item('Herring', MenuAction(lambda:"herring"))
veggies.add_item("Carrot", MenuAction(lambda:"carrot"))
veggies.add_item("Tomato", MenuAction(lambda:"tomato"))
fruit.add_item("Banana", MenuAction(lambda:"banana"))
fruit.add_item("Orange", MenuAction(lambda:"orange"))
################################################################################
# Test: both iterations should traverse the above menu in the order
#    carrot
#    tomato
#    banana
#    orange
#    bagel
#    herring

print " ########################## External iterator ######"
for item in root: # Python's for loop will use the external iterator
    print item.action()
print " ########################## Internal iterator ######"
def show(item):
    print item.action()

root.each(show)
