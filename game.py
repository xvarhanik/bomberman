import tkinter as tk

class Game(tk.Tk):
    def __init__(self):
        super().__init__()
        self.bg=tk.PhotoImage(file="sprites/BackgroundTile.png")
        self.canvas=tk.Canvas(width=self.bg.width(),height=self.bg.height())
        self.canvas.pack()
        self.canvas.create_image(self.bg.width()/2,self.bg.height()/2,image=self.bg)
        self.player1=Player(self.canvas,75,75,"bomberman")
        self.player2=Player(self.canvas,675,675,"creep")
        self.solid=[]
        self.explodable=[]
        self.fire=[]
        self.bombs=[]
        self.game_over=False
        #key binding
        self.canvas.bind_all("<KeyPress-Right>",self.player1.keypress_right)
        self.canvas.bind_all("<KeyRelease-Right>",self.player1.keyrelease_right)
        self.canvas.bind_all("<KeyPress-Left>",self.player1.keypress_left)
        self.canvas.bind_all("<KeyRelease-Left>",self.player1.keyrelease_left)
        self.canvas.bind_all("<KeyPress-Up>",self.player1.keypress_up)
        self.canvas.bind_all("<KeyRelease-Up>",self.player1.keyrelease_up)
        self.canvas.bind_all("<KeyPress-Down>",self.player1.keypress_down)
        self.canvas.bind_all("<KeyRelease-Down>",self.player1.keyrelease_down)

        self.canvas.bind_all("<KeyPress-d>",self.player2.keypress_right)
        self.canvas.bind_all("<KeyRelease-d>",self.player2.keyrelease_right)
        self.canvas.bind_all("<KeyPress-a>",self.player2.keypress_left)
        self.canvas.bind_all("<KeyRelease-a>",self.player2.keyrelease_left)
        self.canvas.bind_all("<KeyPress-w>",self.player2.keypress_up)
        self.canvas.bind_all("<KeyRelease-w>",self.player2.keyrelease_up)
        self.canvas.bind_all("<KeyPress-s>",self.player2.keypress_down)
        self.canvas.bind_all("<KeyRelease-s>",self.player2.keyrelease_down)

        self.canvas.bind_all("<KeyRelease-p>",self.player1.keypress_bomb)
        self.canvas.bind_all("<KeyRelease-b>",self.player2.keypress_bomb)
        #vytvaranie mapy
        
        #solid bloky
        for i in range(15):
            self.solid.append(Solid(self.canvas,25+i*50,25))
            self.solid.append(Solid(self.canvas,25+i*50,725))

        for i in range(13):
            self.solid.append(Solid(self.canvas,25,75+50*i))
            self.solid.append(Solid(self.canvas,725,75+50*i))

        for i in range(3,14):
            if i%2==1:
                for j in range(3,14):
                    if j%2==1:
                        self.solid.append(Solid(self.canvas,25+(i-1)*50,25+(j-1)*50))

        #bloky co sa daju znicit
        for i in range(3,14):
            if i%2==0:
                for j in range(3,14):
                    self.explodable.append(Explodable(self.canvas,25+(i-1)*50,25+(j-1)*50))
            else:
                for j in range(3,14):
                    if j%2==0:
                        self.explodable.append(Explodable(self.canvas,25+(i-1)*50,25+(j-1)*50))   
            
        for i in range(9):
            self.explodable.append(Explodable(self.canvas,225+i*50,75))   
            self.explodable.append(Explodable(self.canvas,525-50*i,675))
            self.explodable.append(Explodable(self.canvas,675,525-50*i))
            self.explodable.append(Explodable(self.canvas,75,225+i*50))   
        self.explodable.append(Explodable(self.canvas,675,75))
        self.explodable.append(Explodable(self.canvas,75,675))
        
    def explosion(self,x,y):
        
        X=[x,x+50,x-50,x,x]
        Y=[y,y,y,y+50,y-50]

        in_solid=False
        for wall1,wall2 in zip(self.explodable,self.solid):
            if wall1.x==x+50 and wall1.y==y and not wall1.destroyed:
                in_solid=True
                break
            if wall2.x==x+50 and wall2.y==y :
                in_solid=True  
                break 
        if not in_solid:
            X.append(x+100)
            Y.append(y)
        
        in_solid=False
        for wall1,wall2 in zip(self.explodable,self.solid):
            if wall1.x==x-50 and wall1.y==y and not wall1.destroyed:
                in_solid=True
                break
            if wall2.x==x-50 and wall2.y==y :
                in_solid=True  
                break 
        if not in_solid:
            X.append(x-100)
            Y.append(y)

        in_solid=False
        for wall1,wall2 in zip(self.explodable,self.solid):
            if wall1.x==x and wall1.y==y+50. and not wall1.destroyed:
                in_solid=True
                break
            if wall2.x==x and wall2.y==y+50 :
                in_solid=True  
                break 
        if not in_solid:
            X.append(x)
            Y.append(y+100)

        in_solid=False
        for wall1,wall2 in zip(self.explodable,self.solid):
            if wall1.x==x and wall1.y==y-50 and not wall1.destroyed:
                in_solid=True
                break
            if wall2.x==x and wall2.y==y-50 :
                in_solid=True  
                break 
        if not in_solid:
            X.append(x)
            Y.append(y-100)

        for i in range(len(X)):
            in_solid=False
            for wall in self.solid:
                if wall.x==X[i] and wall.y==Y[i]:
                    in_solid=True
            if not in_solid:
                self.fire.append(Fire(self.canvas,X[i],Y[i]))
                for wall in self.explodable:
                    if wall.x==X[i] and wall.y==Y[i]:
                        wall.destroy()
            

    def player_on_fire(self):
        for fire in self.fire:
            if not fire.destroyed:
                if fire.x-25 <= self.player1.x <= fire.x+25 and fire.y-25 <= self.player1.y <=fire.y+25:
                    return "Vyhral hrac 2"
                if fire.x-25 <= self.player2.x <= fire.x+25 and fire.y-25 <= self.player2.y <=fire.y+25:
                    return "Vyhral hrac 1"
        return False


    #hlavna slucka celej hry!
    def timer(self):
        if not self.game_over:    
            bomb1=self.player1.sprite_loop(self.solid,self.explodable)
            bomb2=self.player2.sprite_loop(self.solid,self.explodable)

            already_planted=False
            if not bomb1==None:
                for bomb in self.bombs:
                    if not bomb.destroyed and bomb==bomb1:
                        already_planted=True
                if not already_planted:
                    self.bombs.append(bomb1)
                else:
                    bomb1.destroy()

            already_planted=False
            if not bomb2==None:
                for bomb in self.bombs:
                    if not bomb.destroyed and bomb==bomb2:
                        already_planted=True
                if not already_planted:
                    self.bombs.append(bomb2)
                else:
                    bomb2.destroy()

            for bomb in self.bombs:
                if not bomb.destroyed:
                    x,y=bomb.sprite_loop()
                    if x>0 and y>0:
                        self.explosion(bomb.x,bomb.y)

            for fire in self.fire:
                if not fire.destroyed:
                    fire.sprite_loop()
                    self.game_over=self.player_on_fire()    
            self.canvas.after(40,self.timer)

        else:
            self.canvas.create_text(350,350,text=self.game_over,fill="red",font=("Helvetica", "32") )

