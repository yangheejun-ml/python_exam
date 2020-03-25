class CarMixIn:
    def ready(self):
        print("믹스인 레디")
    def start(self):
        print("{} 가 {} 속도로 달립니다.".format(self.name, self.speed))

class Perfromance():
    def __init__(self, name, speed):
        self.name = name
        self.speed = speed
        self.ready()

class SuperCar(CarMixIn, Perfromance):
    def show_info(self):
        print("{}는 {} 속도의 성능입니다.".format(self.name, self.speed))
    def start(self):
        print("스타트")

s = SuperCar("람보르", 300)
s.show_info()
s.start()