from pygame import*
from  time import sleep
class GameSprite(sprite.Sprite):
    def __init__(self,picture,x,y,w,h):
        super().__init__()
        self.image = transform.scale(image.load(picture),(w, h))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
    def reset(self):
        win.blit(self.image,(self.rect.x,self.rect.y))

class Player(GameSprite):
    #Super(GameSprite)
    def __init__(self,picture,x,y,w,h,speed_x,speed_y ):
        GameSprite.__init__(self, picture, x, y, w, h)   
        self.speed_x = speed_x
        self.speed_y = speed_y
    def update(self):
        if pl.rect.x <= width - 80 and pl.speed_x > 0 or pl.rect.x >= 0 and pl.speed_x < 0:
            self.rect.x  +=self.speed_x
        platforms_touched = sprite.spritecollide(self, barriers, False)
        if self.speed_x > 0 :
            for p in platforms_touched:
                self.rect.right = min(self.rect.right, p.rect.left)
        elif self.speed_x < 0 :
            for p in platforms_touched:
                self.rect.left = max(self.rect.left, p.rect.right)

        if pl.rect.y <= height - 80 and pl.speed_y > 0 or pl.rect.y >= 0 and pl.speed_y < 0:
            self.rect.y  +=self.speed_y
        platforms_touched = sprite.spritecollide(self, barriers, False)
        if self.speed_y > 0 :
            for p in platforms_touched:
                self.rect.bottom = min(self.rect.bottom, p.rect.top)
        elif self.speed_y < 0 :
            for p in platforms_touched:
                self.rect.top = max(self.rect.top, p.rect.bottom)
    def fire_right(self):   
        bullet_right = Bullet('Bullet.png',self.rect.right,self.rect.centery,15,20,15)
        bullets.add(bullet_right)
    def fire_left(self):
        bullet_left = Bullet('Bullet.png',self.rect.left,self.rect.centery,15,20,15)
        bullets.add(bullet_left)
        
class Mexicano(GameSprite):
    diraction = 'left'
    def __init__(self,picture,x,y,w,h,speed_x):    
        GameSprite.__init__(self, picture, x, y, w, h) 
        self.speed = speed_x      
    def update(self): 
        
        if self.rect.x <= height - 80:
            self.diraction = 'right'
        elif self.rect.x >= width-85:
            self.diraction = 'left' 
            
            enemy = Mexicano('Bullet.png',500,200,80,80,6)
        if self.diraction == 'left':
            self.rect.x -= self.speed
        else:
            self.rect.x += self.speed

class Bullet(GameSprite):
    def __init__(self,picture,x,y,w,h,speed_x): 
        GameSprite.__init__(self, picture, x, y, w, h) 
        self.speed = speed_x
    def update(self):
        self.rect.x += self.speed
        if self.rect.x > width+10:
            self.kill()
    




height = 500
width = 700
win = display.set_mode((width, height))
display.set_caption('Лабиринт')
back = (6,29,66)
tine = 2
coin = GameSprite('Coin.png', 480,440,70,70)
pl =  Player('Player.png',20,300,100,100,0,0)
barriers = sprite.Group()
bullets = sprite.Group()
enemys = sprite.Group()
enemy = Mexicano('enemy1.png',500,200,80,80,6)
coin1= GameSprite('Coin.png', 0,0,70,70)
brick = GameSprite('brick.png', 190,120,200,300)
brick2 = GameSprite('brick.png', 190,260,199,300)
barriers.add(brick)
barriers.add(brick2)
enemys.add(enemy)



run = True
finish = False
while run:

    
    time.delay(50)
    for e in event.get():
        
        if e.type == QUIT:
            run = False

        elif e.type == KEYDOWN:
            if e.key == K_w:
                pl.speed_y = -5
            if e.key == K_s:
                pl.speed_y = 5
            if e.key == K_a:
                pl.speed_x = -5
            if e.key == K_SPACE:
                pl.fire_right()
            if e.key == K_LSHIFT:    
                pl.fire_left()
            if e.key == K_d:
                pl.speed_x = 5
                
            if e.key == K_t:
               
                enemy.speed = 0
                
        elif e.type == KEYUP:
            if e.key == K_w:
                pl.speed_y = 0
            if e.key == K_s:
                pl.speed_y = 0
            if e.key == K_a:
                pl.speed_x = 0
            if e.key == K_d:
                pl.speed_x = 0
            if e.key == K_t:        
                enemys.speed = 5
                
    if not finish:
        win.fill(back)
        pl.reset()
        pl.update()
        bullets.update()
        bullets.draw(win)
        enemy.reset()
        coin1.reset()
        coin.reset()
        barriers.draw(win)
        
        sprite.groupcollide(bullets,barriers,True,False)
        sprite.groupcollide(enemys,bullets,True,True)
        enemys.update()
        enemys.draw(win)
        if sprite.collide_rect(pl,coin):
            finish = True
            win.blit(transform.scale(image.load('win.png'),(width,height)),(0,0))
        if sprite.spritecollide(pl,enemys, False):
            finish = True
            win.blit(transform.scale(image.load('lose.jpg'),(width,height)),(0,0))
    
    
    
    
    
    display.update()
