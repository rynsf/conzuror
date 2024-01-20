import pygame
from constant import *

class Hanoi():
    def __init__(self, x, y, screen, map, renderer):
        self.x = x
        self.y = y
        self.w = 300
        self.h = 150
        self.stacks = [[n for n in range(1, 11)], [], []]
        self.renderer = renderer
        self.screen = screen
        for n in range(y, y+(self.h//TILE_SIZE)):
            for m in range(x, x+(self.w//TILE_SIZE)):
                map[n][m] = self
        
    def move(self, src, dst):
        if (src in (0, 1, 2) 
            and dst in (0, 1, 2) 
            and len(self.stacks[src]) != 0):
            if (len(self.stacks[dst]) == 0
                or self.stacks[dst][0] > self.stacks[src][0]):
                self.stacks[dst].insert(0, self.stacks[src].pop(0))
                self.renderer(20)
                return
        print("Invalid move")

    def render(self, playerx, playery):
        surface = pygame.Surface((self.w, self.h))
        surface.fill("white")
        pygame.draw.rect(surface, 
                         "orange", 
                         (0, 130, self.w, 20)) # TODO magic numbers
        pygame.draw.line(surface, 
                         "black",
                         (50, 0),
                         (50, 130),
                         2)
        pygame.draw.line(surface, 
                         "black",
                         (150, 0),
                         (150, 130),
                         2)
        pygame.draw.line(surface, 
                         "black",
                         (250, 0),
                         (250, 130),
                         2)
        x = 50
        for s in self.stacks:
            y = 120
            for n in s[::-1]:
                pygame.draw.rect(surface, 
                                 "green",
                                 (x - n*5, y, n*10, 10))
                y -= 10
            x += 100
        self.screen.blit(surface, 
                     (WIDTH/2 - TILE_SIZE/2 + ((self.x - playerx) * TILE_SIZE), 
                      HEIGHT/2 - TILE_SIZE/2 + ((self.y - playery) * TILE_SIZE),
                      self.w, 
                      self.h)) 
