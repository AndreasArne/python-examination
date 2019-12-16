class C1():
    def f(self):
        self._f1()

    def _f1(self):
        print("f1")


class C2(C1):
    def __init__(self):
        super().f()
    def _f1(self):
        print("new f1")

c2 = C2()