class BaseSprite:
    def __init__(self, canvas, x, y):
        self.canvas=canvas
        self.x, self.y = x, y
        self.id = self.canvas.create_image(x,y)
        self.destroyed = False

    def load_sprite(self,file_path,quantity):
        sprites=[]
        for i in range(quantity):
            sprites.append(tk.PhotoImage(file=file_path.format(i)))
        return sprites

    def sprite_loop(self):
        pass

    def destroy(self):
        self.destroyed=True
        self.canvas.delete(self.id)


class Player(BaseSprite):   
        def __init__(self,canvas,x,y,model):
            super().__init__(canvas,x,y)
            self.sprite_sheet = self.load_all_sprites(model)
            self.movement = "idle"
            self.direction = "front"
            self.sprite_index = 0
            self.dx=self.dy=0
            self.key_pressed=0
            self.bomb=None

        def load_all_sprites(self,model):
            sprite_sheet={
                "idle": {"left":[],"right":[],"front":[],"back":[]},
                "move": {"left":[],"right":[],"front":[],"back":[]}
                }       
            if model=="bomberman":
                sprite_sheet["idle"]["left"]=self.load_sprite("sprites/Bomberman/Left/{}.png",1)
                sprite_sheet["idle"]["right"]=self.load_sprite("sprites/Bomberman/Right/{}.png",1)
                sprite_sheet["idle"]["front"]=self.load_sprite("sprites/Bomberman/Front/{}.png",1)
                sprite_sheet["idle"]["back"]=self.load_sprite("sprites/Bomberman/Back/{}.png",1)

                sprite_sheet["move"]["left"]=self.load_sprite("sprites/Bomberman/Left/{}.png",8)
                sprite_sheet["move"]["right"]=self.load_sprite("sprites/Bomberman/Right/{}.png",8)
                sprite_sheet["move"]["front"]=self.load_sprite("sprites/Bomberman/Front/{}.png",8)
                sprite_sheet["move"]["back"]=self.load_sprite("sprites/Bomberman/Back/{}.png",8)

            elif model=="creep":
                sprite_sheet["idle"]["left"]=self.load_sprite("sprites/Creep/Left/{}.png",1)
                sprite_sheet["idle"]["right"]=self.load_sprite("sprites/Creep/Right/{}.png",1)
                sprite_sheet["idle"]["front"]=self.load_sprite("sprites/Creep/Front/{}.png",1)
                sprite_sheet["idle"]["back"]=self.load_sprite("sprites/Creep/Back/{}.png",1)

                sprite_sheet["move"]["left"]=self.load_sprite("sprites/Creep/Left/{}.png",7)
                sprite_sheet["move"]["right"]=self.load_sprite("sprites/Creep/Right/{}.png",7)
                sprite_sheet["move"]["front"]=self.load_sprite("sprites/Creep/Front/{}.png",6)
                sprite_sheet["move"]["back"]=self.load_sprite("sprites/Creep/Back/{}.png",6)

            return sprite_sheet
        # hracov hlavny loop
        def sprite_loop(self,solid,explodable):
            self.sprite_index=self.next_animation_index(self.sprite_index)
            img=self.sprite_sheet[self.movement][self.direction][self.sprite_index]
            self.canvas.itemconfig(self.id,image=img)
            #kontrola kolizie so stenou a pohyb
            colision=False
            for wall in explodable:
                if not wall.destroyed:
                    if self.wall_colision(wall.x,wall.y,self.x+self.dx*5,self.y+self.dy*5): 
                        colision=True
            for wall in solid:
                if not wall.destroyed:
                    if self.wall_colision(wall.x,wall.y,self.x+self.dx*5,self.y+self.dy*5):
                        colision=True

            if self.movement == "move" and not colision:
                self.move()
            bomb=self.bomb
            self.bomb=None
            return bomb

        def move(self):
            self.x+=self.dx
            self.y+=self.dy
            self.canvas.coords(self.id,self.x,self.y)

        def next_animation_index(self,idx):
            idx+=1
            max = len(self.sprite_sheet[self.movement][self.direction])
            idx = idx % max
            return idx

        def wall_colision(self,x1,y1,x2,y2):
            if x1-25<= x2 <=x1+25 and y1-25 <= y2 <=y1+25:
                return True
            return False
            

        #keypress funkcie
        def keypress_right(self,event):
            if self.key_pressed==0:
                self.movement = "move"
                self.direction = "right"
                self.key_pressed+=1
                self.dx = 5
        def keyrelease_right(self,event):
            if self.direction=="right":
                self.dx = 0
                self.movement = "idle"
                self.key_pressed-=1

        def keypress_left(self,event):
            if self.key_pressed==0:
                self.movement = "move"
                self.direction = "left" 
                self.key_pressed+=1            
                self.dx = -5
        def keyrelease_left(self,event):     
            if self.direction=="left":
                self.dx = 0
                self.movement = "idle"
                self.key_pressed-=1

        def keypress_up(self,event):
            if self.key_pressed==0:
                self.movement = "move"
                self.direction = "back"
                self.key_pressed+=1
                self.dy = -5
        def keyrelease_up(self,event):
             if self.direction=="back":
                self.dy = 0
                self.movement = "idle"
                self.key_pressed-=1

        def keypress_down(self,event):
            if self.key_pressed==0:
                self.movement = "move"
                self.direction = "front"
                self.key_pressed+=1
                self.dy = 5

        def keyrelease_down(self,event):
            if self.direction=="front":
                self.dy = 0
                self.movement = "idle"
                self.key_pressed-=1
        
        def keypress_bomb(self,event):
            self.bomb=Bomb(self.canvas,self.x,self.y)

