# Here are three classes. They are not linked in any formal way. They
# can be controlled independently.
class Screen_saver:

    _options = ["None", "Black screen", "Machine Name", "LHC@Home"]

    def select(self, option):
        try:
            print "Screen saver set to:", self._options[option]
        except IndexError:
            print "Unknown screen saver"

    def switch_on_screen_saver_after(self, time):
        print "Screen saver"

class Screen_sleep:

    def sleep_after(self, time):
        if time:
            print "Screen will be switched off after %d minutes of inactivity" % time
        else:
            print "Screen sleep disabled"

class Hibernator:

    def sleep_after(self, time):
        if time:
            print "Machine will hibernate after %d minutes of inactivity" % time
        else:
            print "Hibernation switched off"

screen_saver = Screen_saver()
screen_sleep = Screen_sleep()
hibernator   = Hibernator()


screen_saver.select(2)
screen_sleep.sleep_after(30)
hibernator.sleep_after(45)
print "================================================================================"

# Without removing the ability to control the classes independently,
# create a Facade which provides a more convenient interface for
# controlling these classes in concert, in the following two ways:

# 1. Maximum energy saving mode: the cheapest screen saver should be
#    chosen, and both the screen and the machine should switch off
#    after only a brief period of inactivity.

# 2. Intensive work on LHC@Home: you don't want the screen or the
#    machine to switch off at all.

class ComputerFacade:

    def __init__(self, screen_saver, screen_sleep, hibernator):
        self.screen_saver = screen_saver
        self.screen_sleep = screen_sleep
        self.hibernator = hibernator

    def maximum_energy_saving(self):
        self.screen_saver.select(1)
        self.screen_saver.switch_on_screen_saver_after(6)
        self.screen_sleep.sleep_after(18)
        self.hibernator.sleep_after(30)

    def intensive_work(self):
        self.screen_saver.select(3)
        self.screen_saver.switch_on_screen_saver_after(0)
        self.screen_sleep.sleep_after(0)
        self.hibernator.sleep_after(0)


computer_facade = ComputerFacade(Screen_saver(),
                                 Screen_sleep(),
                                 Hibernator())

print('Turning on maximum energy saving mode')
computer_facade.maximum_energy_saving()
print "================================================================================"
print('Turning on intensive work mode')
computer_facade.intensive_work()
print "================================================================================"
