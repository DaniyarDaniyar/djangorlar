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
    User("Alice", 25)
    User("Bob", 30)
    for u in User.all():
        print(u.id, u.name, u.age)

if __name__ == "__main__":
    demo()
