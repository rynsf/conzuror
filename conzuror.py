import pygame
import random
import select
import sys
import spell

TILE_SIZE = 50
WIDTH = 500
HEIGHT = 500
SPELL_PER_SECOND = 2
FPS = 60

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
        return map[self.y-1][self.x] != 1

    def moveNorth(self):
        if self.canMoveNorth():
            self.y -= 1
        render(SPELL_PER_SECOND)
        
    def canMoveSouth(self):
        return map[self.y+1][self.x] != 1

    def moveSouth(self):
        if self.canMoveSouth():
            self.y += 1
        render(SPELL_PER_SECOND)
    
    def canMoveEast(self):
        return map[self.y][self.x+1] != 1

    def moveEast(self):
        if self.canMoveEast():
            self.x += 1
        render(SPELL_PER_SECOND)
            
    def canMoveWest(self):
        return map[self.y][self.x-1] != 1

    def moveWest(self):
        if self.canMoveWest():
            self.x -= 1
        render(SPELL_PER_SECOND)
            
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

def render(hz):
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
    clock.tick(hz) 

def help():
    print(
"""Conzuror
You are a conjuror. You cast spells. With your spells you
control the computer. You cast spells in a programming 
language called spell, which is a lisp. While, you can
also use keystrokes to  
control the computer,                 ↑
which is good for basic                W
movements. You grasp the          ← A     D→
true power of what the                 S
computer is capable of                ↓   
once you master the art 
of casting spells. Lets have a basic look at how spell works.

Spell
Spell is your magic language. There are three kind of entities
that can be written in a spell code. They are:
* Numbers - like 7, or 2.
* Atoms - are names and symbols.
* Lists - A group of entities enclosed in parenthesis '( )'. 
          Lists can contain any number of elements and even 
          other lists.

Function calls
Spell is written with lists, which is its own data structure.
The first elements of a list is considered to be a procedure,
the other elements as arguments which are passed to the
procedure.

'+' is a function in spell which, you guess, adds. To add 
numbers you would call '+' passing the numbers to be added 
as arguments. Like this:

 > (+ 5 1 3)
 9

Spell have alot of these functions. They are the way by 
which you task the computer to do something. You can also 
define your own procedures. When you finally learn that
you will become a true magician. You will be able to 
command the computer at your will. But first, lets see 
some more spells:

Procedure calls can contain other procedure calls which 
will be evaluated first and the value of which will be 
passed to the outer call. 

 > (+ 2 (- 5 3))
 4
""")

pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Conzuror")

running = True
toPrompt = True
numOpenParen = 0
prompt = ""
clock = pygame.time.Clock()
compy = Compy(1, 1)
map = [[1 if m%2 else n%2 for n in range(1, 100)] for m in range(1, 100)] # TODO remove magic numbers, too many magic numbers in the map TODO find a better way to represent maps
mazeGen()
map[len(map)-2][len(map[0])-2] = 3

spell.global_env["move-north"] = compy.moveNorth
spell.global_env["move-south"] = compy.moveSouth
spell.global_env["move-east"] = compy.moveEast
spell.global_env["move-west"] = compy.moveWest
spell.global_env["can-move-north?"] = compy.canMoveNorth
spell.global_env["can-move-south?"] = compy.canMoveSouth
spell.global_env["can-move-east?"] = compy.canMoveEast
spell.global_env["can-move-west?"] = compy.canMoveWest
spell.global_env["is-won?"] = compy.isWon
spell.global_env["can-move-right?"] = compy.canMoveRight
spell.global_env["turn-right"] = compy.turnRight
spell.global_env["can-move-left?"] = compy.canMoveLeft
spell.global_env["turn-left"] = compy.turnLeft
spell.global_env["can-move-forward?"] = compy.canMoveForward
spell.global_env["move-forward"] = compy.moveForward
spell.global_env["help"] = help

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

    render(FPS)
    if compy.isWon():
        print("You Won")

pygame.quit()
