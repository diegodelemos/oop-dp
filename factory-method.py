######################################################################
## We start off with some Python magic (related to giving our       ##
## objects informative printed representations) which you can       ##
## mostly ignore.                                                   ##
##                                                                  ##
## What you need to take away from this section is that we have two ##
## class hierarchies, the Lego hierarchy and the Mecano hierarchy,  ##
## and that in each hierarchy there are three concrete classes:     ##
## each hierarchy contains a Wheel class, a Chassis class and an    ##
## Engine class.                                                    ##
######################################################################

def __repr__(self): return "a " + self.__class__.__name__

class Lego(object):
    __repr__ = __repr__

class LegoWheel(Lego):   pass
class LegoChassis(Lego): pass
class LegoEngine(Lego):  pass


class Mecano(object):
    __repr__ = __repr__

class MecanoWheel(Mecano):   pass
class MecanoChassis(Mecano): pass
class MecanoEngine(Mecano):  pass

#########################################################
##                                                     ##
## Some tests to check the implementation's behaviour. ##
##                                                     ##
#########################################################

def test():

    LegoCar = LegoKid().make_car()
    assert map(type, LegoCar) == [LegoWheel, LegoWheel, LegoWheel, LegoWheel, LegoChassis, LegoEngine]

    MecanoCar = MecanoKid().make_car()
    assert map(type, MecanoCar) == [MecanoWheel, MecanoWheel, MecanoWheel, MecanoWheel, MecanoChassis, MecanoEngine]

    print "OK"

######################################################################
##                                                                  ##
## Exercise:                                                        ##
##                                                                  ##
## Create a superclass, which establishes a template for creating   ##
## cars: For our purposes, cars are made by sticking four wheels, a ##
## chassis and an engine, into a Python list.                       ##
##                                                                  ##
## Create different subclasses, which, in their defininitions of    ##
## relevant methods, specify what exactly a wheel, or a chassis or  ##
## an engine *is*.                                                  ##
##                                                                  ##
######################################################################

class Kid:

    def make_car(self):
        # Define how generic cars are made: just stick four wheels, a
        # chassis and an engine into a Python list.
        car = []
        for n in range(4):
            car.append(self.wheel())
        car.append(self.chassis())
        car.append(self.engine())        
        # You will need to call self.wheel, self,chassis an
        # self.engine, to fill the list.
        return car

    def wheel(self):
        raise NotImplementedError

    def chassis(self):
        raise NotImplementedError

    def engine(self):
        raise NotImplementedError


class LegoKid(Kid):

    def wheel(self):
        return LegoWheel()

    def chassis(self):
        return LegoChassis()        

    def engine(self):
        return LegoEngine()        


class MecanoKid(Kid):

    def wheel(self):
        return MecanoWheel()

    def chassis(self):
        return MecanoChassis()

    def engine(self):
        return MecanoEngine()

test()
