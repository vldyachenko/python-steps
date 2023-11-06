import pyautogui 
from tkinter import *
import time
import random
from threading import Timer

class roketka:
    def __init__(self, canvas, color): 
        self.canvas = canvas
        self.id = canvas.create_rectangle(random.randint(-1,2), random.randint(-1,2), random.randint(80,120), random.randint(6,12), fill=color)
        self.canvas.move(self.id, 200, 300)
        self.x = 0 
        self.canvas_width = self.canvas.winfo_width()
        self.canvas.bind_all('<Left>', self.turn_left)
        self.canvas.bind_all('<Right>', self.turn_right)
        self.canvas.bind_all('<Button-1>', self.click )
#Display paddle
    def draw(self):
        self.canvas.move(self.id, self.x, 0)
        pos = self.canvas.coords(self.id)
        if pos[0] <= 0:
            self.x = 0
        elif pos[2] >= self.canvas_width:
            self.x = 0 
#Movement of the paddle:
    def turn_left(self, evt):
        self.x = -2

    def turn_right(self, evt):
        self.x = 2

    def click(self, evt):
      self.click = True

class ball:
    initial_speed = 2
    speed = initial_speed

    def __init__(self, canvas, Roketka, color):
        self.canvas = canvas
        self.roketka = Roketka
        self.id = canvas.create_oval(random.randint(6,12), random.randint(6,12), random.randint(18,29), random.randint(18,29), fill=color)
        self.canvas.move(self.id, 245, 100)
        starts = [-4, -3, -2, -1, 1, 2, 3, 4]
        random.shuffle(starts)
        self.x = starts[0]
        self.y = -self.speed
        self.canvas_height = self.canvas.winfo_height()
        self.canvas_width = self.canvas.winfo_width()
        self.hit_bottom = False

#Check if ball is hit by the paddle
    def hit_roketka(self, pos):
        roketka_pos = self.canvas.coords(self.roketka.id)
        if pos[2] >= roketka_pos[0] and pos[0] <= roketka_pos[2]:
            if pos[3] >= roketka_pos[1] and pos[3] <= roketka_pos[3]:
                return True
            return False  
#Draw the ball and movement
    def draw(self):
        self.canvas.move(self.id, self.x, self.y)
        pos = self.canvas.coords(self.id)
        if pos[1] <= 0:
            self.y = self.speed
        if pos[3] >= self.canvas_height:
            self.hit_bottom = True
        if self.hit_roketka(pos) == True:
            game_menu.count += 1
            ball.speed += 1
            t = Timer(1.5, self.speed_decrease)
            t.start()
            self.y = -self.speed
        if pos[0] <= 0:
            self.x = self.speed
        if pos[2] >= self.canvas_width:
            self.x = -self.speed

#When the ball is hit, it's speed is increased - it should be lower after some time
    def speed_decrease(self):
        if ball.speed > ball.initial_speed:   
            ball.speed += -1
        return ball.speed

class game_menu:
    
    count = 0
    state = "hidden"

    def __init__(self, canvas):
        self.canvas = canvas
        
    def print_count(self):
        number = self.canvas.create_text(32, 12, text="Score:" + str(self.count), fill="blue", font=('Helvetica 15'))
        self.canvas.itemconfig(number, state = self.state )
        self.canvas.pack()

    def game_over(self):
        self.color = "#%02x%02x%02x" % ( random.randint(0, 255), random.randint(0, 255), random.randint(0, 255) )
        self.canvas.create_text(250, 250, text="Game Over", fill=self.color, font=('Helvetica 20 bold'))
        self.canvas.pack() 


#Random colors generated
ball_color = "#%02x%02x%02x" % ( random.randint(0, 255), random.randint(0, 255), random.randint(0, 255) )
roketka_color = "#%02x%02x%02x" % ( random.randint(0, 255), random.randint(0, 255), random.randint(0, 255) )

#Main screen
tk = Tk()
tk.title("Super_random_game")
tk.resizable(0, 0) # means that the window size should not be changable
tk.wm_attributes("-topmost", 1) #Canvas window should be placed at the top of other windows ("–topmost")
canvas = Canvas(tk, width=500, height=500, bd=0, highlightthickness=0) #bd=0, highlightthickness=0 border config
canvas.pack()
tk.update()

#Creating objects:
Roketka = roketka(canvas,roketka_color )
Ball = ball(canvas, Roketka, ball_color)
Game_menu = game_menu(canvas)

#main loop
while 1:
    if Roketka.click == True:
      if Ball.hit_bottom == False:     
        Ball.draw()
        Roketka.draw()
      elif Ball.hit_bottom == True:
        Game_menu.game_over()
        Game_menu.state = "normal"
        Game_menu.print_count()
    tk.update_idletasks()
    tk.update()
    time.sleep(0.01)

