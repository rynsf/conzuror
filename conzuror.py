import pygame
import random
import select
import sys
import spell
import hanoi
from constant import *
import tutor

class Compy():
    def __init__(self, x, y):
        self.x = x # coordinates on the tile system
        self.y = y
        self.direction = {'N':True, 'S':False, 'E':False, 'W':False} # TODO a better way to store directions?
        
    def canMoveForward(self):
        if self.direction['N']:
            return self.canMoveNorth()
        if self.direction['S']:
            return self.canMoveSouth()
        if self.direction['E']:
            return self.canMoveEast()
        if self.direction['W']:
            return self.canMoveWest()

    def moveForward(self):
        if self.direction['N']:
            if self.canMoveForward():
                self.y -= 1
        if self.direction['S']:
            if self.canMoveForward():
                self.y += 1
        if self.direction['E']:
            if self.canMoveForward():
                self.x += 1
        if self.direction['W']:
            if self.canMoveForward():
                self.x -= 1
        render(SPELL_PER_SECOND)

    def canMoveRight(self):
        if self.direction['N']:
            return self.canMoveEast()
        if self.direction['S']:
            return self.canMoveWest()
        if self.direction['E']:
            return self.canMoveSouth()
        if self.direction['W']:
            return self.canMoveNorth()

    def turnRight(self): 
        if self.direction['N']:
            self.direction['E'] = True
            self.direction['N'] = False
        elif self.direction['S']:
            self.direction['W'] = True
            self.direction['S'] = False
        elif self.direction['E']:
            self.direction['S'] = True
            self.direction['E'] = False
        elif self.direction['W']:
            self.direction['N'] = True
            self.direction['W'] = False

    def canMoveLeft(self):
        if self.direction['N']:
            return self.canMoveWest()
        if self.direction['S']:
            return self.canMoveEast()
        if self.direction['E']:
            return self.canMoveNorth()
        if self.direction['W']:
            return self.canMoveSouth()
    
    def turnLeft(self):
        if self.direction['N']:
            self.direction['W'] = True
            self.direction['N'] = False
        elif self.direction['S']:
            self.direction['E'] = True
            self.direction['S'] = False
        elif self.direction['E']:
            self.direction['N'] = True
            self.direction['E'] = False
        elif self.direction['W']:
            self.direction['S'] = True
            self.direction['W'] = False

    def canMoveNorth(self):
        return not map[self.y-1][self.x].collide # TODO write a collison detections system

    def moveNorth(self):
        if self.canMoveNorth():
            self.y -= 1
        render(SPELL_PER_SECOND)
        
    def canMoveSouth(self):
        return not map[self.y+1][self.x].collide # TODO write a collison detections system

    def moveSouth(self):
        if self.canMoveSouth():
            self.y += 1
        render(SPELL_PER_SECOND)
    
    def canMoveEast(self):
        return not map[self.y][self.x+1].collide # TODO write a collison detections system

    def moveEast(self):
        if self.canMoveEast():
            self.x += 1
        render(SPELL_PER_SECOND)
            
    def canMoveWest(self):
        return not map[self.y][self.x-1].collide # TODO write a collison detections system

    def moveWest(self):
        if self.canMoveWest():
            self.x -= 1
        render(SPELL_PER_SECOND) 
            
    def render(self):
        pygame.draw.rect(screen, 
                         "red", 
                         ((WIDTH/2) - (TILE_SIZE/2), 
                          (HEIGHT/2) - (TILE_SIZE/2),
                          TILE_SIZE, 
                          TILE_SIZE))
        if self.direction["N"]:
            triangle = ((WIDTH/2, HEIGHT/2 - 10), 
                        (WIDTH/2 - 10, HEIGHT/2 + 10), 
                        (WIDTH/2 + 10, HEIGHT/2 + 10))
        if self.direction["S"]:
            triangle = ((WIDTH/2 + 10, HEIGHT/2 - 10), 
                        (WIDTH/2 - 10, HEIGHT/2 - 10), 
                        (WIDTH/2, HEIGHT/2 + 10))
        if self.direction["E"]:
            triangle = ((WIDTH/2 - 10, HEIGHT/2 - 10), 
                        (WIDTH/2 - 10, HEIGHT/2 + 10), 
                        (WIDTH/2 + 10, HEIGHT/2))
        if self.direction["W"]:
            triangle = ((WIDTH/2 - 10, HEIGHT/2), 
                        (WIDTH/2 + 10, HEIGHT/2 - 10), 
                        (WIDTH/2 + 10, HEIGHT/2 + 10))

        pygame.draw.polygon(screen,
                            "white",
                            triangle)

class Tile():
    def __init__(self, collide, color):
        self.collide = collide
        self.color = color

    def render(self, rect):
        pygame.draw.rect(screen, self.color, rect)

def initLevel():
    global map, level, towerOfHanoi
    if level == 0:
        global mazeReached
        compy.x = 1
        compy.y = 1
        map = mazeGen()
        map[len(map)-2][len(map[0])-2] = Tile(False, "blue")
        mazeReached = mazeReachedClosure(len(map)-2, len(map[0])-2)
        spell.global_env["maze-reached?"] = mazeReached
    elif level == 1:
        compy.x = 1
        compy.y = 1
        maxx = 10
        maxy = 10
        map = [[EMPTY_TILE for n in range(maxx)] for m in range(maxy)]
        for n in range(maxy):
            for m in range(maxx):
                if m == 0 or m == len(map[0]) - 1 or n == 0 or n == len(map) - 1: 
                    map[n][m] = WALL_TILE
        towerOfHanoi = hanoi.Hanoi(2, 4, screen, map, render)
        spell.global_env["hanoi"] = towerOfHanoi.move

