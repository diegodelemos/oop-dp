## Structural pattern
# Object adapter: Exposing just the `size`
# `insert` `lookup`, `remove` and `does_map`
class ObjectAdapter:

    def __init__(self):
        self.map = dict()

    def size(self):
        return len(self.map)

    def insert(self, key, value):
        self.map[key] = value

    def lookup(self, key):
        return self.map.get(key)

    def remove(self, key):
        if self.map.get(key):
            del(self.map[key])

    def does_map(self, key):
        return key in self.map

# Class adapter: Exposing dict methods and the `size`
# `insert` `lookup`, `remove` and `does_map` new ones.
class ClassAdapter(dict):

    def size(self):
        return len(self)

    def insert(self, key, value):
        self[key] = value

    def lookup(self, key):
        return self.get(key)

    def remove(self, key):
        if self.get(key):
            del(self[key])

    def does_map(self, key):
        return key in self


def test(Map):
    m = Map()
    # The object starts out empty
    assert m.size() == 0
    # Adding two mappings, grows its size to two.
    m.insert(2,4)
    m.insert(3,9)
    assert m.size() == 2
    # The entered mappings can be looked up
    assert m.lookup(3) == 9
    # But others just give None
    assert m.lookup(4) == None
    # Removing non-existent keys is silently does nothing
    assert m.remove(4) == None
    assert m.size() == 2
    # Removing existing keys silently reduces the size
    assert m.remove(2) == None
    assert m.size() == 1
    # does_map checks for presence of keys
    assert     m.does_map(3)
    assert not m.does_map(2)
    print Map.__name__ + " passed the tests"
