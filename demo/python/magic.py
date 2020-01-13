class Person:

    def __init__(self, name, age):
        self._name = name
        self._age = age
        self._money = 100

    def __repr__(self):
        return self._name

    @staticmethod
    def _key(self):
        return f'{self._name}_{self._age}'

    def __eq__(self, other):
        return self._key(self) == self._key(other)

    # hash类型的集合对自身成员的hash操作：set(),  frozenset([iterable]),   dict(**kwarg)
    def __hash__(self):
        return hash(self._key(self))

    """ __getattr__, __setattr__, __delattr__
    p = Person('lz', 32)
    # print(p.name)
    p.name = 'ppt'
    print(p.__dict__)
    del p.name
    print(p.__dict__)
    结果：
    # __setattr__: _name lz
    # __setattr__: _age 32
    # __setattr__: name ppt
    # {'_name': 'lz', '_age': 32, 'name': 'ppt'}
    # __delattr__: name
    # {'_name': 'lz', '_age': 32}
    """
    def __getattr__(self, key):
        print('__getattr__', key)
        return f'{self._name}_{self._age}'

    # def __setattr__(self, key, val):
    #     print('__setattr__:', key, val)
    #     self.__dict__[key] = val

    # def __delattr__(self, key):
    #     print('__delattr__:', key)
    #     # object.__delattr__(self, key)
    #     self.__dict__.pop(key, None)

    """property
    # p = Person('lz', 32)
    # print(p.money)
    # p.money = 90
    # print(p.money)
    """
    @property
    def money(self):
        print("getter")
        return self._money

    @money.setter
    def money(self, val):
        print('setter')
        self._money += val

    @money.deleter
    def money(self):
        # del self._money
        self._money -= 10

def hash():
    p1 = Person('zs', 20)
    p2 = Person('lz', 32)
    p3 = Person('lz', 32)
    print(p1 == p2, p2 == p3)

    data = [p1, p2, p3]
    print(len(data), len(set(data)))
    print(set(data))