def mazeGen():
    global map
    map = [[1 if m%2 else n%2 for n in range(1, 100)] for m in range(1, 100)] # TODO remove magic numbers, too many magic numbers in the map TODO find a better way to represent maps
    stack = []
    c = [1, 1]
    stack.insert(-1, c) 
    map[c[0]][c[1]] = 2
    while len(stack) != 0:
        c = stack.pop()
        unvisited_neighbour = []
        if getTile(c[1], c[0]-2) == 0:
            unvisited_neighbour.insert(-1, [c[0]-2, c[1]])
        if getTile(c[1]+2, c[0]) == 0:
            unvisited_neighbour.insert(-1, [c[0], c[1]+2])
        if getTile(c[1], c[0]+2) == 0:
            unvisited_neighbour.insert(-1, [c[0]+2, c[1]])
        if getTile(c[1]-2, c[0]) == 0:
            unvisited_neighbour.insert(-1, [c[0], c[1]-2])
        if len(unvisited_neighbour) != 0:
            stack.insert(-1, c)
            chosen_cell = random.choice(unvisited_neighbour)
            if c[0] == chosen_cell[0]:
                map[c[0]][(c[1]+chosen_cell[1])//2] = 2
            if c[1] == chosen_cell[1]:
                map[(c[0]+chosen_cell[0])//2][c[1]] = 2
            map[chosen_cell[0]][chosen_cell[1]] = 2
            stack.insert(-1, chosen_cell)
    map = [[WALL_TILE if m == 1 else EMPTY_TILE for m in n] for n in map]
    return map

def getTile(x, y): # TODO make map a class of its own
    if (x < 0 or 
        x >= len(map[0]) or 
        y < 0 or 
        y >= len(map)):
        return EMPTY_TILE 

    return map[y][x]
    
def repl():
    global toPrompt
    global numOpenParen
    global prompt
    if toPrompt:
        print("> ", end='', flush=True)
        toPrompt = False 
    if select.select([sys.stdin], [], [], 0) == ([sys.stdin], [], []):
        s = sys.stdin.readline()
        for i in s:
            if i == '(':
                numOpenParen += 1
            if i == ')':
                numOpenParen -= 1
        prompt += s
        if numOpenParen == 0:
            val = spell.evaluate(spell.read(prompt))
            prompt = ""
            toPrompt = True
            if val is not None:
                print(spell.schemestr(val))

def mazeReachedClosure(y, x):
    def reached():
        if compy.y == y and compy.x == x:
            return True
        return False
    return reached

def isWon():
    if level == 0:
        return mazeReached()
    if level == 1:
        return towerOfHanoi.solved()

def render(hz):
    drawHanoi = False
    screen.fill("white")
    for y in range(11):
        for x in range(11):
            tile = getTile(compy.x-5+x, compy.y-5+y)
            if isinstance(tile, Tile):
                tile.render((x*TILE_SIZE - (TILE_SIZE/2), 
                             y*TILE_SIZE - (TILE_SIZE/2),
                             TILE_SIZE,
                             TILE_SIZE))
            elif isinstance(tile, hanoi.Hanoi) and not drawHanoi:
                drawHanoi = True

    if drawHanoi:
        towerOfHanoi.render(compy.x, compy.y)

    compy.render()
    if gameState == ENDGAME:
        surface =  font.render("You Won", True, "black", "white")
        rect = surface.get_rect()
        screen.blit(surface, (WIDTH/2 - rect.w/2, HEIGHT/2 - rect.h/2, rect.w, rect.h))

    pygame.display.flip()
    clock.tick(hz) 

pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
font = pygame.font.Font(None, 128)
pygame.display.set_caption("Conzuror")

map = []
running = True
toPrompt = True
numOpenParen = 0
towerOfHanoi = None
gameState = PLAYING
EMPTY_TILE = Tile(False, "white")
WALL_TILE = Tile(True, "black")
level = 1
prompt = ""
clock = pygame.time.Clock()
compy = Compy(1, 1)

initLevel()

spell.global_env["can-move-north?"] = compy.canMoveNorth
spell.global_env["move-north"] = compy.moveNorth
spell.global_env["can-move-south?"] = compy.canMoveSouth
spell.global_env["move-south"] = compy.moveSouth
spell.global_env["can-move-east?"] = compy.canMoveEast
spell.global_env["move-east"] = compy.moveEast
spell.global_env["can-move-west?"] = compy.canMoveWest
spell.global_env["move-west"] = compy.moveWest
spell.global_env["can-move-right?"] = compy.canMoveRight
spell.global_env["turn-right"] = compy.turnRight
spell.global_env["can-move-left?"] = compy.canMoveLeft
spell.global_env["turn-left"] = compy.turnLeft
spell.global_env["can-move-forward?"] = compy.canMoveForward
spell.global_env["move-forward"] = compy.moveForward
spell.global_env["tutor"] = tutor.help

print()
print("Welcome to Conzuror!")
print("Ready to cast spells and conjure the spirit of the computer!")

while running:
    repl()
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            running = False
        if e.type == pygame.KEYDOWN:
            if e.key == pygame.K_w:
                compy.moveNorth()
            if e.key == pygame.K_s:
                compy.moveSouth()
            if e.key == pygame.K_a:
                compy.moveWest()
            if e.key == pygame.K_d:
                compy.moveEast()
            if e.key == pygame.K_SPACE:
                gameState = PLAYING
                level = (level+1) % 2 # We have two levels cycle them
                initLevel()

    render(FPS)
    if isWon():
        gameState = ENDGAME


pygame.quit()
