import pygame
import random
from constants import *
from circleshape import CircleShape

class Asteroid(CircleShape):

    def __init__(self, x, y, radius):
        super().__init__(x, y, radius)
        
    def draw(self, screen):
        pygame.draw.circle(screen, "orange", self.position, self.radius, 2)
    
    def update(self, dt):
        self.position += self.velocity * dt

    def split(self):        
        self.kill()
        
        if self.radius <= ASTEROID_MIN_RADIUS:
            return
        
        new_Angle = random.uniform(20, 50)

        chunk1 = self.velocity.rotate(new_Angle)
        chunk2 = self.velocity.rotate(-new_Angle)
        
        new_radius = self.radius - ASTEROID_MIN_RADIUS
        
        asteroid = Asteroid(self.position.x, self.position.y , new_radius)
        asteroid.velocity = chunk1 * 1.2
        asteroid = Asteroid(self.position.x, self.position.y , new_radius)
        asteroid.velocity = chunk2 * 1.2