from abc import ABCMeta, abstractmethod
from os import getcwd
import webbrowser
import Tkinter

class Graphics:

    __metaclass__ = ABCMeta

    @abstractmethod
    def circle(self, x,y, r): pass

    @abstractmethod
    def line(self, x1,y1, x2,y2): pass

    @abstractmethod
    def rectangle(self, x,y, w,h): pass

class SVGGraphics(Graphics):

    def start(self):
        base_name = 'drawing'
        self._filename = "{}/{}.svg".format(getcwd(), base_name)
        self._file = open(self._filename,'w')
        self._file.write('<html>\n')
        self._file.write('<body>\n')
        self._file.write('<svg width="100" height="100">\n')

    def finish(self):
        self._file.write('</svg>\n')
        self._file.write('</body>\n')
        self._file.write('</html>\n')
        self._file.close()
        webbrowser.open('file:///'+self._filename, new=1)

    def circle(self, x,y, r):
        self._file.write('<circle cx="{x}" cy="{y}" r="{r}" stroke="black" stroke-width="2" fill-opacity="0" />\n'
                         .format(**locals()))

    def line(self, x1,y1, x2,y2):
        self._file.write ('<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="black" stroke-width="2" fill-opacity="0" />\n'
                          .format(**locals()))

    def rectangle(self, x,y, w,h):
        self._file.write('<rect x="{x}" y="{y}" width="{w}" height="{h}" stroke="black" stroke-width="2" fill-opacity="0" />\n'
                         .format(**locals()))

class TkInterGraphics(Graphics):

    def start(self):
        root = Tkinter.Tk()
        self._canvas = Tkinter.Canvas(root)

    def finish(self):
        self._canvas.pack()

    def line(self, x1,y1, x2,y2):
        self._canvas.create_line(x1,y1, x2,y2,           width=2)

    def circle(self, x,y, r):
        self._canvas.create_oval(x-r,y-r, x+r,y+r,       width=2)

    def rectangle(self, x,y, w,h):
        self._canvas.create_rectangle(x, y,   x+w, y+h,  width=2)

################################################################################

class Abstraction:

    __metaclass__ = ABCMeta

    def __init__(self, implementation):
        self._imp = implementation

class Drawing(Abstraction):

    def start(self):  self._imp.start()

    def finish(self): self._imp.finish()

class Creature(Abstraction):

    def draw(self, x,y):
        self.legs (x,y)
        self.torso(x,y)
        self.head (x,y)
        self.tail (x,y)

    @abstractmethod
    def legs(self, x,y): pass
p
    @abstractmethod
    def torso(self, x,y): pass

    @abstractmethod
    def head(self, x,y): pass

    @abstractmethod
    def tail(self, x,y): pass

class Man(Creature):

    def legs(self, x,y):
        self._imp.line  (x,    y+100,    x+20, y+60) # Left leg
        self._imp.line  (x+40, y+100,    x+20, y+60) # Right leg
        self._imp.line  (x+20, y+ 30,    x   , y+50) # Left arm
        self._imp.line  (x+20, y+ 30,    x+40, y+50) # Right arm

    def torso(self, x,y):
        self._imp.line  (x+20, y+ 30,    x+20, y+60) # Body

    def head(self, x,y):
        self._imp.circle(x+20, y+ 15, 15)

    def tail(self, x,y): pass

class Dog(Creature):

    def legs(self, x,y):
        self._imp.line(x,    y+100,    x+5 , y+80) # Front legs
        self._imp.line(x+10, y+100,    x+5 , y+80)
        self._imp.line(x+30, y+100,    x+35, y+80) # Hind legs
        self._imp.line(x+40, y+100,    x+35, y+80)

    def torso(self, x,y):
        self._imp.rectangle(x+5, y+65 , 30, 15)

    def head(self, x,y):
        self._imp.rectangle(x-7, y+55, 20, 10) # Head

    def tail(self, x,y):
        self._imp.line(x+35, y+65,    x+45, y+60) # Tail

def man_with_dog(implementation):
    d = Drawing(implementation)
    man = Man(implementation)
    dog = Dog(implementation)
    d.start()
    man.draw( 0,0)
    dog.draw(50,0)
    d.finish()

svg = SVGGraphics()
tki = TkInterGraphics()
man_with_dog(svg)
man_with_dog(tki)

# On one side of the bridge, you can describe the components of your
# program at a high level, and use the interface these components
# provide to write complex programs in which the components interact
# in various ways. All this can be done in complete ignorance of how
# these components are actually implemented.

# On the other side of the bridge, you provide completely independent
# sets of implementations of the elements which are required to make
# the above components actually work.

# The bridge between the two sides:

# 1. Separates the concerns of expressing your high-level logic (what
#    components there are and how they are related and interact)from
#    the low-level details of how the components are
#    implementented. In context of the example code, you can draw a
#    man walking his dog, or a savannah scene or even a technical
#    drawing of a rocket or some abstract art etc. without caring in
#    the slightest whether they will end up being drawn using SVG or
#    Tkinter or anything else. The artist and the rocket designer
#    doesn't need to know anything about SVG and Tkinter, while the
#    SVG expert doesn't need to know anything about rockets or
#    savannahs..

# 2. Provides flexibility by allowing the choice of low-level
#    implementation to be changed without having to touch the
#    high-level description of the program's behaviour. In our example
#    context, once you've drawn your man walking his dog model, it
#    will work with all back ends.

# 3. Avoids class explosion, by turning an N * M problem into an N + M
#    problem: N interfaces on one side of the bridge can be combined
#    with M backends on the other side of the bridge to give N * M
#    possible combinations.
