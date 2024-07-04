import pygame as pg
import random as rand


###############################
#classes
###############################

# NB
#self.image = pg.transform.scale(self.image,(L,l)) pour changer la taille
#self.image=pg.image.load("nom du fichier/nom de l'image") pour charger une image
#screen = pg.display.set_mode((WIDTH,HEIGHT)) pour créer un écran
#clock = pg.time.Clock() pour avoir un nb min de FPS
#nom du groupe = pg.sprite.Group() pour créer un groupe de sprites
#nom du groupe.add(nom du sprite) pour ajouter un sprite à un groupe
#for event in pg.event.get():              pour détecter un event
        #if event.type == pg.KEYDOWN:      pour détecter une touche préssée
            #if event.key == pg.K_ESCAPE:  pour détecter une touche particulière
#if event.type == pg.KEYUP pour détecter une touche relevée (à part ça, ça fonctionne comme un keydown)
#nom de la police = pg.font.SysFont("nom de la police(sur traitement de texte)",taille de la police) pour définir une police
#nom de l'image = nom de la police.render("texte", True, couleur du texte(système Red, Green, Blue)) pour écrire un texte
#screen.blit(nom de l'image, (x, y)) pour afficher un non-sprite


# if event.type == pg.QUIT:
# pg.quit() pour fermer pygame en cas de bugs

### Vaisseau joueur
class Ship(pg.sprite.Sprite):

	# Constructeur
    def __init__(self ):
        super(Ship,self).__init__()
        # Image et son rectangle
        self.image=pg.image.load("sprite/s_ship1.png")
        self.image = pg.transform.scale(self.image,(80,80))
        self.rect=self.image.get_rect()

        # On place le vaisseau au bon endroit
        self.rect.center =(WIDTH/2,HEIGHT-self.rect.h/2)

        # La "vraie" position du vaiseeau, peut être décimale
        self.x = self.rect.centerx
        self.y = self.rect.centery

        # Booléens - qu'est-ce que le vaisseau est en train de faire ?
        self.moveLeft = False
        self.moveRight = False
        self.shoot = False

        # Moteur
        self.speed = 6

        # Canon
        self.reload = 37 # Temps pour recharger
        self.time = 0 # Temps depuis le dernier tir

        self.ammo = "N"

    # Déplacement
    def move(self,dist):
        # On change d'abord la "vraie" position..
        self.x = self.x + dist

        # Et on met le rectangle à cet endroit (ou à peu près, à l'entier près)
        self.rect.center = (self.x, self.y)

	# Le vaisseau réagit aux commandes
    def update(self):
        self.time += 1
        if self.moveLeft:
            if self.rect.left >0:
                self.move(-self.speed)
        if self.moveRight:
            if self.rect.right<WIDTH:
                self.move(self.speed)
        if self.shoot :
            if self.time > self.reload :
                if self.ammo == "N":
                    shoot = Bullet (self.x, self.y - self.rect.h/2)

                else:
                    shoot = Bomb_bullet (self.x, self.y - self.rect.h/2)

                all_S_bullet.add(shoot)
                all_B_bullet.add(shoot)
                all_sprite.add(shoot)
                self.time = 0

### aliens
class Alien(pg.sprite.Sprite):

	# Constructeur
    def __init__(self):
        super(Alien,self).__init__()
        # Image et son rectangle
        self.image=pg.image.load("sprite/aliensprite3.png")
        self.image = pg.transform.scale(self.image,(50,80))
        self.rect=self.image.get_rect()

        # On place l'alien au bon endroit
        self.rect.center =(self.rect.w/2,self.rect.h/2 + MARGE)

        # La "vraie" position de l'alien, peut être décimale
        self.x = self.rect.centerx
        self.y = self.rect.centery

        # Booléens - qu'est-ce que l'alien est en train de faire ?
        self.moveLeft = False
        self.moveRight = True
        self.moveDown = False

        # Moteur
        self.speed = 4
        self.descente = self.rect.h

        #valeur
        self.value = 1
    # Déplacement
    def moveS(self,dist):
        self.x = self.x + dist
        self.rect.center = (self.x, self.y)

    def moveD(self, dist) :
        self.y = self.y + dist
        self.rect.center = (self.x, self.y)

	# L'alien se déplace
    def update(self):

        #changements de direction
        self.moveDown = False
        if self.rect.left < 0:
            self.moveRight = True
            self.moveLeft = False
            self.moveDown = True
        if self.rect.right > WIDTH:
            self.moveRight = False
            self.moveLeft = True
            self.moveDown = True

       #vrai déplacement
        if self.moveDown:
            self.moveD(self.descente)
        if self.moveLeft:
            self.moveS(-self.speed)
        if self.moveRight:
            self.moveS(self.speed)

class Alien2(Alien):
    def __init__(self):

        super(Alien2, self).__init__()
        # Image et son rectangle
        self.image=pg.image.load("sprite/aliensprite2.png")
        self.image = pg.transform.scale(self.image,(50,80))
        #reload
        self.reload = 0
        self.value = 3

    def update(self) :
        super(Alien2, self).update()
        self.reload = self.reload + 1
        if self.reload == 50 :
            shoot = Alien_bullet(self.x, self.y + self.rect.h)
            all_A_bullet.add(shoot)
            all_sprite.add(shoot)
            self.reload = 0

