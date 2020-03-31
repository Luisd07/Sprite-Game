# Imports and initializes Pygame
import pygame
pygame.init()

# Makes a window
win = pygame.display.set_mode((500, 480))
# Caption at the top of the window (The Title)
pygame.display.set_caption("The Beginning")

# variables for the character

walkRight = [pygame.image.load('Characters/R1.png'), pygame.image.load('Characters/R2.png'), pygame.image.load('Characters/R3.png'),
                 pygame.image.load('Characters/R4.png'), pygame.image.load('Characters/R5.png'), pygame.image.load('Characters/R6.png'),
                 pygame.image.load('Characters/R7.png'), pygame.image.load('Characters/R8.png'), pygame.image.load('Characters/R9.png')]
walkLeft = [pygame.image.load('Characters/L1.png'), pygame.image.load('Characters/L2.png'), pygame.image.load('Characters/L3.png'),
                pygame.image.load('Characters/L4.png'), pygame.image.load('Characters/L5.png'), pygame.image.load('Characters/L6.png'),
                pygame.image.load('Characters/L7.png'), pygame.image.load('Characters/L8.png'), pygame.image.load('Characters/L9.png')]
bg = pygame.image.load('Characters/bg.jpg')
char = pygame.image.load('Characters/standing.png')


clock = pygame.time.Clock()

bulletsound = pygame.mixer.Sound('Music/Gun Shot.ogg')
hitsound = pygame.mixer.Sound('Music/Hit.ogg')

music = pygame.mixer.music.load('Music/bg music.mp3')
pygame.mixer.music.play(-1)

score = 0


