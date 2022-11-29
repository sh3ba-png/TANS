class Mob:
    def __init__(self, mas_coordinate, type, tick):
        self.id = 0
        self.hp = 200
        self.hp_mn = 200
        self.start_hp = self.hp
        self.picture1 = 0  # картинка в первой позиции
        self.picture2 = 0  # картинка во второй позиции
        self.type = type  # дракон или змея
        self.coordinate = 0
        self.mas_coordinate = mas_coordinate
        self.tick = tick
        self.damages = []

    def get_currant_position(self):
        return self.mas_coordinate[self.coordinate]

    def next_position(self):
        if self.coordinate < len(self.mas_coordinate) - 1:
            self.coordinate += 1

    def is_cross_over(self):
        if self.mas_coordinate[self.coordinate] == self.mas_coordinate[-1]:
            return True

    def get_damage(self, damage):
        self.hp -= damage

    def will_hp_at_tick(self, tick_, damage):
        start_hp = self.start_hp
        count_doletit = 0
        for d in self.damages:
            if d[1] < tick_:
                start_hp -= d[0]
                count_doletit += 1
        if start_hp <= 0:
            return 0
        if (count_doletit == len(self.damages)) or (start_hp >= damage):
            return 1
        return 0

    def set_hp(self):
        if self.type == 0:
            self.hp = 100 + self.id * 5
            self.hp_mn = self.hp

        if self.type == 1:
            self.hp = 50 + self.id * 5
            self.hp_mn = self.hp
        self.start_hp = self.hp




