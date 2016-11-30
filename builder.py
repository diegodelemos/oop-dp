from composite_jacek import Menu, MenuAction

# Builder provides a high-level interface for the creation of complex
# objects. The idea is that a high-level overview of the structure of
# the object should be used as a plan. This plan can then be given to
# any of a number builders, each of which should be able to use the
# plan to construct an object. Exactly how the object's components are
# made and the details of how they must be connected at low-level, is
# up to the builder, but the overall sturcture of the object is
# determined by the plan.

# Formally, the plan is called the 'Director'. The director tells the
# builder what to do, but does not interfere in *how* the builder does
# it.

# A key feature of the Builder pattern is that the Builder receives
# high level instructons about the object's composition, until the
# Director issues the "That's all, now give me the result"
# instruction.

# For the purposes of this exercise, we will use the following
# Director, which specifies the sturcture of a menu.

def build_me_a_menu(builder):
    builder.action('Action A', lambda:'Action A')
    builder.action("Action B", lambda:"Action B")
    builder.menu("Submenu 1")
    builder.action("Action 1 A", lambda:"Action 1 A")
    builder.action("Action 1 B", lambda:"Action 1 B")
    builder.menu("Submenu 1 1")
    builder.action("Action 1 1 A", lambda:"Action 1 1 A")
    builder.action("Action 1 1 B", lambda:"Action 1 1 B")
    builder.end_menu()
    builder.action("Action 1 C", lambda:"Action 1 C")
    builder.menu("Submenu 1 2")
    builder.action("Action 1 2 A", lambda:"Action 1 2 A")
    builder.action("Action 1 2 B", lambda:"Action 1 2 B")
    builder.end_menu()
    builder.end_menu()
    builder.action("Action C", lambda:"Action C")
    return builder.getMenu()

# Your task is to implement two different Builders which will be able
# to receive these instructions, and produce appropriate versions of
# the menu described by the Director.

# The first builder should create a textual representation of the
# nested contents of the menu.
class MenuTextMapBuilder:

    indent_size = 8

    def __init__(self):
        self.product = []
        self.depth = 0

    def menu(self, name):
        self.product.append(self._indent() + name + " -->")
        self.depth += 1

    def action(self, name, action):
        self.product.append('{indent}{msg}'.
                            format(indent=self._indent(),
                                   msg=name
                            )
        )

    def end_menu(self):
        if self.depth >= 1:
            self.depth -= 1

    def getMenu(self):
        return '\n'.join(self.product)

    def _indent(self):
        return ' ' * self.indent_size * self.depth


# The menu created in the example usage above, should look like this
# (exactly like this, in the case of MenuTextMapBuilder).
expected_text_view_of_menu = """
Action A
Action B
Submenu 1 -->
        Action 1 A
        Action 1 B
        Submenu 1 1 -->
                Action 1 1 A
                Action 1 1 B
        Action 1 C
        Submenu 1 2 -->
                Action 1 2 A
                Action 1 2 B
Action C"""[1:]


# The second builder should use the Menu classes we developed in the
# exercises for Composite, to create the menu specified by the
# Director.
class MenuBuilder:

    def __init__(self):
        self.nested_menus = [Menu()]

    def menu(self, name):
        new_menu = Menu()
        self.nested_menus[-1].add_item(name, new_menu)
        self.nested_menus.append(new_menu)

    def action(self, name, action):
        self.nested_menus[-1].add_item(name, MenuAction(action))

    def end_menu(self):
        if self.nested_menus:
            self.nested_menus.pop()

    def getMenu(self):
        return self.nested_menus[0]


#################################################################################
# Bits of Python magic creating utilities to test the MenuBuilder:              #
# IGNORE !!!                                                                    #
                                                                                #
from contextlib import contextmanager                                           #
from cStringIO import StringIO                                                  #
import sys                                                                      #
                                                                                #
@contextmanager                                                                 #
def menu_choices(text):                                                         #
    oldstdin = sys.stdin                                                        #
    sys.stdin = StringIO('\n'.join(text))                                       #
    try:                                                                        #
        yield sys.stdin                                                         #
    finally:                                                                    #
        sys.stdin = oldstdin                                                    #
                                                                                #
# End of ignorable magic                                                        #
#################################################################################

# Check that the MenuTextMapBuilder creates what we expect.
assert build_me_a_menu(MenuTextMapBuilder()) == expected_text_view_of_menu
print '*****MenuTextMapBuilder OK*******'

# Check that the Menu builder creates what we expect

#    Build the menu.
run = build_me_a_menu(MenuBuilder()).doit

#    Check that the choice 0 invokes Action A.
with menu_choices('0'):
    assert run() == 'Action A'
#    Check that the choices 2 followed by 1, invoke Action 1 B
with menu_choices('21'):
    assert run() == 'Action 1 B'
#    And so on
with menu_choices('220'):
    assert run() == 'Action 1 1 A'

with menu_choices('23'):
    assert run() == 'Action 1 C'

print '\n**********MenuBuilder OK*********'
print 
print "*********************************"
print "          All correct"
