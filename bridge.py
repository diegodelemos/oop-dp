from abc import ABCMeta, abstractmethod
from os import getcwd
import webbrowser
import Tkinter

#################################################################
##                                                             ##
## This function draws a picture of a man in SVG and views it. ##
##                                                             ##
#################################################################

def man(x,y):
    base_name = 'drawing'
    filename = "{}/{}.svg".format(getcwd(), base_name)
    file = open(filename,'w')
    file.write('<html>\n')
    file.write('<body>\n')
    file.write('<svg width="300" height="300">\n')

    def line(x1,y1,  x2,y2):
        file.write ('<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="black" stroke-width="2" fill-opacity="0" />\n'
                    .format(**locals()))

    def circle(x,y,   r):
        file.write('<circle cx="{x}" cy="{y}" r="{r}" stroke="black" stroke-width="2" fill-opacity="0" />\n'
                   .format(**locals()))

    # limbs
    line  (x,    y+100,    x+20, y+60) # Left leg
    line  (x+40, y+100,    x+20, y+60) # Right leg
    line  (x+20, y+ 30,    x   , y+50) # Left arm
    line  (x+20, y+ 30,    x+40, y+50) # Right arm
    # body
    line  (x+20, y+ 30,    x+20, y+60) # Body
    # head
    circle(x+20, y+ 15, 15)

    file.write('</svg>\n')
    file.write('</body>\n')
    file.write('</html>\n')
    file.close()
    webbrowser.open('file:///'+filename, new=1)

##########################################################################
##                                                                      ##
## This function draws a picture of a dog in Tkinter (Python's standard ##
## GUI library) and views it.                                           ##
##                                                                      ##
##########################################################################

def dog(x,y):
    root = Tkinter.Tk()
    canvas = Tkinter.Canvas(root)

    def line(self, x1,y1, x2,y2):
        self._canvas.create_line(x1,y1, x2,y2,           width=2)

    def circle(self, x,y, r):
        self._canvas.create_oval(x-r,y-r, x+r,y+r,       width=2)

    def rectangle(self, x,y, w,h):
        self._canvas.create_rectangle(x, y,   x+w, y+h,  width=2)

    # legs
    canvas.create_line(x,    y+100,    x+5 , y+80,           width=2) # Front legs
    canvas.create_line(x+10, y+100,    x+5 , y+80,           width=2)
    canvas.create_line(x+30, y+100,    x+35, y+80,           width=2) # Hind legs
    canvas.create_line(x+40, y+100,    x+35, y+80,           width=2)
    # body
    canvas.create_rectangle(x+5, y+65, (x+5)+30, (y+65)+15,  width=2)
    # head
    canvas.create_rectangle(x-7, y+55, (x-7)+20, (y+55)+10,  width=2)
    # tail
    canvas.create_line(x+35, y+65,     x+45, y+60,           width=2)

    canvas.pack()

# dog(100,100)
# man(100,100)

#################################################################################
##                                                                             ##
## Exercise:                                                                   ##
##                                                                             ##
## Use the bridge pattern to make it easy to draw dogs, people, cats,          ##
## elephants (and other mammals) but also any pictures in general using        ##
## either SVG or Tkinter (or any other graphics backend you choose to support) ##
##                                                                             ##
#################################################################################

class Graphics:

    __metaclass__ = ABCMeta

    @abstractmethod
    def circle(self, x,y, r): pass

    @abstractmethod
    def line(self, x1,y1, x2,y2): pass

    @abstractmethod
    def rectangle(self, x,y, w,h): pass



class SVGGraphics:

    def start(self):
        base_name = 'drawing'
        self.filename = "{}/{}.svg".format(getcwd(), base_name)
        self.file = open(self.filename,'w')
        self.file.write('<html>\n')
        self.file.write('<body>\n')
        self.file.write('<svg width="300" height="300">\n')

    def circle(self, x, y, r):
        self.file.write('<circle cx="{x}" cy="{y}" r="{r}" stroke="black" '
                        'stroke-width="2" fill-opacity="0" />\n'
                        .format(**locals()))

    def line(self, x1, y1, x2, y2):
        self.file.write('<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" '
                        'stroke="black" stroke-width="2" fill-opacity="0"'
                        '/>\n'.format(**locals()))

    def rectangle(self, x, y, w, h):
        self.file.write('<rect x="{x}" y="{y}" width="{w}" height="{h}"'
                        ' stroke="black" stroke-width="2" fill-opacity="0"'
                        '/>\n'.format(**locals()))

    def finish(self):
        self.file.write('</svg>\n')
        self.file.write('</body>\n')
        self.file.write('</html>\n')
        self.file.close()
        webbrowser.open('file:///'+self.filename, new=1)


class TkinterGraphics:

    def start(self):
        root = Tkinter.Tk()
        self._canvas = Tkinter.Canvas(root)

    def line(self, x1,y1, x2,y2):
        self._canvas.create_line(x1,y1, x2,y2,           width=2)

    def circle(self, x,y, r):
        self._canvas.create_oval(x-r,y-r, x+r,y+r,       width=2)

    def rectangle(self, x,y, w,h):
        self._canvas.create_rectangle(x, y,   x+w, y+h,  width=2)

    def finish(self):
        self._canvas.pack()


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

    @abstractmethod
    def torso(self, x,y): pass

    @abstractmethod
    def head(self, x,y): pass

    @abstractmethod
    def tail(self, x,y): pass



class Stickman(Creature):

    def legs(self, x, y):
        self._imp.line(x,    y+100, x+20, y+60) # Left leg
        self._imp.line(x+40, y+100, x+20, y+60) # Right leg
        self._imp.line(x+20, y+ 30, x   , y+50) # Left arm
        self._imp.line(x+20, y+ 30, x+40, y+50) # Right arm

    def torso(self, x, y):
        self._imp.line(x+20, y+ 30,    x+20, y+60) # Body

    def head(self, x, y):
        self._imp.circle(x+20, y+ 15, 15)

    def tail(self, x, y):
        pass

class Dog(Creature):
    
    def legs(self, x, y):
        self._imp.line(x, y+100, x+5, y+80) # Front legs
        self._imp.line(x+10, y+100, x+5, y+80)
        self._imp.line(x+30, y+100, x+35, y+80) # Hind legs
        self._imp.line(x+40, y+100, x+35, y+80)

    def torso(self, x, y):
        self._imp.rectangle(x+5, y+65, 30, 15)

    def head(self, x, y):
        self._imp.rectangle(x-7, y+55, 20, 10)

    def tail(self, x, y):
        self._imp.line(x+35, y+65, x+45, y+60)
        
imp = SVGGraphics()
drawing = Drawing(imp)
drawing.start()
# start drawing
dog = Dog(imp)
dog.draw(50, 0)
stickman = Stickman(imp)
stickman.draw(0, 0)
# finish drawing
drawing.finish()

imp = TkinterGraphics()
drawing = Drawing(imp)
drawing.start()
# start drawing
dog = Dog(imp)
dog.draw(50, 0)
stickman = Stickman(imp)
stickman.draw(0, 0)
# finish drawing
drawing.finish()
