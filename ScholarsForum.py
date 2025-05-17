from turtle import *

def flower():
    speed(0)
    for i in range(300):
        circle(190-i, 90)
        left(90)
        circle(190-i,90)
        left(30)

flower()
mainloop()