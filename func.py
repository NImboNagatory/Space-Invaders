from tkinter import Frame, Canvas
from turtle import TurtleScreen, RawTurtle
from random import randint


class InvaderScreen(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)
        self.canvas = Canvas(self, highlightthickness=0)
        self.canvas.config(width=800, height=700)
        self.screen = TurtleScreen(self.canvas)
        self.screen.register_shape('data/invader.gif')
        self.screen.bgcolor("black")
        self.canvas.grid(padx=(5, 5), pady=(5, 5))
        self.player_turtle_2 = None
        self.player_turtle_3 = None
        self.player_turtle_1 = None
        self.score_turtle = None
        self.bullet = None
        self.invader_bullet = None
        self.invader_count = 30
        self.invader_bullet_speed = 99
        self.broken = []
        self.score = 0
        self.invaders = []
        self.player_cord = 0
        self.bullet_speed = 50
        self.shooting_enabled = True
        self.invaders_shooting_enabled = True
        self.player_movement_enabled = True
        self.draw_score()
        self.create_player()
        self.bind_mouse(master)
        self.bind_mouse_click(master)
        self.draw_invaders()

    def draw_invaders(self):
        x_loc = -350
        y_loc = 310
        for turtles in range(self.invader_count):
            new_turtle = RawTurtle(self.screen)
            new_turtle.shape("turtle")
            new_turtle.color("white")
            new_turtle.penup()
            new_turtle.speed("fastest")
            new_turtle.setheading(270)
            self.invaders.append(new_turtle)
            if x_loc != 350:
                x_loc += 50
            if self.invaders.index(new_turtle) % 15 == 0:
                x_loc = -350
                y_loc -= 20
            new_turtle.goto(x_loc, y_loc)

    def invasion(self):
        x_loc = -350
        y_loc = 310
        for char in self.invaders:
            char.hideturtle()
            if x_loc != 350:
                x_loc += 50
            if self.invaders.index(char) % 15 == 0:
                x_loc = -350
                y_loc -= 20
            char.goto(x_loc, y_loc)
            char.showturtle()

    def draw_score(self):
        if self.score_turtle is None:
            self.score_turtle = RawTurtle(self.screen, shape="turtle")
            self.score_turtle.hideturtle()
            self.score_turtle.pensize(width=200)
            self.score_turtle.color("white")
            self.score_turtle.speed("fastest")
            self.score_turtle.penup()
        self.score_turtle.goto(270, 310)
        self.score_turtle.write(self.score, font=("Arial", 20, "normal"))

    def create_player(self):
        self.player_turtle_1 = RawTurtle(self.screen, shape="square")
        self.player_turtle_1.shapesize(stretch_wid=2, stretch_len=0.5)
        self.player_turtle_1.color("green")
        self.player_turtle_1.penup()
        self.player_turtle_1.speed("fastest")
        self.player_turtle_1.goto(x=0, y=-335)
        self.player_turtle_1.setheading(90)
        self.player_turtle_2 = RawTurtle(self.screen, shape="square")
        self.player_turtle_2.shapesize(stretch_wid=1, stretch_len=0.5)
        self.player_turtle_2.color("green")
        self.player_turtle_2.penup()
        self.player_turtle_2.speed("fastest")
        self.player_turtle_2.goto(x=0, y=-330)
        self.player_turtle_2.setheading(90)
        self.player_turtle_3 = RawTurtle(self.screen, shape="square")
        self.player_turtle_3.shapesize(stretch_wid=0.2, stretch_len=0.5)
        self.player_turtle_3.color("green")
        self.player_turtle_3.penup()
        self.player_turtle_3.speed("fastest")
        self.player_turtle_3.goto(x=0, y=-325)
        self.player_turtle_3.setheading(90)

    def player_shoot(self, event):
        if self.shooting_enabled:
            self.shooting_enabled = False
            new_bullet = RawTurtle(self.screen, shape="square")
            new_bullet.hideturtle()
            new_bullet.speed("fastest")
            new_bullet.setheading(270)
            new_bullet.penup()
            new_bullet.shapesize(stretch_wid=0.1, stretch_len=0.5)
            new_bullet.color("green")
            new_bullet.goto(x=-(799 / 2 - round(event.x)), y=-320)
            new_bullet.showturtle()
            self.bullet = new_bullet

    def move_bullet(self):
        if self.bullet is not None:
            self.bullet.goto(x=self.bullet.xcor(), y=self.bullet.ycor() + self.bullet_speed)
            if self.bullet.ycor() > 400:
                self.bullet.hideturtle()
                self.bullet = None
                self.shooting_enabled = True

    def move_invader_bullets(self):
        if self.invader_bullet is not None:
            self.invader_bullet.goto(x=self.invader_bullet.xcor(),
                                     y=self.invader_bullet.ycor() - self.invader_bullet_speed)
            if self.invader_bullet.ycor() < -380:
                self.invader_bullet.hideturtle()
                self.invader_bullet = None

    def move_player(self):
        if self.player_movement_enabled:
            self.player_turtle_3.goto(x=self.player_cord, y=-325)
            self.player_turtle_2.goto(x=self.player_cord, y=-330)
            self.player_turtle_1.goto(x=self.player_cord, y=-335)

    def motion(self, event):
        if 780 > round(event.x) > 20:
            self.player_cord = -(799 / 2 - round(event.x))

    def check_bullet_impact(self):
        for char in self.invaders:
            if self.bullet is not None:
                if self.bullet.distance(char) < 18:
                    char.hideturtle()
                    char.goto(-380, 380)
                    self.score += 20
                    self.bullet.hideturtle()
                    self.bullet.goto(char.xcor(), -380)
                    self.bullet = None
                    self.score_turtle.clear()
                    self.draw_score()
                    self.broken.append(self.invaders.index(char))
                    self.shooting_enabled = True
                    if len(self.broken) == self.invader_count:
                        self.shooting_enabled = False
                        self.invasion()
                        self.shooting_enabled = True
                        self.broken = []
            if self.invader_bullet is not None:
                if self.invader_bullet.distance(self.player_turtle_1) < 18:
                    self.invader_bullet.goto(x=self.invader_bullet.xcor() - 500, y=self.invader_bullet.ycor())
                    self.final_screen()

    def final_screen(self):
        self.player_movement_enabled = False
        self.invaders_shooting_enabled = False
        self.shooting_enabled = False

        self.broken = []
        for char in self.invaders:
            char.hideturtle()
        self.score_turtle.clear()
        self.score_turtle.goto(-150, 0)
        self.score_turtle.write(f"Your finishing score {self.score}\n\nwait a bit for next round",
                                font=("Arial", 20, "normal"))
        self.canvas.update()
        self.canvas.after(3000)
        self.canvas.update()
        self.score_turtle.clear()
        self.score = 0
        self.draw_score()
        self.invasion()
        self.player_movement_enabled = True
        self.invaders_shooting_enabled = True
        self.shooting_enabled = True

    def invader_shoot(self):
        if self.invader_bullet is None and self.invaders_shooting_enabled:
            rand_number = randint(0, 29)
            if rand_number not in self.broken:
                invader_bullet = RawTurtle(self.screen, shape="square")
                invader_bullet.hideturtle()
                invader_bullet.speed("fastest")
                invader_bullet.setheading(270)
                invader_bullet.penup()
                invader_bullet.shapesize(stretch_wid=0.1, stretch_len=0.5)
                invader_bullet.color("white")
                invader_bullet.goto(x=self.invaders[rand_number].xcor(), y=250)
                invader_bullet.showturtle()
                self.invader_bullet = invader_bullet

    def bind_mouse(self, gui):
        return gui.bind("<Motion>", self.motion)

    def bind_mouse_click(self, gui):
        return gui.bind("<Button-1>", self.player_shoot)

    def game(self):
        self.invader_shoot()
        self.move_invader_bullets()
        self.move_bullet()
        self.check_bullet_impact()
        self.move_player()