class A_ship(Alien) :
    def __init__(self):
        super(A_ship, self).__init__()
        self.image=pg.image.load("sprite/aliensprite1.png")
        self.image = pg.transform.scale(self.image,(50,50))
        self.rect.center =(self.rect.w/2,self.rect.h/2)
        self.speed = 10
        self.value = 10
        self.x = self.rect.centerx
        self.y = self.rect.centery


    def update(self):
        self.moveS(self.speed)

        if self.rect.right == WIDTH:
            self.kill()
#tirs
class Bullet(pg.sprite.Sprite) :
    def __init__(self, x_start, y_start) :
        super(Bullet,self).__init__()
        self.image = pg.image.load("sprite/laserBlue01.png")
        self.rect=self.image.get_rect()
        self.rect.center = (x_start,y_start)
        self.x = self.rect.centerx
        self.y = self.rect.centery
        self.speed = 8

    def update(self):
       self.y = self.y - self.speed
       self.rect.center = (self.x, self.y)

       # Détruire les tirs qui sortent de l'écran
       if self.y < 0 or self.y > HEIGHT:
           self.kill()

class Alien_bullet(Bullet) :
    def __init__(self, x_start, y_start):
        super(Alien_bullet,self).__init__(x_start, y_start)
        self.image = pg.image.load("sprite/laserRed01.png")
        self.image = pg.transform.rotate(self.image, 180)
        self.speed = -self.speed

class Bomb_bullet(Bullet) :
    def __init__(self, x_start, y_start):
        super(Bomb_bullet, self).__init__(x_start, y_start)
        self.image = pg.image.load("sprite/bomb.png")
        self.rect=self.image.get_rect()
        self.rect.center = (x_start,y_start)
        self.x = self.rect.centerx
        self.y = self.rect.centery
        self.timer = 0
        self.apt = False


    def update(self):
        super(Bomb_bullet, self).update()
        if self.apt :
            timer_nice = str(self.timer).rjust(2, "0")
            self.image = pg.image.load("sprite/explo/expl_01_00"+timer_nice+".png")
            self.image = pg.transform.scale(self.image,(round(6.5*self.timer),round(6.5*self.timer)))
            self.rect=self.image.get_rect()
            self.rect.centerx = self.x
            self.rect.centery = self.y
            self.timer+=1
            if self.timer == 23:
                self.kill()

class Bonus(pg.sprite.Sprite) :
    def __init__(self) :
        super(Bonus, self).__init__()
        self.image = pg.image.load("sprite/powerupBlue_bolt.png")
        self.rect=self.image.get_rect()
        self.rect.center = (rand.randint(0 + player.rect.w, WIDTH - player.rect.w),rand.randint(HEIGHT/2 + player.rect.h,HEIGHT - player.rect.h))
        self.x = self.rect.centerx
        self.y = self.rect.centery

class Bomb_up(Bonus):
    def __init__(self):
        super(Bomb_up, self).__init__()
        self.image = pg.image.load("sprite/powerupRed_bolt.png")


###############################
# programme principal
###############################

### Definitions et initialisation


# Constantes
FPS = 60
WIDTH=800 #width max = 1550
HEIGHT=600  #height max = 800
INTERVAL = 50
INTERVALA = 2 * FPS
INTERVALB = 200
INTERVAL2 =10
TIME = 0
TIMEB = 0
TIMEA = 0
TIME2 = 0
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0,255,0)
BLUE = (0, 0, 255)

MARGE = 80
VICT = 100

play = False

# Début du jeu ...
pg.init()
screen = pg.display.set_mode((WIDTH,HEIGHT))
clock = pg.time.Clock()
Bg = pg.image.load("sprite/star-background.png").convert()
po_score = pg.font.SysFont("arial",12)
po_rule = pg.font.SysFont("arial",20)
po_END = pg.font.SysFont("algerian",102)

while not play:
    screen.blit( Bg, (0, 0))
    img_rule0 = po_rule.render("Gauche et droite pour se déplacer, espace pour tirer", True, WHITE)
    screen.blit(img_rule0, (200, 50))
    img_rule1 = po_rule.render("Obtenez 100 points sans vous faire toucher pour gangner", True, WHITE)
    screen.blit(img_rule1, (200, 100))
    img_rule2 = po_rule.render("Le bonus bleu accélère la cadence de tir", True, WHITE)
    screen.blit(img_rule2, (200, 150))
    img_rule3 = po_rule.render("Le bonus rouge réinitiallise le score et débloque les bombes", True, WHITE)
    screen.blit(img_rule3, (200, 200))
    img_rule4 = po_rule.render("De plus, il fait passer l'objectif à 500 points", True, WHITE)
    screen.blit(img_rule4, (200, 250))
    img_rule5 = po_rule.render("Appuyez sur Entrée pour continuer", True, WHITE)
    screen.blit(img_rule5, (200, 300))
    pg.display.flip()


    for event in pg.event.get():
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_RETURN:
                play = True

