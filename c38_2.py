class Dog:
    def __init__(self, name, breeding, age, weight):
        self.name = name
        self.breeding = breeding
        self.age = age
        self.weight = weight

    def sleep(self):
        print(f"{self.name} спит...")

    def eat(self, food):
        self.weight += 0.5
        print(f"{self.name} кушает {food}.")

    def info(self):
        print(f"Имя - {self.name}, возраст - {self.age}, порода - {self.breeding}, вес - {self.weight}")

dog1 = Dog('Белка', 'лайка', 3, 4)
dog2 = Dog('Стрелка', 'болонкка', 1, 3)
dog1.sleep()
dog2.sleep()
dog1.info()
dog2.info()

dog1.eat('meat')
dog2.eat('milk')
dog1.info()
dog2.info()