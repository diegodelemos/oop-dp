import sys

LEFT, RIGHT = 4,76

################################################################################
# The harness which runs a simple simulation. It's not part of the
# pattern and you can ignore it.
def clear_screen():
    return [None] * 80

def show_screen(screen):
    for thing in screen:
        sys.stdout.write(str(thing) if thing is not None else ' ')
    print

def step(dt):
    screen = clear_screen()
    for p in particles:
        p.move(dt)
        p.draw(screen)
    show_screen(screen)

def go():
    for n in range(60):
        step(0.7)
    print
    print "=" * 80
################################################################################
# The simplest, naive implementation of the basic particle
class Particle:

    def __init__(self, x, v, id):
        self.position = x
        self.speed = v
        self.id = id

    def move(self, dt):
        self.position += self.speed * dt
        if not (LEFT < self.position < RIGHT):
            self.speed = - self.speed
        if self.position > RIGHT:
            self.position = RIGHT - (self.position - RIGHT)
        if self.position < LEFT:
            self.position = LEFT + (LEFT - self.position)

    def draw(self, screen):
        screen[int(self.position)] = self.id

# An enhanced version of the particle: it makes a noise each time it
# bounces off a boundary.
class NoisyParticle(Particle):

    def move(self, dt):
        self.bang = None
        before = self.speed
        Particle.move(self, dt)
        after = self.speed
        if after*before < 0:
            if self.speed < 0:
                self.bang = 'r'
            else:
                self.bang = 'l'

    def draw(self, screen):
        Particle.draw(self, screen)
        if self.bang == 'l':
            screen[:4] = "BANG"
        if self.bang == 'r':
            screen[-4:] = "BANG"

class CountingParticle(Particle):

    def __init__(self, *args):
        Particle.__init__(self, *args)
        self._count = 0

    def move(self, dt):
        before = self.speed
        Particle.move(self, dt)
        after = self.speed
        if after*before < 0:
            self._count += 1

    def draw(self, screen):
        Particle.draw(self, screen)
        screen[int(self.position)] = self._count
        
particles = [Particle(20, 5.9, 'a'),
             NoisyParticle(40,6.9,'b'),
             CountingParticle(60, 7.9, 0)]
go()


# A decorator which enhances the Particle class: it prints "BANG"
# whenever the particle bounces off a boundary.

# Using this decorator class, we can take an ordinary Particle and (at
# run time) add the extra functionality provided by NoisyParticle, to
# it.

class Bang:

    def __init__(self, component):
        self.component = component

    def move(self,dt):
        self.bang = None
        before = self.component.speed
        self.component.move(dt)
        after = self.component.speed
        if after*before < 0:
            if self.component.speed < 0:
                self.bang = 'r'
            else: 
                self.bang = 'l'

    def draw(self, screen):
        self.component.draw(screen)
        if self.bang == 'l':
            screen[:4] = "BANG"
        if self.bang == 'r':
            screen[-4:] = "BANG"

################################################################################
# A simple test run: 4 particles bounce around, one of them is Bang-decorated.
particles = map(Particle, [10, 30, 50, 70], [2,3,4,5], range(4))
particles[-1] = Bang(particles[-1])
go()

################################################################################

# Exercise

# Introduce a second, orthogonal, decorator, which allows us to
# enhance a Particle with the extra functionality provided by
# CountingParticle.

# It should be possible to *compose* decorators: you should be able to
# wrap a single Particle in both the Noisy decorator and the Counting
# decorator. To do this, you will have to think carefully about the
# interface that the original Particle must provide. It turns out that
# the original naive implementation's interface is not complete
# enough.

class TheInterface:

    def move(self, dt):
        raise NotImplementedError

    def draw(self, screen):
        raise NotImplementedError

    def speed(self):
        raise NotImplementedError

    def position(self):
        raise NotImplementedError


class Particle(TheInterface):

    def __init__(self, x, v, id):
        self._position = x
        self._speed = v
        self._id = id

    def move(self, dt):
        self._position += self._speed * dt
        if not (LEFT < self._position < RIGHT):
            self._speed = - self._speed
        if self._position > RIGHT:
            self._position = RIGHT - (self._position - RIGHT)
        if self._position < LEFT:
            self._position = LEFT + (LEFT - self._position)

    def draw(self, screen):
        screen[int(self._position)] = self._id

    def speed(self):
        return self._speed

    def position(self):
        return self._position

class ParticleDecorator(TheInterface):    
    
    def __init__(self, particle):
        self._particle = particle

    def move(self, dt):
        self._particle.move(dt)

    def draw(self, screen):
        self._particle.draw(screen)

    def speed(self):
        return self._particle.speed()

    def position(self):
        return self._particle.position()

        
class Bang(ParticleDecorator):

    def __init__(self, particle):
        ParticleDecorator.__init__(self, particle)

    def move(self, dt):
        self.bang = None
        before = self.speed()
        # prevent from moving twice
        self._particle.move(dt)
        after = self.speed()
        if after*before < 0:
            if self.speed() < 0:
                self.bang = 'r'
            else: 
                self.bang = 'l'

    def draw(self, screen):
        self._particle.draw(screen)
        if self.bang == 'l':
            screen[:4] = "BANG"
        if self.bang == 'r':
            screen[-4:] = "BANG"



class Count(ParticleDecorator):
    
    def __init__(self, particle):
        ParticleDecorator.__init__(self, particle)
        self._count = 0

    def move(self, dt):
        before = self.speed()
        self._particle.move(dt)
        after = self.speed()
        if after*before < 0:
            self._count += 1

    def draw(self, screen):
        self._particle.draw(screen)
        screen[int(self.position())] = self._count

        
################################################################################

# Once you've finished, you should be able to run the following code,
# and it should give sensible output.

particles = (           Particle(10,2,'+'),
                   Bang(Particle(30,3,'x')),
             Count     (Particle(50,4, 0 )),
             Count(Bang(Particle(60,5, 0 ))),
             Bang(Count(Particle(70,5, 0 ))))

go()
