class Person:

    def __init__(self, name, age):
        self.name = name
        self.age = age

    def __repr__(self):
        return self.name

    @staticmethod
    def _key(self):
        return f'{self.name}_{self.age}'

    def __eq__(self, other):
        return self._key(self) == self._key(other)

    # hash类型的集合对自身成员的hash操作：set(),  frozenset([iterable]),   dict(**kwarg)
    def __hash__(self):
        return hash(self._key(self))


p1 = Person('zs', 20)
p2 = Person('lz', 32)
p3 = Person('lz', 32)
print(p1 == p2, p2 == p3)

data = [p1, p2, p3]
print(len(data), len(set(data)))
print(set(data))