class Explodable(BaseSprite):
    def __init__(self,canvas,x,y):
        super().__init__(canvas,x,y)
        self.img = self.load_sprite("sprites\Blocks\Explodable\{}.png",1)
        self.canvas.itemconfig(self.id,image=self.img)

class Solid(BaseSprite):
    def __init__(self,canvas,x,y):
        super().__init__(canvas,x,y)
        self.img = self.load_sprite("sprites\Blocks\Solid\{}.png",1)
        self.canvas.itemconfig(self.id,image=self.img)

class Bomb(BaseSprite):
    def __init__(self,canvas,x,y):
        x,y=self.find_bomb_coords(x,y)
        super().__init__(canvas,x,y)
        self.sprite_sheet=self.load_sprite("sprites\Bomb\{}.png",3)
        self.tick=0
        self.sprite_index = 0
        flames=[]
    
    def __eq__(self,other):
        if other==None:
            return False
        if self.x==other.x and self.y==other.y:
            return True
        return False

    def find_bomb_coords(self,x,y):
        lst=[75,125,175,225,275,325,375,425,475,525,575,625,675,725]
        return lst[min(range(len(lst)), key = lambda i: abs(lst[i]-x))],lst[min(range(len(lst)), key = lambda i: abs(lst[i]-y))]
    
    def sprite_loop(self):
        if self.tick<3:
            self.sprite_index=self.next_animation_index()
            img=self.sprite_sheet[self.sprite_index]
            self.canvas.itemconfig(self.id,image=img)
            self.tick+=0.05
        else:
            self.destroy()
            return self.x, self.y
        return -1,-1

    def next_animation_index(self):
        if self.tick<1:
            return 0
        if self.tick<2:
            return 1
        return 2


class Fire(BaseSprite):
    def __init__(self,canvas,x,y):
        super().__init__(canvas,x,y)
        self.sprite_sheet=self.load_sprite("sprites\Flame\{}.png",5)     
        self.sprite_index=0
        self.tick=0

    def next_animation_index(self,idx):
        idx+=1
        max = len(self.sprite_sheet)
        idx = idx % max
        return idx

    def sprite_loop(self):
        if self.tick<1.5:
            self.tick+=0.05
            self.sprite_index=self.next_animation_index(self.sprite_index)
            img=self.sprite_sheet[self.sprite_index]
            self.canvas.itemconfig(self.id,image=img)
        else:
            self.destroy()
        
          


#main loop
game=Game()
game.timer()
game.mainloop()