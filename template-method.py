class Communicator:

    def seasonal_greeting(self):
        # Here starts the concrete algorithm implementation
        self.initiate_communication_stream()
        self.send_message()
        self.hook()
        self.close_communication_stream()
        # Here ends the concrete algorithm implementation

    # Leave this one out on first pass
    def hook(self):
        # Let say this has a default implementation
        pass


class Noisy(Communicator):

    def initiate_communication_stream(self):
        print "Opening window"
        
    def send_message(self):
        print "MERRY CHRISTMAS!!!!"

    def close_communication_stream(self):
        print "Closing window"


class Smoke_signal(Communicator):

    def initiate_communication_stream(self):
        print "Lighting fire"

    def send_message(self):
        print "Waving blanket over fire"

    def close_communication_stream(self):
        print "Pouring water onto fire"


class Telephone(Communicator):

    def initiate_communication_stream(self):
        print "Dialling number"

    def send_message(self):
        print "Merry Christmas"

    def close_communication_stream(self):
        print "Replacing receiver"

    # Over-writing default implementation
    def hook(self):
        print "... and a happy New Year"

n = Noisy()
s = Smoke_signal()
t = Telephone()
for c in (n,s,t):
    c.seasonal_greeting()
    print "================================================================================"

# Don't forget to go back and add the hook
