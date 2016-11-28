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

    LegoCar = FlexibleKid(LegoKit()).make_car()
    assert map(type, LegoCar) == [LegoWheel, LegoWheel, LegoWheel, LegoWheel, LegoChassis, LegoEngine]

    MecanoCar = FlexibleKid(MecanoKit()).make_car()
    assert map(type, MecanoCar) == [MecanoWheel, MecanoWheel, MecanoWheel, MecanoWheel, MecanoChassis, MecanoEngine]

    print "OK"

######################################################################
##                                                                  ##
## Exercise:                                                        ##
##                                                                  ##
## Take the Kid class shown below, and make it more flexible, by    ##
## removing the hard-wired references to Lego components. Introduce ##
## the flexibility by adding an extra layer of indirection: the Kid ##
## should receive a factory class, and ask it for the required      ##
## components (wheel, chassis or engine). The factory gets to       ##
## decide exactly what an engine or chassis or wheel actually *is*. ##
##                                                                  ##
######################################################################

class Kid:

    def make_car(self):
        car = []
        for n in range(4):
            car.append(LegoWheel())
        car.append(LegoChassis())
        car.append(LegoEngine())
        return car


class FlexibleKid:

    def __init__(self, kit):
        # kit object must always implement Kit interface
        # We are encapsulating what varies here
        self._kit = kit

    def make_car(self):
        # Factory method
        car = []
        for n in range(4):
            car.append(self._kit.make_wheel())
        car.append(self._kit.make_chassis())
        car.append(self._kit.make_engine())
        return car


class Kit:

    def make_wheel(self):
        raise NotImplementedError

    def make_engine(self):
        raise NotImplementedError

    def make_chassis(self):
        raise NotImplementedError
    
class LegoKit(Kit):
    # here we could have the classes
    # itself and because types are
    # first class objects we could
    # pass them and instantiate them.
    # The goal of this pattern is to
    # pass types around
    def make_wheel(self):
        return LegoWheel()

    def make_engine(self):
        return LegoEngine()

    def make_chassis(self):
        return LegoChassis() 

class MecanoKit(Kit):

    def make_wheel(self):
        return MecanoWheel()

    def make_engine(self):
        return MecanoEngine()

    def make_chassis(self):
        return MecanoChassis()


test()
