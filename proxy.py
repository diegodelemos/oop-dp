REPEAT, QUESTION = 10, 3

# Your program contains an object which carries out some expensive
# task.
class WorkerInterface: pass

class Worker(WorkerInterface):

    # We simulate the expense by deliberatly wasting time in the
    # operation.
    def do_something_difficult_with(self, n):
        import time
        time.sleep(1)
        return n + 1

w = Worker()

# If the worker's results are required repeatedly, the we may spend
# signifcant resources (time, in this example) on getting them
for i in range(REPEAT):
    print w.do_something_difficult_with(QUESTION)

# We could make considerable savings by caching the results. We can do
# this by hiding the worker bebind a caching proxy. Clients will talk
# to the worker via the proxy, but they can do so in complete
# ignorance of the proxy's existance: they can talk to the proxy just
# like they would talk to the worker itself.

# Exercise: Implement a caching proxy which will only get the worker
# to work out *new* results. The proxy should remember any questions,
# and corresponding results, that the worker has ever seen, and use
# those to give the answer immediately whenever an already answered
# question is asked again.
class CachingWorkerProxy(WorkerInterface):

    def __init__(self, worker):
        self._cache = {}
        self._worker = worker

    def do_something_difficult_with(self, n):
        if not n in self._cache:
            self._cache[n] = self._worker.do_something_difficult_with(n)

        return self._cache[n]

print "Starting to use proxy"
# Hide the worker behind the proxy
wp = CachingWorkerProxy(w)
# Observe that performance drastically improves.
for i in range(REPEAT):
    print wp.do_something_difficult_with(QUESTION)