class player(object):

    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vel = 5
        self.isJump = False
        self.jumpCount = 10
        self.left = False
        self.right = False
        self.walkCount = 0
        self.standing = True
        self.hitBox = (self.x + 17, self.y + 11, 28, 52)
        self.health = 10
        self.visible = True

    def draw(self, win):
        if self.walkCount + 1 >= 27:
            self.walkCount = 0

        if not(self.standing):
            if self.left:
                win.blit(walkLeft[self.walkCount // 3], (self.x, self.y))
                self.walkCount += 1
            elif self.right:
                win.blit(walkRight[self.walkCount // 3], (self.x, self.y))
                self.walkCount += 1
        else:
            if self.right:
                win.blit(walkRight[0], (self.x, self.y))
            else:
                win.blit(walkLeft[0], (self.x, self.y))

        pygame.draw.rect(win, (255, 0, 0), (self.hitBox[0], self.hitBox[1] - 20, 50, 10))
        pygame.draw.rect(win, (0, 128, 0), (self.hitBox[0], self.hitBox[1] - 20, 50 - (5 * (10 - self.health)), 10))
        self.hitBox = (self.x + 17, self.y + 11, 28, 52)

# pygame.draw.rect(win, (255, 0, 0), self.hitbox, 2)

    def hit(self):
        self.isJump = False
        self.jumpCount = 10
        self.x = 60
        self.y = 410
        self.walkCount = 0
        font1 = pygame.font.SysFont('comicsans', 100)
        text = font1.render('-5', 1, (255, 0, 0))
        win.blit(text, (250 - (text.get_width()/2), 200))
        pygame.display.update()
        i = 0
        while i < 200:
            pygame.time.delay(10)
            i += 1
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    i = 201
                    pygame.quit()


class projectile(object):
    def __init__(self, x, y, radius, color, facing):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.facing = facing
        self.vel = 10 * facing

    def draw(self, win):
        pygame.draw.circle(win, self.color, (self.x, self.y), self.radius)


class enemy(object):
    walkRight = [pygame.image.load('Characters/R1E.png'), pygame.image.load('Characters/R2E.png'), pygame.image.load('Characters/R3E.png'),
                 pygame.image.load('Characters/R4E.png'), pygame.image.load('Characters/R5E.png'), pygame.image.load('Characters/R6E.png'),
                 pygame.image.load('Characters/R7E.png'), pygame.image.load('Characters/R8E.png'), pygame.image.load('Characters/R9E.png'),
                 pygame.image.load('Characters/R10E.png'), pygame.image.load('Characters/R11E.png')]
    walkLeft = [pygame.image.load('Characters/L1E.png'), pygame.image.load('Characters/L2E.png'), pygame.image.load('Characters/L3E.png'),
                pygame.image.load('Characters/L4E.png'), pygame.image.load('Characters/L5E.png'), pygame.image.load('Characters/L6E.png'),
                pygame.image.load('Characters/L7E.png'), pygame.image.load('Characters/L8E.png'), pygame.image.load('Characters/L9E.png'),
                pygame.image.load('Characters/L10E.png'), pygame.image.load('Characters/L11E.png')]

    def __init__(self, x, y, width, height, end):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.end = end
        self.path = [self.x, self.end]
        self.walkCount = 0
        self.vel = 3
        self.hitBox = (self.x + 20, self.y, 28, 60)
        self.health = 10
        self.visible = True

    def draw(self, win):
        self.move()
        if self.visible:
            if self.walkCount + 1 >= 33:
                self.walkCount = 0

            if self.vel > 0:
                win.blit(self.walkRight[self.walkCount // 3], (self.x, self.y))
                self.walkCount += 1
            else:
                win.blit(self.walkLeft[self.walkCount // 3], (self.x, self.y))
                self.walkCount += 1
            pygame.draw.rect(win, (255, 0, 0), (self.hitBox[0], self.hitBox[1] - 20, 50, 10))
            pygame.draw.rect(win, (0, 128, 0), (self.hitBox[0], self.hitBox[1] - 20, 50 - (5 * (10 - self.health)), 10))
            self.hitBox = (self.x + 20, self.y, 28, 60)

# pygame.draw.rect(win, (255, 0, 0), self.hitbox, 2)

    def move(self):
        if self.vel > 0:
            if self.x + self.vel < self.path[1]:
                self.x += self.vel
            else:
                self.vel = self.vel * -1
                self.walkCount = 0
        else:
            if self.x - self.vel > self.path[0]:
                self.x += self.vel
            else:
                self.vel = self.vel * -1
                self.walkCount = 0

    def hit(self):
        if self.health > 0:
            self.health -= 1
        else:
            self.visible = False
            print("Hit")


def redrawGameWindow():
    win.blit(bg, (0, 0))
    text = font.render('Score: ' + str(score), 1, (255, 0, 0))
    win.blit(text, (390, 10))
    man.draw(win)
    goblin.draw(win)
    for bullet in bullets:
        bullet.draw(win)

    # refreshes the screen
    pygame.display.update()


# the loop (checks all the events etc.)

font = pygame.font.SysFont('comicsans', 30, True)
man = player(300, 400, 64, 64)
singleShot = 0
goblin = enemy(100, 400, 64, 64, 450)
bullets = []
run = True
while run:
    clock.tick(27)

    if goblin.visible == True:
        if man.hitBox[1] < goblin.hitBox[1] + goblin.hitBox[3] and man.hitBox[1] + man.hitBox[3] > goblin.hitBox[1]:
            if man.hitBox[0] + man.hitBox[2] > goblin.hitBox[0] and man.hitBox[0] < goblin.hitBox[0] + goblin.hitBox[2]:
                man.hit()
                score -= 5

    if singleShot > 0:
        singleShot += 1
    if singleShot > 3:
        singleShot = 0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    for bullet in bullets:
        if goblin.visible == True:
            if bullet.y - bullet.radius < goblin.hitBox[1] + goblin.hitBox[3] and bullet.y + bullet.radius > goblin.hitBox[1]:
                if bullet.x + bullet.radius > goblin.hitBox[0] and bullet.x - bullet.radius < goblin.hitBox[0] + goblin.hitBox[3]:
                    hitsound.play()
                    goblin.hit()
                    score += 1
                    bullets.pop(bullets.index(bullet))

        if bullet.x < 500 and bullet.x > 0:
            bullet.x += bullet.vel
        else:
            bullets.pop(bullets.index(bullet))

    keys = pygame.key.get_pressed()

    if keys[pygame.K_SPACE] and singleShot == 0:
        bulletsound.play()
        if man.left:
            facing = -1
        else:
            facing = 1

        if len(bullets) < 10:
            bullets.append(projectile(round(man.x + man.width // 2), round(man.y + man.height // 2), 6, (0, 0, 0), facing))

        singleShot = 1

    if keys[pygame.K_LEFT] and man.x > man.vel:
        man.x -= man.vel
        man.left = True
        man.right = False
        man.standing = False
    elif keys[pygame.K_RIGHT] and man.x < 500 - man.width - man.vel:
        man.x += man.vel
        man.left = False
        man.right = True
        man.standing = False
    else:
        man.standing = True
        man.walkCount = 0

    if not(man.isJump):
        if keys[pygame.K_UP]:
            man.isJump = True
            man.right = False
            man.left = False
            man.walkCount = 0
    else:
        if man.jumpCount >= -10:
            neg = 1
            if man.jumpCount < 0:
                neg = -1
            man.y -= (man.jumpCount ** 2) * 0.5 * neg
            man.jumpCount -= 1
        else:
            man.isJump = False
            man.jumpCount = 10

    redrawGameWindow()
pygame.quit()
