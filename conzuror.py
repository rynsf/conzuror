import pygame
import random
import select
import sys
import spell

TILE_SIZE = 50
WIDTH = 500
HEIGHT = 500

class Compy():
    def __init__(self, x, y):
        self.x = x # coordinates on the tile system
        self.y = y
        self.direction = {'N':True, 'S':False, 'E':False, 'W':False} # TODO a better way to store directions
        
    def move_forward(self):
        if self.direction['N']:
            self.y -= 1
        if self.direction['S']:
            self.y += 1
        if self.direction['E']:
            self.x += 1
        if self.direction['W']:
            self.x -= 1

    def turn_right(self):
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

    def turn_left(self):
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

    def canMoveNorth(self):
        return map[self.y-1][self.x] != 1

    def moveNorth(self):
        if self.canMoveNorth():
            self.y -= 1
        
    def canMoveSouth(self):
        return map[self.y+1][self.x] != 1

    def moveSouth(self):
        if self.canMoveSouth():
            self.y += 1
    
    def canMoveEast(self):
        return map[self.y][self.x+1] != 1

    def moveEast(self):
        if self.canMoveEast():
            self.x += 1
            
    def canMoveWest(self):
        return map[self.y][self.x-1] != 1

    def moveWest(self):
        if self.canMoveWest():
            self.x -= 1
            
    def isWon(self):
        if map[self.y][self.x] == 3:
            return True

    def render(self):
        pygame.draw.rect(screen, 
                         "red", 
                         ((WIDTH/2) - (TILE_SIZE/2), 
                          (HEIGHT/2) - (TILE_SIZE/2),
                          TILE_SIZE, 
                          TILE_SIZE))


def mazeGen():
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


def getTile(x, y):
    if x < 0 or x >= len(map[0]):
        return 2
    if y < 0 or y >= len(map):
        return 2

    return map[y][x]
    
def repl():
    global toPrompt
    if toPrompt:
        print("> ", end='', flush=True)
        toPrompt = False 
    if select.select([sys.stdin], [], [], 0) == ([sys.stdin], [], []):
        s = sys.stdin.readline()
        val = spell.evaluate(spell.read(s))
        toPrompt = True
        if val is not None:
            print(spell.schemestr(val))


def render():
    screen.fill("white")
    for y in range(11):
        for x in range(11):
            if getTile(compy.x-5+x, compy.y-5+y) == 1:
                pygame.draw.rect(screen, "black", 
                                 (x*TILE_SIZE - (TILE_SIZE/2), 
                                 y*TILE_SIZE - (TILE_SIZE/2),
                                 TILE_SIZE,
                                 TILE_SIZE))
            elif getTile(compy.x-5+x, compy.y-5+y) == 3:
                pygame.draw.rect(screen, "blue", 
                                 (x*TILE_SIZE - (TILE_SIZE/2), 
                                 y*TILE_SIZE - (TILE_SIZE/2),
                                 TILE_SIZE,
                                 TILE_SIZE))
    compy.render()
    pygame.display.flip()

pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Conzuror")

running = True
toPrompt = True
clock = pygame.time.Clock()
compy = Compy(1, 1)
map = [[1 if m%2 else n%2 for n in range(1, 100)] for m in range(1, 100)] # TODO remove magic numbers, too many magic numbers in the map TODO find a better way to represent maps
mazeGen()
map[len(map)-2][len(map[0])-2] = 3

spell.global_env["move-north"] = compy.moveNorth
spell.global_env["move-south"] = compy.moveSouth
spell.global_env["move-east"] = compy.moveEast
spell.global_env["move-west"] = compy.moveWest
spell.global_env["can-move-north"] = compy.canMoveNorth
spell.global_env["can-move-south"] = compy.canMoveSouth
spell.global_env["can-move-east"] = compy.canMoveEast
spell.global_env["can-move-west"] = compy.canMoveWest

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

    render()
    if compy.isWon():
        print("You Won")

    clock.tick(60) 

pygame.quit()
