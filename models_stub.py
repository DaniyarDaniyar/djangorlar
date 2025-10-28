# models_stub.py
class Model:
    _db = {}
    _id = 1

    def __init__(self, **kwargs):
        self.id = Model._id
        Model._id += 1
        for k, v in kwargs.items():
            setattr(self, k, v)
        Model._db[self.id] = self

    @classmethod
    def all(cls):
        return list(cls._db.values())

class User(Model):
    def __init__(self, name, age):
        super().__init__(name=name, age=age)

def demo():
    User._db.clear()
<<<<<<< HEAD
<<<<<<< HEAD
    User("Frank", 25)
=======
<<<<<<< HEAD
    User("John", 25)
=======
    User("Daniyar", 25)
>>>>>>> 66f2641 (duplicate3:change)
>>>>>>> 3316f2b (duplicate3:change)
=======
    User("Daniyar", 25)
>>>>>>> 0c707ff (duplicate3:change)
    User("Bob", 30)
    for u in User.all():
        print(u.id, u.name, u.age)

if __name__ == "__main__":
    demo()
