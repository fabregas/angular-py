

class Test:
    def __init__(self, p, v=2):
        self.p = p
        self._v = v

    def some(self):
        return self._v + self.p

        for i in range(10):
            for j in range(5):
                print(i, j)


t = Test(3)
assert t.some() == 5, 'invalid value, expected 5'
