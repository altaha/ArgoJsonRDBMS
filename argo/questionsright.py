
class House(object):
    def __init__(self, sf):
        self.sf = sf

    def is_big(self):
        return True if self.sf > 100 else False


my_house = House(150)
print(House.is_big(my_house))
