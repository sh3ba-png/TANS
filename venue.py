import math


class Point:  # место встречи
    def __init__(self, x, y):
        self.x = x
        self.y = y


def core(position_of_tower, position_of_mob, Vm, Vp, start_position, left_turn, right_turn, finish_position, t1=0):
    # моб идет сверху
    if left_turn.y == position_of_mob.y and position_of_mob.x != right_turn.x:
        # CosAngle - угол между горизонталью и башней (< 90*)
        Dy = abs(position_of_mob.y - position_of_tower.y)
        Dx = abs(position_of_mob.x - position_of_tower.x)
        hypotenuse = math.sqrt(Dy ** 2 + Dx ** 2)
        if position_of_mob.x > position_of_tower.x:
            CosAngle = -Dx / hypotenuse
        else:
            CosAngle = Dx / hypotenuse
        # Из теоремы косинусов
        # (t**2) * (Vp**2 - Vm**2) + t * 2 * g * Vm * CosAngle - g**2 = 0
        # D = b**2 - 4 * a * c
        if t1 == 0:
            D = (2 * hypotenuse * Vm * CosAngle) ** 2 - 4 * (Vp**2 - Vm**2) * (- hypotenuse**2)
            t = (-(2 * hypotenuse * Vm * CosAngle) + math.sqrt(D)) / (2 * (Vp**2 - Vm**2))
            meeting_position = Point(position_of_mob.x + t * Vm, position_of_mob.y)
        else:
            # t^2*(Vp^2 - Vm^2) + t*(2*Vm^2*t1 + 2*g*Vm*cos) - g^2 - Vm^2*t1^2 - 2*g*Vm*t1*cos
            D = (2 * Vm**2 * t1 + 2 * hypotenuse * Vm * CosAngle) ** 2 - 4 * (Vp**2 - Vm**2) * (- hypotenuse**2 - Vm**2 * t1**2 - 2 * hypotenuse * Vm * t1 * CosAngle)
            t = (-(2 * Vm**2 * t1 + 2 * hypotenuse * Vm * CosAngle) + math.sqrt(D)) / (2 * (Vp**2 - Vm**2))
            meeting_position = Point(position_of_mob.x + abs(t - t1) * Vm, position_of_mob.y)
        t1 = 0
        if meeting_position.x > right_turn.x:
            t1 = abs(position_of_mob.x - right_turn.x) / Vm  # Время требуемое для того, чтобы дойти до угла
            meet_pos_after_angle, t = core(position_of_tower, right_turn, Vm, Vp, start_position, left_turn, right_turn,
                                        finish_position, t1)
            meeting_position = Point(meet_pos_after_angle.x, meet_pos_after_angle.y)
        return meeting_position, t + t1
    elif position_of_mob.x == start_position.x:
        Dy = abs(position_of_mob.y - position_of_tower.y)
        Dx = abs(position_of_mob.x - position_of_tower.x)
        hypotenuse = math.sqrt(Dy ** 2 + Dx ** 2)
        if position_of_mob.y < position_of_tower.y:
            CosAngle = -Dy / hypotenuse
        else:
            CosAngle = Dy / hypotenuse
        # Из теоремы косинусов
        # (t**2) * (Vp**2 - Vm**2) + t * 2 * g * Vm * CosAngle - g**2 = 0
        # D = b**2 - 4 * a * c
        D = (2 * hypotenuse * Vm * CosAngle) ** 2 - 4 * (Vp ** 2 - Vm ** 2) * (- hypotenuse ** 2)
        t = (-(2 * hypotenuse * Vm * CosAngle) + math.sqrt(D)) / (2 * (Vp ** 2 - Vm ** 2))
        meeting_position = Point(position_of_mob.x, position_of_mob.y - t * Vm)
        t1 = 0
        if meeting_position.y < left_turn.y:
            t1 = abs(position_of_mob.y - left_turn.y) / Vm  # Время требуемое для того, чтобы дойти до угла
            meet_pos_after_angle, t = core(position_of_tower, left_turn, Vm, Vp, start_position, left_turn, right_turn,
                                        finish_position, t1)
            meeting_position = Point(meet_pos_after_angle.x, meet_pos_after_angle.y)
        return meeting_position, t + t1
    elif position_of_mob.x == right_turn.x:
        Dy = abs(position_of_mob.y - position_of_tower.y)
        Dx = abs(position_of_mob.x - position_of_tower.x)
        hypotenuse = math.sqrt(Dy ** 2 + Dx ** 2)
        if position_of_mob.y < position_of_tower.y:
            CosAngle = Dy / hypotenuse
        else:
            CosAngle = -Dy / hypotenuse

        if t1 == 0:
            # Из теоремы косинусов
            # (t**2) * (Vp**2 - Vm**2) + t * 2 * g * Vm * CosAngle - g**2 = 0
            # D = b**2 - 4 * a * c
            D = (2 * hypotenuse * Vm * CosAngle) ** 2 - 4 * (Vp ** 2 - Vm ** 2) * (- hypotenuse ** 2)
            t = (-(2 * hypotenuse * Vm * CosAngle) + math.sqrt(D)) / (2 * (Vp ** 2 - Vm ** 2))
            meeting_position = Point(position_of_mob.x, position_of_mob.y + t * Vm)
        else:
            # t^2*(Vp^2 - Vm^2) + t*(2*Vm^2*t1 + 2*g*Vm*cos) - g^2 - Vm^2*t1^2 - 2*g*Vm*t1*cos
            D = (2 * Vm**2 * t1 + 2 * hypotenuse * Vm * CosAngle) ** 2 - 4 * (Vp**2 - Vm**2) * (- hypotenuse**2 - Vm**2 * t1**2 - 2 * hypotenuse * Vm * t1 * CosAngle)
            t = (-(2 * Vm**2 * t1 + 2 * hypotenuse * Vm * CosAngle) + math.sqrt(D)) / (2 * (Vp**2 - Vm**2))
            meeting_position = Point(position_of_mob.x, position_of_mob.y + abs(t - t1) * Vm)

        if meeting_position.y > finish_position.y:
            meeting_position.x = finish_position.x
            meeting_position.y = finish_position.y
        return meeting_position, t