# On initialise les variables
perdu = False
end = False
score = 0
proba = 5
bonus_power = 2.1

# Et on crée les premiers sprites, ainsi que les groupes pour les ranger
player=Ship()
dad=Alien2()

all_Bonus = pg.sprite.Group()
all_powerup = pg.sprite.Group()

all_alien=pg.sprite.Group()
all_alien.add(dad)

all_S_bullet = pg.sprite.Group()

all_A_bullet = pg.sprite.Group()

all_B_bullet = pg.sprite.Group()

all_player = pg.sprite.Group()
all_player.add(player)

all_sprite=pg.sprite.Group()
all_sprite.add(player)
all_sprite.add(dad)

### Boucle principale

while not perdu:

	# Traitement des évènements
    for event in pg.event.get():
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                perdu = True
            if event.key == pg.K_LEFT:
                player.moveLeft = True
            if event.key == pg.K_RIGHT:
                player.moveRight = True
            if event.key == pg.K_SPACE:
                player.shoot = True
        if event.type == pg.KEYUP:
            if event.key == pg.K_LEFT:
                player.moveLeft = False
            if event.key == pg.K_RIGHT:
                player.moveRight = False
            if event.key == pg.K_SPACE:
                player.shoot = False

    # Fonctionnement du jeu
    # détection de collision

    if player.ammo == "N":
        for hit in pg.sprite.groupcollide(all_alien, all_S_bullet, True, True):
           score = score + hit.value

    else:
        toto = pg.sprite.groupcollide(all_alien, all_B_bullet, True, False)
        for hit in toto:
            bomb = toto[hit][0]
            score = score + hit.value
            bomb.apt = True



    for hit in pg.sprite.groupcollide(all_player, all_A_bullet, True, True):
        perdu = True

    #bonus
    for cling in pg.sprite.groupcollide(all_Bonus, all_S_bullet, True, True):
        score = score + 5
        player.reload = player.reload -bonus_power

    for ding in pg.sprite.groupcollide(all_powerup, all_S_bullet, True, True):
        score=0
        VICT = 500
        proba = 70
        bonus_power = 0
        player.reload = 32
        player.ammo = "S"

    #apparition de nouveaux monstres
    TIME = TIME + 1
    if TIME == INTERVAL :
        if TIME2 == INTERVAL2:
            new_mob = Alien2()
            all_alien.add(new_mob)
            all_sprite.add(new_mob)
            TIME = 0
            TIME2 = 0
        else:
            new_mob = Alien()
            all_alien.add(new_mob)
            all_sprite.add(new_mob)
            TIME = 0
            TIME2 = TIME2 + 1
        # trouver la vitesse du dernier alien : [-1] pour le dernier elmt de la liste
        vitesse = all_alien.sprites()[-1].speed
        #spawn d'alien tt les 150 à 200 pixels
        mini = round(100/vitesse)
        maxi = round (150/vitesse)

        INTERVAL = rand.randint(mini,maxi)
    TIMEA = TIMEA + 1
    if INTERVALA == TIMEA:
        new_mob = A_ship()
        all_alien.add(new_mob)
        all_sprite.add(new_mob)
        TIMEA = 0

    #apparition de bonus
    TIMEB = TIMEB + 1
    if TIMEB == INTERVALB :
        luck = rand.randint(1, 100)
        if luck >= proba:
            new_powerup = Bomb_up()
            all_powerup.add(new_powerup)
            all_sprite.add(new_powerup)

        else:
            new_bonus = Bonus()
            all_Bonus.add(new_bonus)
            all_sprite.add(new_bonus)

        TIMEB = 0


    #test victoire des monstres
    for monstre in all_alien :
         if monstre.rect.bottom > HEIGHT-player.rect.h :
             perdu = True
    if score > VICT:
        perdu = True
    # tour de jeu
    all_sprite.update()

	# Dessin
    screen.blit( Bg, (0, 0))
    all_sprite.draw(screen)
    img_score = po_score.render("score: "+str(score), True, WHITE)
    screen.blit(img_score, (20, 10))
    img_goal = po_score.render("Goal: "+str(VICT), True, WHITE)
    screen.blit(img_goal, (20, 25))
    pg.display.flip()

    # Le temps passe...
    clock.tick(FPS)

#game over
while not end:

	# Traitement des évènements
    for event in pg.event.get():
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_SPACE:
                end = True

    if score > VICT:
        img_VICT = po_END.render("VICTORY", True, GREEN)
        screen.blit(img_VICT, (WIDTH/2-img_VICT.get_rect().w/2, HEIGHT/2-img_VICT.get_rect().h/2))
        pg.display.flip()

    else :
        img_GO = po_END.render("GAME OVER", True, RED)
        screen.blit(img_GO, (WIDTH/2-img_GO.get_rect().w/2, HEIGHT/2-img_GO.get_rect().h/2))
        pg.display.flip()

### C'est fini !
pg.quit()
