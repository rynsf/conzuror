import pygame
import random


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

    def 
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
    
def checkWin():
    if map[compy.y][compy.x] == 3:
        print("you won")
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
clock = pygame.time.Clock()
compy = Compy(1, 1)
map = [[1 if m%2 else n%2 for n in range(1, 1000)] for m in range(1, 1000)] # TODO remove magic numbers TODO find a better way to represent maps
mazeGen()
map[len(map)-2][len(map[0])-2] = 3

while running:
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            running = False
        if e.type == pygame.KEYDOWN:
            if e.key == pygame.K_w:
                if map[compy.y-1][compy.x] != 1:
                    compy.y -= 1
            if e.key == pygame.K_s:
                if map[compy.y+1][compy.x] != 1:
                    compy.y += 1
            if e.key == pygame.K_a:
                if map[compy.y][compy.x-1] != 1:
                    compy.x -= 1
            if e.key == pygame.K_d:
                if map[compy.y][compy.x+1] != 1:
                    compy.x += 1

    render()
    checkWin()
    clock.tick(60) 

pygame.quit()
