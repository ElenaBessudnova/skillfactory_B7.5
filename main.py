from random import randint

# класс точки на поле
class Point:
    # инициализатор класса
    def __init__(self, x, y):
        self.x = x
        self.y = y
# магический метод сравнения
    def __eq__(self, other):
        return self.x == other.x and self.y == other.y
    # магический метод строкового представления
    def __repr__(self):
        return f"({self.x}, {self.y})"
class DeskException(Exception):
    pass
class DeskOutException(Exception):
    def __str__(self):
        return "Выход за границы игрового поля"

class DeskUsedException(Exception):
    def __str__(self):
        return "Такой ход уже был"
class DeskWrongException(Exception):
    pass


class Ship:
    # инициализатор класса
    def __init__(self, head, size, bearings):
        self.head = head
        self.size = size
        self.bearings = bearings
        self.lives = size
    @property
    def points(self):
        ship_points = []
        for i in range(self.size):
            new_x = self.head.x
            new_y = self.head.y
            if self.bearings == 0:
                new_x += i
            elif self.bearings == 1:
                new_y += i
            ship_points.append(Point(new_x, new_y))
        return  ship_points

    def hit(self, hit_point):
         return hit_point in self.points

class Desk:
    def __init__(self, visible = True, size = 6):
        self.size = size
        self.visible = visible

        self.count = 0
        self.field = [["0"] * size for _ in range(size)]
        # список кораблей
        self.ships=[]
        # список занятых точек
        self.used=[]
    # метод ставит корабль на поле
    def add_ship(self, ship):
        for p in ship.points:
            if self.out(p) or p in self.used:
                raise DeskWrongException()
        for p in ship.points:
            self.field[p.x][p.y] = "■"
            self.used.append(p)
        self.ships.append(ship)
        self.border(ship)
    def border(self, ship, verb=False):
        neighborhood = [
            (-1, -1), (-1, 0), (-1, 1),
            (0, -1), (0, 0), (0, 1),
            (1, -1), (1, 0), (1, 1)
        ]
        for p in ship.points:
            for dx, dy in neighborhood:
                current_point = Point(p.x+dx, p.y+dy)
                if(0 <= current_point.x<self.size) and (0 <= current_point.y<self.size) and current_point not in self.used:
                    if verb:
                        self.field[current_point.x][current_point.y] = "*"
                    self.used.append(current_point)
    # форматированный вывод поля в консоль
    def __str__(self):
        res = ""
        res += "  | 1 | 2 | 3 | 4 | 5 | 6 | "
        for i, row in enumerate(self.field):
            res += f"\n{i+1} | " + " | ".join(row) + " |"
        if not (self.visible):
            res = res.replace("■", "0")
        return res
    def out(self, p):
        return not((0 <= p.x < self.size) and (0 <= p.y < self.size))
    def fight(self,p):
        if self.out(p):
            raise DeskOutException()

        self.used.append(p)
        for ship in self.ships:
            if p in ship.points:
                ship.lives -= 1
                self.field[p.x][p.y] = "X"
                if ship.lives == 0:
                    self.count += 1
                    self.border(ship, verb=True)
                    print("Корабль убит")
                    return False
                else:
                    print("Корабль ранен")
                    return True
        self.field[p.x][p.y] = "X"
        print("Мимо")
        return False
    def begin(self):
        self.used = []

class Game:
    def __init__(self, size=6):
        self.size = size
        gamer1 = self.random_play_desk()
        gamer2 = self.random_play_desk()
        gamer2.visible = False
        self.computer = Oppon(gamer2, gamer1)
        self.user = User(gamer1, gamer2)

    def random_play_desk(self):
        desk = None
        while desk is None:
            desk = self.random_ship_location()
        return desk

    def random_ship_location(self, size=6):
        sizeList = [3, 2, 2, 1, 1, 1, 1]
        desk = Desk(size=size)
        trycount = 0
        for l in sizeList:
            while True:
                trycount += 1
                if trycount > 2000:
                    return None
                ship = Ship(Point(randint(0, self.size), randint(0, self.size)), l, randint(0, 1))
                try:
                    desk.add_ship(ship)
                    break
                except DeskWrongException:
                    pass
        desk.begin()
        return desk
    def processGame(self):
        step = 0
        while True:
            print("Ваше поле")
            print(self.user.desk)
            print("Поле противника")
            print(self.computer.desk)
            if step % 2 == 0:
                print("Ваш ход")
                repeat = self.user.move()
            else:
                print("Ход противника")
                repeat = self.computer.move()
            if repeat:
                step -=1
            if self.computer.desk.count == 7:
                print("Вы выйграли!")
                break
            if self.user.desk.count == 7:
                print("Вы проиграли")
                break
            step += 1

class Gamer:
    def __init__(self, desk, oppon):
        self.desk = desk
        self.oppon = oppon
    def next_step(self):
        raise NotImplementedError
    def move(self):
        while True:
            try:
                target = self.next_step()
                repeat = self.oppon.fight(target)
                return repeat
            except DeskException as e:
                print(e)

class Oppon(Gamer):
    def next_step(self):
        while True:
            try:
                p = Point(randint(0,5), randint(0,5))
                print(f"Ход компьютера:{p.x+1} {p.y+1}")
                return p
            except DeskUsedException:
                continue

class User(Gamer):
    def next_step(self):
        while True:
            inputX = input('Введите номер строки  ')
            inputY = input('Введите номер столбца  ')
            if not (inputX.isdigit()) or not(inputY.isdigit()):
                print("Значение должно принимать целочисленные значения, попробуйте снова!")
                continue
            PosX = int(inputX)
            PosY = int(inputY)
            try:
                return Point(PosX-1, PosY-1)
            except DeskUsedException:
                continue
newGame = Game()
newGame.processGame()













