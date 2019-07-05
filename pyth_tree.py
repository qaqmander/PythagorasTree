#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import turtle
from math import atan, pi, sqrt
from functools import reduce

class coroutine():    # to wrap generator with `isalive` and `result`
    def __init__(self, _routine):
        self._routine = _routine
        self._isalive = True
        self._result = None
    def send(self, _obj):
        try:
            self._result = self._routine.send(_obj)
        except StopIteration:
            self._isalive = False
    def isalive(self):
        return self._isalive
    def get_result(self):
        return self._result

class scheduler():
    def __init__(self, _routine_ls):
        self._routine_ls = _routine_ls
        self.result = None
    def run(self):
        for routine in self._routine_ls:
            routine.send(None)
        flag = True
        while flag:
            flag = False
            for i in range(len(self._routine_ls)):
                routine = self._routine_ls[i]
                if routine.isalive():
                    routine.send(None)
                    if routine.isalive():    # maybe this is harmful for efficience
                        flag = True
        self.result = []
        for routine in self._routine_ls:
            self.result.append(routine.get_result())

    def get_result(self):
        return self.result

def div(a, b):
    k = int(a) // b
    return k, a - k * b
# parameterize the step, which makes it easier to adjust speed
step_l = 3
step_a = 13

def coroutine_square(pen, a, fillcolor):
    yield None
    pen.speed(0)
    pen.fillcolor(fillcolor)
    pen.pencolor(pen.fillcolor())
    pen.begin_fill()
    q, r = div(90, step_a)
    for t in range(q):
        yield None
        pen.left(step_a)
    pen.left(r)
    q, r = div(a, step_l)
    for t in range(q):
        yield None
        pen.forward(step_l)
    pen.forward(r)
    ret = pen.clone()
    ret._fillpath = ret._fillitem = None
    if fillcolor == end_color:
        ret.ht()
    for i in range(2):
        q, r = div(90, step_a)
        for t in range(q):
            yield None
            pen.right(step_a)
        pen.right(r)

        q, r = div(a, step_l)
        for t in range(q):
            yield None
            pen.forward(step_l)
        pen.forward(r)
    pen.end_fill()
    pen.ht()
    yield [(ret, a)]

def coroutine_triangle(pen, a, pencolor):
    yield None
    pen.speed(0)
    pen.pencolor(pencolor)
    pen.fillcolor(pen.pencolor())
    q, r = div(r_angle, step_a)
    for t in range(q):
        yield None
        pen.right(step_a)
    pen.right(r)
    ret1 = pen.clone()
    ret1._fillpath = ret1._fillitem = None
    q, r = div(a * l_k, step_l)
    for t in range(q):
        yield None
        pen.forward(step_l)
    pen.forward(r)
    q, r = div(90, step_a)
    for t in range(q):
        yield None
        pen.right(step_a)
    pen.right(r)
    ret2 = pen.clone()
    ret2._fillpath = ret2._fillitem = None
    q, r = div(a * r_k, step_l)
    for t in range(q):
        yield None
        pen.forward(step_l)
    pen.forward(r)
    pen.ht()
    yield [(ret1, a * l_k), (ret2, a * r_k)]

if __name__ == '__main__':
    normal_color = 'brown'
    end_color = 'green'
    start_pos = (10, -230)
    all_size = 100
    l, r, n = 3, 4, 4
    r_angle = atan(l / r) * 180 / pi
    l_k = l / sqrt(l ** 2 + r ** 2)
    r_k = r / sqrt(l ** 2 + r ** 2)
    
    turtle.bgcolor('white')
    
    ini_pen = turtle.Pen()
    ini_pen.fillcolor(normal_color)
    ini_pen.pencolor(normal_color)
    ini_pen.up()
    ini_pen.setpos(start_pos)
    ini_pen.down()
    ini_pen.setheading(180)
    ini_pen.forward(all_size) # first line
    ini_pen.setheading(0) # heading east

    coroutine_ls = [coroutine(
        coroutine_square(ini_pen, all_size, normal_color))
    ]
    scher = scheduler(coroutine_ls)
    scher.run()
    pen_list = reduce(lambda x, y: x + y, scher.get_result(), [])

    for i in range(n):    # main loop
        for func in (coroutine_triangle, coroutine_square):
            color = normal_color if i < n - 1 else end_color
            coroutine_ls = []
            for pen, a in pen_list:
                coroutine_ls.append(
                    coroutine(func(pen, a, color))
                )
            scher = scheduler(coroutine_ls)
            scher.run()
            pen_list = reduce(    # to get pens in next turn
                lambda x, y: x + y,
                scher.get_result(),
                []
            )

    turtle.mainloop()
