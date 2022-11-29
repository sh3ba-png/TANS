import math


class Bullet:
    def __init__(self, start_pos, end_pos, damage, mob, castle, BULLET_SPEED, INDENT, WIDTH):
        dist = math.sqrt((start_pos.x - end_pos.x) ** 2 + (start_pos.y - end_pos.y) ** 2)
        self.cur_pos = start_pos
        self.end_pos = end_pos
        self.damage = damage
        self.mob = mob
        self.castle = castle
        self.vec = (((end_pos.x - start_pos.x) / dist) * BULLET_SPEED, ((end_pos.y - start_pos.y) / dist) * BULLET_SPEED)
        self.INDENT = INDENT
        self.WIDTH = WIDTH

    def new_step(self):
        if self.mob.hp <= 0:
            return 0
        self.cur_pos.x += self.vec[0]
        self.cur_pos.y += self.vec[1]
        if self.cur_pos.x < self.INDENT * 2/3 or self.cur_pos.y < self.INDENT * 2/3 or self.cur_pos.x > self.WIDTH - self.INDENT * 2/3:
            return 0
