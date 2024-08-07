from time import *
import pygame
import math

pygame.init()

BLACK = (0,0,0)
YELLOW = (255,255,0)
BLUE = (0,128,255)
RED = (245,143,11)
SOLID_RED = (201, 29, 34)
CREAM = (246, 228, 208)
ORANGE= (234, 135, 30)
CLEAR_GOLD = (246, 212, 100)
DARK_BLUE = (12, 18, 50)
LIGHT_BLUE = (143, 216, 216)
WHITE = (255,255,255)

W, H = 2000, 950

window = pygame.display.set_mode((W,H))
pygame.display.set_caption("Solar System Simulation")


class Planet:      #for each single planets
    AU = 149.6e6 * 1000 #meter
    G = 6.67428e-11 #gravity
    SCALE = 150 / AU  # 1AU = 100 pixels
    TIMESTEP = 3600 * 24  # 1 day

    def __init__(self,name,x,y,radius,color,mass):
        self.name = name
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.mass = mass
        self.orbit = []   #store positions
        self.between_sun = 0
        self.x_vel = 0
        self.y_vel = 0
        self.sun = False

    def draw_to_window(self,win):
        x = self.x * self.SCALE + W / 2
        y = self.y * self.SCALE + H / 2

        if len(self.orbit) > 2:
            updated_points = []
            for point in self.orbit:
                x, y = point
                x = x * self.SCALE + W / 2
                y = y * self.SCALE + H / 2
                updated_points.append((x,y))

            pygame.draw.lines(window,self.color,False, updated_points,2)

        pygame.draw.circle(win,self.color,(x,y),self.radius)

        font = pygame.font.Font(None,24)
        text = font.render(self.name,True,WHITE)
        text_rect = text.get_rect(center=(x, y + self.radius + 10))
        win.blit(text, text_rect)

    def interaction(self,other):
        other_x, other_y = other.x, other.y

        #distance
        distance_x = other_x - self.x
        distance_y = other_y - self.y
        distance = math.sqrt(distance_x ** 2 + distance_y ** 2)

        if other.sun:
            self.between_sun = distance

        #force
        force = self.G * self.mass * other.mass / distance ** 2
        theta_angle = math.atan2(distance_y,distance_x)
        force_x = math.cos(theta_angle) * force
        force_y = math.sin(theta_angle) * force
        return force_x,force_y


    def moving_position(self,planets):
        total_fx = total_fy = 0
        for planet in planets:
            if self == planet:
                continue

            fx,fy = self.interaction(planet)
            total_fx += fx
            total_fy += fy

        self.x_vel += total_fx / self.mass * self.TIMESTEP
        self.y_vel += total_fy / self.mass * self.TIMESTEP

        self.x += self.x_vel * self.TIMESTEP
        self.y += self.y_vel * self.TIMESTEP

        self.orbit.append((self.x,self.y))


def main():
    run = True
    clock = pygame.time.Clock()   #for updating the program per second

    sun = Planet("Sun",0,0, 40,YELLOW,1.98892 * 10**30)
    sun.sun = True

    mercury = Planet("Mercury", 0.387 * Planet.AU, 0, 4, SOLID_RED, 3.30 * 10 ** 23)
    mercury.y_vel = -47.4 * 1000

    venus = Planet("Venus", 0.72 * Planet.AU, 0, 8, CREAM, 4.867 * 10 ** 24)
    venus.y_vel = -35.02 * 1000

    earth = Planet("Earth",-1 * Planet.AU, 0, 10, BLUE, 5.9742 * 10 ** 24)
    earth.y_vel = 29.783 * 1000

    mars = Planet("Mars",-1.524 * Planet.AU, 0, 6, RED, 6.39 * 10 ** 23)
    mars.y_vel = 24.077 * 1000

    jupiter = Planet("Jupiter", 5.203 * Planet.AU, 0, 20, ORANGE, 1.898 * 10 ** 27)
    jupiter.y_vel = -13.06 * 1000

    saturn = Planet("Saturn", -9.537 * Planet.AU, 0, 18, CLEAR_GOLD, 5.683 * 10 ** 26)
    saturn.y_vel = 9.68 * 1000

    uranus = Planet("Uranus", 19.191 * Planet.AU, 0, 15, DARK_BLUE, 8.81 * 10 ** 25)
    uranus.y_vel = -6.79 * 1000

    neptune = Planet("Neptune", -30.068 * Planet.AU, 0, 14, LIGHT_BLUE, 102.4 * 10 ** 24)
    neptune.y_vel = 5.45 * 1000


    planets = [sun,mercury,venus,earth,mars,jupiter,saturn,uranus,neptune]

    while run:
        clock.tick(60)             #set run for 60 FPS
        window.fill((0,0,0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        for planet in planets:
            planet.moving_position(planets)
            planet.draw_to_window(window)

        pygame.display.update()

    pygame.quit()

main()








